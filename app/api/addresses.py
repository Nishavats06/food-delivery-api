from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.models.user import User
from app.models.address import Address
from app.schemas.address import AddressCreate, AddressOut
from app.schemas.response import ResponseWrapper
from app.api.deps import get_current_user

router = APIRouter(prefix="/addresses", tags=["Addresses"])


@router.get("", response_model=ResponseWrapper[List[AddressOut]])
def list_addresses(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    addresses = db.query(Address).filter(Address.user_id == current_user.id).all()
    return ResponseWrapper(success=True, message="success", data=addresses)


@router.post("", response_model=ResponseWrapper[AddressOut], status_code=status.HTTP_201_CREATED)
def create_address(
    address_in: AddressCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if address_in.is_default:
        db.query(Address).filter(Address.user_id == current_user.id).update({"is_default": False})

    new_address = Address(
        user_id=current_user.id,
        label=address_in.label,
        location=address_in.location.model_dump(),
        is_default=address_in.is_default,
    )
    db.add(new_address)
    db.commit()
    db.refresh(new_address)
    return ResponseWrapper(success=True, message="Address created successfully", data=new_address)


@router.delete("/{address_id}", response_model=ResponseWrapper[None])
def delete_address(
    address_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    address = db.query(Address).filter(
        Address.id == address_id, Address.user_id == current_user.id
    ).first()
    if not address:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Address not found")

    db.delete(address)
    db.commit()
    return ResponseWrapper(success=True, message="Address deleted successfully", data=None)




# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session
# from typing import List

# from app.db.session import get_db
# from app.models.user import User
# from app.models.address import Address
# from app.schemas.address import AddressCreate, AddressOut
# from app.api.deps import get_current_user

# router = APIRouter(prefix="/addresses", tags=["Addresses"])


# @router.get("", response_model=List[AddressOut])
# def list_addresses(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
#     return db.query(Address).filter(Address.user_id == current_user.id).all()


# @router.post("", response_model=AddressOut, status_code=status.HTTP_201_CREATED)
# def create_address(
#     address_in: AddressCreate,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user),
# ):
#     if address_in.is_default:
#         db.query(Address).filter(Address.user_id == current_user.id).update({"is_default": False})

#     new_address = Address(
#         user_id=current_user.id,
#         label=address_in.label,
#         location=address_in.location.model_dump(),
#         is_default=address_in.is_default,
#     )
#     db.add(new_address)
#     db.commit()
#     db.refresh(new_address)
#     return new_address


# @router.delete("/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_address(
#     address_id: int,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user),
# ):
#     address = db.query(Address).filter(
#         Address.id == address_id, Address.user_id == current_user.id
#     ).first()
#     if not address:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Address not found")

#     db.delete(address)
#     db.commit()
#     return None