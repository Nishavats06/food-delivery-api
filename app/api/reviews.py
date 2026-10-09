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
from app.core.common_responses import UNAUTHORIZED_RESPONSE, FORBIDDEN_RESPONSE, NOT_FOUND_RESPONSE
from app.models.order import Order, OrderStatus

def recalculate_rating(db: Session, restaurant_id: int):
    reviews = db.query(Review).filter(Review.restaurant_id == restaurant_id).all()
    if reviews:
        avg_rating = sum(r.rating for r in reviews) / len(reviews)
        restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
        restaurant.rating = round(avg_rating, 1)
        db.commit()

router = APIRouter(tags=["Reviews"])


@router.post(
    "/restaurants/{restaurant_id}/reviews",
    response_model=ResponseWrapper[ReviewOut],
    status_code=status.HTTP_201_CREATED,
    responses={**UNAUTHORIZED_RESPONSE, **NOT_FOUND_RESPONSE},
)
def create_review(
    restaurant_id: int,
    review_in: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")

    has_delivered_order = db.query(Order).filter(
        Order.user_id == current_user.id,
        Order.restaurant_id == restaurant_id,
        Order.status == OrderStatus.DELIVERED,
    ).first()
    if not has_delivered_order:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You can only review restaurants you have ordered from",
        )

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
    recalculate_rating(db, restaurant_id)
    return ResponseWrapper(success=True, message="Review submitted successfully", data=new_review)


@router.get(
    "/restaurants/{restaurant_id}/reviews",
    response_model=ResponseWrapper[List[ReviewOut]],
    responses=NOT_FOUND_RESPONSE,
)
def list_reviews(restaurant_id: int, db: Session = Depends(get_db)):
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")

    reviews = db.query(Review).filter(Review.restaurant_id == restaurant_id).all()
    return ResponseWrapper(success=True, message="success", data=reviews)


@router.patch(
    "/reviews/{review_id}",
    response_model=ResponseWrapper[ReviewOut],
    responses={**UNAUTHORIZED_RESPONSE, **FORBIDDEN_RESPONSE, **NOT_FOUND_RESPONSE},
)
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
    recalculate_rating(db, review.restaurant_id)
    return ResponseWrapper(success=True, message="Review updated successfully", data=review)


@router.delete(
    "/reviews/{review_id}",
    response_model=ResponseWrapper[None],
    responses={**UNAUTHORIZED_RESPONSE, **FORBIDDEN_RESPONSE, **NOT_FOUND_RESPONSE},
)
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
    recalculate_rating(db, review.restaurant_id)
    return ResponseWrapper(success=True, message="Review deleted successfully", data=None)



