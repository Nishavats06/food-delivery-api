from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi import UploadFile, File

from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserOut, Token
from app.schemas.response import ResponseWrapper
from app.core.security import hash_password, verify_password, create_access_token
from app.api.deps import get_current_user
from app.core.cloudinary_config import upload_image
from app.schemas.google_auth import GoogleLoginRequest
from app.core.google_auth import verify_google_token
from app.models.user import User, UserRole
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=ResponseWrapper[UserOut], status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_in.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    new_user = User(
        first_name=user_in.first_name,
        last_name=user_in.last_name,
        email=user_in.email,
        phone_number=user_in.phone_number,
        hashed_password=hash_password(user_in.password),
        role=user_in.role,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return ResponseWrapper(success=True, message="Registration successful", data=new_user)


@router.post("/login", response_model=ResponseWrapper[Token])
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")

    access_token = create_access_token(data={"sub": user.email})
    token = Token(access_token=access_token, token_type="bearer")
    return ResponseWrapper(success=True, message="Login successful", data=token)


@router.get("/me", response_model=ResponseWrapper[UserOut])
def read_current_user(current_user: User = Depends(get_current_user)):
    return ResponseWrapper(success=True, message="success", data=current_user)

@router.post("/me/profile-picture", response_model=ResponseWrapper[UserOut])
def upload_profile_picture(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    image_url = upload_image(file.file, folder="profile_pictures")
    current_user.profile_picture_url = image_url
    db.commit()
    db.refresh(current_user)
    return ResponseWrapper(success=True, message="Profile picture updated successfully", data=current_user)

@router.post("/google-login", response_model=ResponseWrapper[Token])
def google_login(payload: GoogleLoginRequest, db: Session = Depends(get_db)):
    google_data = verify_google_token(payload.id_token)
    if not google_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Google token")

    user = db.query(User).filter(User.email == google_data["email"]).first()

    if not user:
        user = User(
            first_name=google_data["first_name"],
            last_name=google_data["last_name"],
            email=google_data["email"],
            hashed_password=hash_password(google_data["email"] + settings.SECRET_KEY),
            profile_picture_url=google_data["profile_picture_url"],
            role=UserRole.CUSTOMER,
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    access_token = create_access_token(data={"sub": user.email})
    token = Token(access_token=access_token, token_type="bearer")
    return ResponseWrapper(success=True, message="Google login successful", data=token)