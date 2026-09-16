from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.models.user import User, UserRole
from app.models.cart import Cart, CartItem
from app.models.address import Address
from app.models.order import Order, OrderItem, OrderStatus
from app.models.restaurant import Restaurant
from app.schemas.order import OrderCreate, OrderOut, OrderStatusUpdate
from app.api.deps import get_current_user

router = APIRouter(prefix="/orders", tags=["Orders"])

DELIVERY_FEE = 40.0
TAX_RATE = 0.05


@router.post("", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
def create_order(
    order_in: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart or not cart.items:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cart is empty")

    address = db.query(Address).filter(
        Address.id == order_in.address_id, Address.user_id == current_user.id
    ).first()
    if not address:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Address not found")

    restaurant_id = cart.items[0].menu_item.restaurant_id
    for item in cart.items:
        if item.menu_item.restaurant_id != restaurant_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cart contains items from multiple restaurants",
            )

    subtotal = sum(item.menu_item.price * item.quantity for item in cart.items)
    taxes = round(subtotal * TAX_RATE, 2)
    total = round(subtotal + DELIVERY_FEE + taxes, 2)

    new_order = Order(
        user_id=current_user.id,
        restaurant_id=restaurant_id,
        delivery_address=address.location,
        status=OrderStatus.PLACED,
        subtotal=round(subtotal, 2),
        delivery_fee=DELIVERY_FEE,
        taxes=taxes,
        total=total,
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    for item in cart.items:
        order_item = OrderItem(
            order_id=new_order.id,
            menu_item_id=item.menu_item_id,
            name=item.menu_item.name,
            price=item.menu_item.price,
            quantity=item.quantity,
        )
        db.add(order_item)

    for item in cart.items:
        db.delete(item)

    db.commit()
    db.refresh(new_order)
    return new_order


@router.get("", response_model=List[OrderOut])
def list_orders(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role == UserRole.RESTAURANT_OWNER:
        restaurant_ids = [r.id for r in db.query(Restaurant).filter(Restaurant.owner_id == current_user.id).all()]
        return db.query(Order).filter(Order.restaurant_id.in_(restaurant_ids)).all()
    return db.query(Order).filter(Order.user_id == current_user.id).all()


@router.get("/{order_id}", response_model=OrderOut)
def get_order(order_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    is_customer_owner = order.user_id == current_user.id
    is_restaurant_owner = (
        current_user.role == UserRole.RESTAURANT_OWNER
        and order.restaurant.owner_id == current_user.id
    )
    if not is_customer_owner and not is_restaurant_owner:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this order")

    return order


@router.patch("/{order_id}/status", response_model=OrderOut)
def update_order_status(
    order_id: int,
    status_in: OrderStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    if current_user.role != UserRole.RESTAURANT_OWNER or order.restaurant.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this order")

    order.status = status_in.status
    db.commit()
    db.refresh(order)
    return order