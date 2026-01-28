from sqlalchemy.orm import Session
from app.models.note import Note, NoteVersion, NoteTag

# Create a new note in the DB
def create_note(db: Session, user_id: str, title: str, content: str, tags: list[str]):
    note = Note(user_id=user_id)
    db.add(note)
    db.flush()

    version = NoteVersion(
        note_id=note.id,
        title=title,
        content=content
    )
    db.add(version)

    for tag in tags:
        db.add(NoteTag(note_id=note.id, tag=tag))

    db.commit()
    db.refresh(note)

    return note, version

# Update an existing note in the DB
def update_note(db: Session, note: Note, title: str, content: str, tags: list[str]):
    note.current_version += 1

    version = NoteVersion(
        note_id=note.id,
        title=title,
        content=content
    )
    db.add(version)

    db.query(NoteTag).filter(NoteTag.note_id == note.id).delete()
    for tag in tags:
        db.add(NoteTag(note_id=note.id, tag=tag))

    db.commit()
    return version

# Soft delete the data to keep it recoverable
def soft_delete_note(db: Session, note: Note):
    note.is_deleted = True
    db.commit()
