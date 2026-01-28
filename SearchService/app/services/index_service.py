from sqlalchemy.orm import Session
from app.models.document import IndexedDocument

# Create index for a note
def index_document(db: Session, user_id: str, source_id: str, title: str, content: str):
    # Delete old index and insert new in case of update
    db.query(IndexedDocument).filter(
        IndexedDocument.source_id == source_id,
        IndexedDocument.user_id == user_id
    ).delete()

    doc = IndexedDocument(
        user_id=user_id,
        source_id=source_id,
        title=title,
        content=content
    )

    db.add(doc)
    db.commit()
    return doc

# Delete the index 
def delete_document(db: Session, user_id: str, source_id: str):
    db.query(IndexedDocument).filter(
        IndexedDocument.source_id == source_id,
        IndexedDocument.user_id == user_id
    ).delete()
    db.commit()
