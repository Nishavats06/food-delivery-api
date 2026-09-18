from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List

from app.db.session import get_db
from app.models.user import User
from app.models.restaurant import Restaurant
from app.models.review import Review
from app.schemas.review import ReviewCreate, ReviewUpdate, ReviewOut
from app.schemas.response import ResponseWrapper
from app.api.deps import get_current_user

router = APIRouter(tags=["Reviews"])


@router.post("/restaurants/{restaurant_id}/reviews", response_model=ResponseWrapper[ReviewOut], status_code=status.HTTP_201_CREATED)
def create_review(
    restaurant_id: int,
    review_in: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")

    new_review = Review(
        user_id=current_user.id,
        restaurant_id=restaurant_id,
        rating=review_in.rating,
        comment=review_in.comment,
    )
    db.add(new_review)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You have already reviewed this restaurant")

    db.refresh(new_review)
    return ResponseWrapper(success=True, message="Review submitted successfully", data=new_review)


@router.get("/restaurants/{restaurant_id}/reviews", response_model=ResponseWrapper[List[ReviewOut]])
def list_reviews(restaurant_id: int, db: Session = Depends(get_db)):
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")

    reviews = db.query(Review).filter(Review.restaurant_id == restaurant_id).all()
    return ResponseWrapper(success=True, message="success", data=reviews)


@router.patch("/reviews/{review_id}", response_model=ResponseWrapper[ReviewOut])
def update_review(
    review_id: int,
    review_in: ReviewUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
    if review.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your review")

    update_data = review_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(review, field, value)

    db.commit()
    db.refresh(review)
    return ResponseWrapper(success=True, message="Review updated successfully", data=review)


@router.delete("/reviews/{review_id}", response_model=ResponseWrapper[None])
def delete_review(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
    if review.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your review")

    db.delete(review)
    db.commit()
    return ResponseWrapper(success=True, message="Review deleted successfully", data=None)



# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session
# from sqlalchemy.exc import IntegrityError
# from typing import List

# from app.db.session import get_db
# from app.models.user import User
# from app.models.restaurant import Restaurant
# from app.models.review import Review
# from app.schemas.review import ReviewCreate, ReviewUpdate, ReviewOut
# from app.api.deps import get_current_user

# router = APIRouter(tags=["Reviews"])


# @router.post("/restaurants/{restaurant_id}/reviews", response_model=ReviewOut, status_code=status.HTTP_201_CREATED)
# def create_review(
#     restaurant_id: int,
#     review_in: ReviewCreate,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user),
# ):
#     restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
#     if not restaurant:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")

#     new_review = Review(
#         user_id=current_user.id,
#         restaurant_id=restaurant_id,
#         rating=review_in.rating,
#         comment=review_in.comment,
#     )
#     db.add(new_review)
#     try:
#         db.commit()
#     except IntegrityError:
#         db.rollback()
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You have already reviewed this restaurant")

#     db.refresh(new_review)
#     return new_review


# @router.get("/restaurants/{restaurant_id}/reviews", response_model=List[ReviewOut])
# def list_reviews(restaurant_id: int, db: Session = Depends(get_db)):
#     restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
#     if not restaurant:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")

#     return db.query(Review).filter(Review.restaurant_id == restaurant_id).all()


# @router.patch("/reviews/{review_id}", response_model=ReviewOut)
# def update_review(
#     review_id: int,
#     review_in: ReviewUpdate,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user),
# ):
#     review = db.query(Review).filter(Review.id == review_id).first()
#     if not review:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
#     if review.user_id != current_user.id:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your review")

#     update_data = review_in.model_dump(exclude_unset=True)
#     for field, value in update_data.items():
#         setattr(review, field, value)

#     db.commit()
#     db.refresh(review)
#     return review


# @router.delete("/reviews/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_review(
#     review_id: int,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user),
# ):
#     review = db.query(Review).filter(Review.id == review_id).first()
#     if not review:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
#     if review.user_id != current_user.id:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your review")

#     db.delete(review)
#     db.commit()
#     return None
