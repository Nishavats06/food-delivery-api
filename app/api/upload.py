from fastapi import APIRouter, Depends, UploadFile, File
from app.core.cloudinary_config import upload_image
from app.schemas.response import ResponseWrapper
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.response import ResponseWrapper, ImageUploadOut

router = APIRouter(prefix="/upload", tags=["Upload"])


@router.post("/image", response_model=ResponseWrapper[ImageUploadOut])
def upload_image_endpoint(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
):
    image_url = upload_image(file.file, folder="uploads")
    return ResponseWrapper(success=True, message="Image uploaded successfully", data=ImageUploadOut(image_url=image_url))