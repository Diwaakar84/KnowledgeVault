from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from app.db.session import get_db
from app.models.document import IndexedDocument
from jose import jwt, JWTError
from fastapi import Request
from app.config import JWT_SECRET, JWT_ALGORITHM
from app.services.index_service import index_document, delete_document

# Router for these APIs prefixing all endpoints with /media
router = APIRouter(prefix="/search", tags=["search"])

# Verify the current user token to check if he is an authenticated user or not 
def get_current_user(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing auth token")

    token = auth_header.split(" ")[1]

    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload["sub"]
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# API request formats
class IndexRequest(BaseModel):
    source_id: str
    title: str
    content: str

class SearchResult(BaseModel):
    source_id: str
    title: str
    snippet: str

# Create an index for the specified document
@router.post("/index")
def index(
    data: IndexRequest,
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    index_document(db, user_id, data.source_id, data.title, data.content)
    return {"status": "indexed"}

# Delete the index for the note specified
@router.delete("/index/{source_id}")
def delete_index(
    source_id: str,
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    delete_document(db, user_id, source_id)
    return {"status": "deleted"}

# Search the specified note
@router.get("")
def search(
    q: str = Query(..., min_length=1),
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    results = db.query(IndexedDocument).filter(
        IndexedDocument.user_id == user_id,
        (IndexedDocument.title.ilike(f"%{q}%")) |
        (IndexedDocument.content.ilike(f"%{q}%"))
    ).limit(20).all()

    return [
        {
            "source_id": str(doc.source_id),
            "title": doc.title,
            "snippet": doc.content[:150]
        }
        for doc in results
    ]
