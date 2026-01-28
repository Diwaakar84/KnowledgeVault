from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.db.session import get_db
from app.middleware.auth import get_current_user
from app.models.media import MediaFile
from app.services.storage_service import generate_presigned_upload

# Router for these APIs prefixing all endpoints with /media
router = APIRouter(prefix="/media", tags=["media"])

# API request format
class UploadRequest(BaseModel):
    file_name: str
    file_type: str

class UploadResponse(BaseModel):
    upload_url: str
    file_id: str

# File upload API
@router.post("/upload-url", response_model=UploadResponse)
def get_upload_url(
    data: UploadRequest,
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    upload_url, key = generate_presigned_upload(data.file_name, data.file_type)

    media = MediaFile(
        user_id=user_id,
        file_name=data.file_name,
        file_type=data.file_type,
        s3_key=key
    )

    db.add(media)
    db.commit()
    db.refresh(media)

    return {
        "upload_url": upload_url,
        "file_id": str(media.id)
    }
