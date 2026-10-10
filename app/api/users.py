from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserOut, UserUpdate
from app.schemas.response import ResponseWrapper
from app.api.deps import get_current_user
from app.core.common_responses import UNAUTHORIZED_RESPONSE

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=ResponseWrapper[UserOut], responses=UNAUTHORIZED_RESPONSE)
def read_current_user(current_user: User = Depends(get_current_user)):
    return ResponseWrapper(success=True, message="success", data=current_user)


@router.patch("/me", response_model=ResponseWrapper[UserOut], responses=UNAUTHORIZED_RESPONSE)
def update_current_user(
    user_in: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    update_data = user_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(current_user, field, value)
    db.commit()
    db.refresh(current_user)
    return ResponseWrapper(success=True, message="Profile updated successfully", data=current_user)


@router.delete("/me", response_model=ResponseWrapper[None], responses=UNAUTHORIZED_RESPONSE)
def delete_current_user(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db.delete(current_user)
    db.commit()
    return ResponseWrapper(success=True, message="Account deleted successfully", data=None)