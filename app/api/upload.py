from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from app.core.cloudinary_config import upload_image
from app.schemas.response import ResponseWrapper, ImageUploadOut
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/upload", tags=["Upload"])

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB
ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp", "image/jpg"}


@router.post("/file", response_model=ResponseWrapper[ImageUploadOut])
async def upload_file_endpoint(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
):
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file type '{file.content_type}'. Allowed: jpeg, png, webp",
        )

    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File too large. Maximum allowed size is 5MB",
        )

    file.file.seek(0)
    image_url = upload_image(file.file, folder="uploads")
    return ResponseWrapper(success=True, message="File uploaded successfully", data=ImageUploadOut(image_url=image_url))