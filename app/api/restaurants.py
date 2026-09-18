from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional, List

from app.db.session import get_db
from app.models.user import User
from app.models.restaurant import Restaurant
from app.schemas.restaurant import RestaurantCreate, RestaurantUpdate, RestaurantOut
from app.schemas.response import ResponseWrapper
from app.api.deps import require_owner

router = APIRouter(prefix="/restaurants", tags=["Restaurants"])


@router.get("", response_model=ResponseWrapper[List[RestaurantOut]])
def list_restaurants(
    search: Optional[str] = None,
    category_id: Optional[int] = None,
    cuisine_type: Optional[str] = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    query = db.query(Restaurant)
    if search:
        query = query.filter(Restaurant.name.ilike(f"%{search}%"))
    if category_id:
        query = query.filter(Restaurant.category_id == category_id)
    if cuisine_type:
        query = query.filter(Restaurant.cuisine_type.ilike(f"%{cuisine_type}%"))
    restaurants = query.offset(skip).limit(limit).all()
    return ResponseWrapper(success=True, message="success", data=restaurants)


@router.post("", response_model=ResponseWrapper[RestaurantOut], status_code=status.HTTP_201_CREATED)
def create_restaurant(
    restaurant_in: RestaurantCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_owner),
):
    new_restaurant = Restaurant(
        name=restaurant_in.name,
        description=restaurant_in.description,
        address=restaurant_in.address.model_dump(),
        cuisine_type=restaurant_in.cuisine_type,
        image_url=restaurant_in.image_url,
        category_id=restaurant_in.category_id,
        owner_id=current_user.id,
    )
    db.add(new_restaurant)
    db.commit()
    db.refresh(new_restaurant)
    return ResponseWrapper(success=True, message="Restaurant created successfully", data=new_restaurant)


@router.get("/{restaurant_id}", response_model=ResponseWrapper[RestaurantOut])
def get_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")
    return ResponseWrapper(success=True, message="success", data=restaurant)


@router.patch("/{restaurant_id}", response_model=ResponseWrapper[RestaurantOut])
def update_restaurant(
    restaurant_id: int,
    restaurant_in: RestaurantUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_owner),
):
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")
    if restaurant.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your restaurant")

    update_data = restaurant_in.model_dump(exclude_unset=True)
    if "address" in update_data and update_data["address"] is not None:
        update_data["address"] = restaurant_in.address.model_dump()
    for field, value in update_data.items():
        setattr(restaurant, field, value)

    db.commit()
    db.refresh(restaurant)
    return ResponseWrapper(success=True, message="Restaurant updated successfully", data=restaurant)


@router.delete("/{restaurant_id}", response_model=ResponseWrapper[None])
def delete_restaurant(
    restaurant_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_owner),
):
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")
    if restaurant.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your restaurant")

    db.delete(restaurant)
    db.commit()
    return ResponseWrapper(success=True, message="Restaurant deleted successfully", data=None)


# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session
# from typing import Optional, List

# from app.db.session import get_db
# from app.models.user import User
# from app.models.restaurant import Restaurant
# from app.schemas.restaurant import RestaurantCreate, RestaurantUpdate, RestaurantOut
# from app.api.deps import require_owner

# router = APIRouter(prefix="/restaurants", tags=["Restaurants"])



# @router.get("", response_model=List[RestaurantOut])
# def list_restaurants(
#     search: Optional[str] = None,
#     category_id: Optional[int] = None,
#     cuisine_type: Optional[str] = None,
#     skip: int = 0,
#     limit: int = 10,
#     db: Session = Depends(get_db),
# ):
#     query = db.query(Restaurant)

#     if search:
#         query = query.filter(Restaurant.name.ilike(f"%{search}%"))

#     if category_id:
#         query = query.filter(Restaurant.category_id == category_id)

#     if cuisine_type:
#         query = query.filter(Restaurant.cuisine_type.ilike(f"%{cuisine_type}%"))

#     restaurants = query.offset(skip).limit(limit).all()
#     return restaurants

# @router.post("", response_model=RestaurantOut, status_code=status.HTTP_201_CREATED)
# def create_restaurant(
#     restaurant_in: RestaurantCreate,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(require_owner),
# ):
#     new_restaurant = Restaurant(
#         name=restaurant_in.name,
#         description=restaurant_in.description,
#         address=restaurant_in.address.model_dump(),
#         cuisine_type=restaurant_in.cuisine_type,
#         image_url=restaurant_in.image_url,
#         category_id=restaurant_in.category_id,
#         owner_id=current_user.id,
#     )
#     db.add(new_restaurant)
#     db.commit()
#     db.refresh(new_restaurant)
#     return new_restaurant


# @router.get("/{restaurant_id}", response_model=RestaurantOut)
# def get_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
#     restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
#     if not restaurant:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")
#     return restaurant


# @router.patch("/{restaurant_id}", response_model=RestaurantOut)
# def update_restaurant(
#     restaurant_id: int,
#     restaurant_in: RestaurantUpdate,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(require_owner),
# ):
#     restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
#     if not restaurant:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")

#     if restaurant.owner_id != current_user.id:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your restaurant")

#     update_data = restaurant_in.model_dump(exclude_unset=True)
#     for field, value in update_data.items():
#         setattr(restaurant, field, value)

#     db.commit()
#     db.refresh(restaurant)
#     return restaurant


# @router.delete("/{restaurant_id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_restaurant(
#     restaurant_id: int,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(require_owner),
# ):
#     restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
#     if not restaurant:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")

#     if restaurant.owner_id != current_user.id:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your restaurant")

#     db.delete(restaurant)
#     db.commit()
#     return None