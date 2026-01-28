from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from app.config import SEARCH_SERVICE_URL
from app.db.session import get_db
from app.middleware.auth import get_current_user
from app.models.note import Note, NoteVersion
from app.services.note_service import create_note, update_note, soft_delete_note
import httpx
from app.cache.sharded_redis import ShardedRedis, REDIS_NODES
import json

# Router for these APIs prefixing all endpoints with /auth
router = APIRouter(prefix="/notes", tags=["notes"])

sharded_cache = ShardedRedis(REDIS_NODES)

# Request formats for the endpoints
class NoteCreate(BaseModel):
    title: str
    content: str
    tags: List[str] = []

class NoteUpdate(BaseModel):
    title: str
    content: str
    tags: List[str] = []

class NoteOut(BaseModel):
    id: str
    title: str
    content: str
    tags: List[str]
    version: int

# Create a new note
@router.post("")
async def create(
    data: NoteCreate, 
    request: Request,
    user_id: str = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    # Create the note in the DB
    note, version = create_note(db, user_id, data.title, data.content, data.tags)

    try:
        async with httpx.AsyncClient() as client:
            # Create search indexing to make future access faster
            await client.post(
                f"{SEARCH_SERVICE_URL}/search/index",
                headers={"Authorization": request.headers.get("Authorization")},
                json={
                    "source_id": str(note.id),
                    "title": data.title,
                    "content": data.content
                },
                timeout=2.0
            )
    except Exception as e:
        print("Search indexing failed:", e)
    
    return {"id": str(note.id), "version": note.current_version}

# Fetch the list of notes created by the user
@router.get("")
def list_notes(user_id: str = Depends(get_current_user), db: Session = Depends(get_db)):
    notes = db.query(Note).filter(
        Note.user_id == user_id,
        Note.is_deleted == False
    ).all()

    result = []
    for note in notes:
        version = db.query(NoteVersion).filter(
            NoteVersion.note_id == note.id
        ).order_by(NoteVersion.created_at.desc()).first()

        result.append({
            "id": str(note.id),
            "title": version.title,
            "content": version.content,
            "version": note.current_version
        })

    return result

# Fetch the specific note of the user
@router.get("/{note_id}")
def get(note_id: str, user_id: str = Depends(get_current_user), db: Session = Depends(get_db)):
    cache_key = f"note:{user_id}:{note_id}"

    # 1. Try cache
    # Check if that note is present in the cache 
    cached = sharded_cache.get(cache_key)
    if cached:
        return json.loads(cached)

    
    # 2. DB fetch
    # If the note isn't present in the cache fetch from the DB
    note = db.query(Note).filter(
        Note.id == note_id,
        Note.user_id == user_id,
        Note.is_deleted == False
    ).first()

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    version = db.query(NoteVersion).filter(
        NoteVersion.note_id == note.id
    ).order_by(NoteVersion.created_at.desc()).first()

    result = {
        "id": str(note.id),
        "title": version.title,
        "content": version.content,
        "version": note.current_version
    }

    # 3. Store in cache (TTL = 60s)
    # Store the fetched note in the DB
    sharded_cache.setex(cache_key, 60, json.dumps(result))

    return result

# Update a specific note of the user
@router.put("/{note_id}")
async def update(
    note_id: str, 
    request: Request,
    data: NoteUpdate, 
    user_id: str = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    note = db.query(Note).filter(
        Note.id == note_id,
        Note.user_id == user_id,
        Note.is_deleted == False
    ).first()

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    version = update_note(db, note, data.title, data.content, data.tags)

    try:
        async with httpx.AsyncClient() as client:
            # Recreate the search index as the note was modified
            await client.post(
                f"{SEARCH_SERVICE_URL}/search/index",
                headers={"Authorization": request.headers.get("Authorization")},
                json={
                    "source_id": str(note.id),
                    "title": data.title,
                    "content": data.content
                },
                timeout=2.0
            )
    except Exception as e:
        print("Search reindex failed:", e)

    # Delete the note from the cache as the value in the cache is outdated
    cache_key = f"note:{user_id}:{note.id}"
    sharded_cache.delete(cache_key)

    return {"version": note.current_version}

# Delete a specific note
@router.delete("/{note_id}")
async def delete(
    note_id: str, 
    request: Request,
    user_id: str = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    note = db.query(Note).filter(
        Note.id == note_id,
        Note.user_id == user_id,
        Note.is_deleted == False
    ).first()

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    soft_delete_note(db, note)

    try:
        async with httpx.AsyncClient() as client:
            # Delete the serach index for the note
            await client.delete(
                f"{SEARCH_SERVICE_URL}/search/index/{note.id}",
                headers={"Authorization": request.headers.get("Authorization")},
                timeout=2.0
            )
    except Exception as e:
        print("Search delete failed:", e)

    # Delete the note from the cache if present
    cache_key = f"note:{user_id}:{note.id}"
    sharded_cache.delete(cache_key)

    return {"status": "deleted"}
