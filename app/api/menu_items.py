from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.models.user import User
from app.models.restaurant import Restaurant
from app.models.menu_item import MenuItem
from app.schemas.menu_item import MenuItemCreate, MenuItemUpdate, MenuItemOut
from app.schemas.response import ResponseWrapper
from app.api.deps import require_owner

router = APIRouter(tags=["Menu"])


def get_owned_restaurant(restaurant_id: int, db: Session, current_user: User) -> Restaurant:
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")
    if restaurant.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your restaurant")
    return restaurant


@router.post("/restaurants/{restaurant_id}/menu", response_model=ResponseWrapper[MenuItemOut], status_code=status.HTTP_201_CREATED)
def create_menu_item(
    restaurant_id: int,
    item_in: MenuItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_owner),
):
    get_owned_restaurant(restaurant_id, db, current_user)

    new_item = MenuItem(
        restaurant_id=restaurant_id,
        name=item_in.name,
        description=item_in.description,
        price=item_in.price,
        image_url=item_in.image_url,
        category_id=item_in.category_id,
        is_available=item_in.is_available,
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return ResponseWrapper(success=True, message="Menu item created successfully", data=new_item)


@router.get("/restaurants/{restaurant_id}/menu", response_model=ResponseWrapper[List[MenuItemOut]])
def list_menu_items(restaurant_id: int, db: Session = Depends(get_db)):
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")

    items = db.query(MenuItem).filter(MenuItem.restaurant_id == restaurant_id).all()
    return ResponseWrapper(success=True, message="success", data=items)


@router.patch("/menu/{item_id}", response_model=ResponseWrapper[MenuItemOut])
def update_menu_item(
    item_id: int,
    item_in: MenuItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_owner),
):
    item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not found")

    get_owned_restaurant(item.restaurant_id, db, current_user)

    update_data = item_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(item, field, value)

    db.commit()
    db.refresh(item)
    return ResponseWrapper(success=True, message="Menu item updated successfully", data=item)


@router.delete("/menu/{item_id}", response_model=ResponseWrapper[None])
def delete_menu_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_owner),
):
    item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not found")

    get_owned_restaurant(item.restaurant_id, db, current_user)

    db.delete(item)
    db.commit()
    return ResponseWrapper(success=True, message="Menu item deleted successfully", data=None)


# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session
# from typing import List

# from app.db.session import get_db
# from app.models.user import User
# from app.models.restaurant import Restaurant
# from app.models.menu_item import MenuItem
# from app.schemas.menu_item import MenuItemCreate, MenuItemUpdate, MenuItemOut
# from app.api.deps import require_owner

# router = APIRouter(tags=["Menu"])


# def get_owned_restaurant(restaurant_id: int, db: Session, current_user: User) -> Restaurant:
#     restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
#     if not restaurant:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")
#     if restaurant.owner_id != current_user.id:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your restaurant")
#     return restaurant


# @router.post("/restaurants/{restaurant_id}/menu", response_model=MenuItemOut, status_code=status.HTTP_201_CREATED)
# def create_menu_item(
#     restaurant_id: int,
#     item_in: MenuItemCreate,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(require_owner),
# ):
#     get_owned_restaurant(restaurant_id, db, current_user)

#     new_item = MenuItem(
#         restaurant_id=restaurant_id,
#         name=item_in.name,
#         description=item_in.description,
#         price=item_in.price,
#         image_url=item_in.image_url,
#         category_id=item_in.category_id,
#         is_available=item_in.is_available,
#     )
#     db.add(new_item)
#     db.commit()
#     db.refresh(new_item)
#     return new_item


# @router.get("/restaurants/{restaurant_id}/menu", response_model=List[MenuItemOut])
# def list_menu_items(restaurant_id: int, db: Session = Depends(get_db)):
#     restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
#     if not restaurant:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")

#     items = db.query(MenuItem).filter(MenuItem.restaurant_id == restaurant_id).all()
#     return items


# @router.patch("/menu/{item_id}", response_model=MenuItemOut)
# def update_menu_item(
#     item_id: int,
#     item_in: MenuItemUpdate,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(require_owner),
# ):
#     item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
#     if not item:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not found")

#     get_owned_restaurant(item.restaurant_id, db, current_user)

#     update_data = item_in.model_dump(exclude_unset=True)
#     for field, value in update_data.items():
#         setattr(item, field, value)

#     db.commit()
#     db.refresh(item)
#     return item


# @router.delete("/menu/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_menu_item(
#     item_id: int,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(require_owner),
# ):
#     item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
#     if not item:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not found")

#     get_owned_restaurant(item.restaurant_id, db, current_user)

#     db.delete(item)
#     db.commit()
#     return None