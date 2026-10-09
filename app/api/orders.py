

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
from app.schemas.response import ResponseWrapper
from app.api.deps import get_current_user
from app.core.common_responses import UNAUTHORIZED_RESPONSE, FORBIDDEN_RESPONSE, NOT_FOUND_RESPONSE
from app.api.cart import get_item_price

VALID_STATUS_TRANSITIONS = {
    OrderStatus.PLACED: [OrderStatus.CONFIRMED, OrderStatus.CANCELLED],
    OrderStatus.CONFIRMED: [OrderStatus.PREPARING, OrderStatus.CANCELLED],
    OrderStatus.PREPARING: [OrderStatus.OUT_FOR_DELIVERY],
    OrderStatus.OUT_FOR_DELIVERY: [OrderStatus.DELIVERED],
    OrderStatus.DELIVERED: [],
    OrderStatus.CANCELLED: [],
}

router = APIRouter(prefix="/orders", tags=["Orders"])

DELIVERY_FEE = 40.0
TAX_RATE = 0.05


@router.post(
    "",
    response_model=ResponseWrapper[OrderOut],
    status_code=status.HTTP_201_CREATED,
    responses={**UNAUTHORIZED_RESPONSE, **NOT_FOUND_RESPONSE},
)
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

    subtotal = sum(get_item_price(item.menu_item, item.portion_name) * item.quantity for item in cart.items)
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
            price=get_item_price(item.menu_item, item.portion_name),
            portion_name=item.portion_name,
            quantity=item.quantity,
        )
        db.add(order_item)

    for item in cart.items:
        db.delete(item)

    db.commit()
    db.refresh(new_order)
    return ResponseWrapper(success=True, message="Order placed successfully", data=new_order)


@router.get("", response_model=ResponseWrapper[List[OrderOut]], responses=UNAUTHORIZED_RESPONSE)
def list_orders(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role == UserRole.RESTAURANT_OWNER:
        restaurant_ids = [r.id for r in db.query(Restaurant).filter(Restaurant.owner_id == current_user.id).all()]
        orders = db.query(Order).filter(Order.restaurant_id.in_(restaurant_ids)).all()
    else:
        orders = db.query(Order).filter(Order.user_id == current_user.id).all()
    return ResponseWrapper(success=True, message="success", data=orders)

@router.get(
    "/restaurant/{restaurant_id}",
    response_model=ResponseWrapper[List[OrderOut]],
    responses={**UNAUTHORIZED_RESPONSE, **FORBIDDEN_RESPONSE, **NOT_FOUND_RESPONSE},
)
def list_restaurant_orders(
    restaurant_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")
    if current_user.role != UserRole.RESTAURANT_OWNER or restaurant.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your restaurant")

    orders = db.query(Order).filter(Order.restaurant_id == restaurant_id).all()
    return ResponseWrapper(success=True, message="success", data=orders)

@router.get(
    "/{order_id}",
    response_model=ResponseWrapper[OrderOut],
    responses={**UNAUTHORIZED_RESPONSE, **FORBIDDEN_RESPONSE, **NOT_FOUND_RESPONSE},
)
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

    return ResponseWrapper(success=True, message="success", data=order)


@router.patch(
    "/{order_id}/status",
    response_model=ResponseWrapper[OrderOut],
    responses={**UNAUTHORIZED_RESPONSE, **FORBIDDEN_RESPONSE, **NOT_FOUND_RESPONSE},
)
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

    allowed_next = VALID_STATUS_TRANSITIONS.get(order.status, [])
    if status_in.status not in allowed_next:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot change status from {order.status.value} to {status_in.status.value}. Allowed: {[s.value for s in allowed_next]}",
        )

    order.status = status_in.status
    db.commit()
    db.refresh(order)
    return ResponseWrapper(success=True, message="Order status updated", data=order)

# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session
# from typing import List

# from app.db.session import get_db
# from app.models.user import User, UserRole
# from app.models.cart import Cart, CartItem
# from app.models.address import Address
# from app.models.order import Order, OrderItem, OrderStatus
# from app.models.restaurant import Restaurant
# from app.schemas.order import OrderCreate, OrderOut, OrderStatusUpdate
# from app.api.deps import get_current_user

# router = APIRouter(prefix="/orders", tags=["Orders"])

# DELIVERY_FEE = 40.0
# TAX_RATE = 0.05


# @router.post("", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
# def create_order(
#     order_in: OrderCreate,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user),
# ):
#     cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
#     if not cart or not cart.items:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cart is empty")

#     address = db.query(Address).filter(
#         Address.id == order_in.address_id, Address.user_id == current_user.id
#     ).first()
#     if not address:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Address not found")

#     restaurant_id = cart.items[0].menu_item.restaurant_id
#     for item in cart.items:
#         if item.menu_item.restaurant_id != restaurant_id:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail="Cart contains items from multiple restaurants",
#             )

#     subtotal = sum(item.menu_item.price * item.quantity for item in cart.items)
#     taxes = round(subtotal * TAX_RATE, 2)
#     total = round(subtotal + DELIVERY_FEE + taxes, 2)

#     new_order = Order(
#         user_id=current_user.id,
#         restaurant_id=restaurant_id,
#         delivery_address=address.location,
#         status=OrderStatus.PLACED,
#         subtotal=round(subtotal, 2),
#         delivery_fee=DELIVERY_FEE,
#         taxes=taxes,
#         total=total,
#     )
#     db.add(new_order)
#     db.commit()
#     db.refresh(new_order)

#     for item in cart.items:
#         order_item = OrderItem(
#             order_id=new_order.id,
#             menu_item_id=item.menu_item_id,
#             name=item.menu_item.name,
#             price=item.menu_item.price,
#             quantity=item.quantity,
#         )
#         db.add(order_item)

#     for item in cart.items:
#         db.delete(item)

#     db.commit()
#     db.refresh(new_order)
#     return new_order


# @router.get("", response_model=List[OrderOut])
# def list_orders(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
#     if current_user.role == UserRole.RESTAURANT_OWNER:
#         restaurant_ids = [r.id for r in db.query(Restaurant).filter(Restaurant.owner_id == current_user.id).all()]
#         return db.query(Order).filter(Order.restaurant_id.in_(restaurant_ids)).all()
#     return db.query(Order).filter(Order.user_id == current_user.id).all()


# @router.get("/{order_id}", response_model=OrderOut)
# def get_order(order_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
#     order = db.query(Order).filter(Order.id == order_id).first()
#     if not order:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

#     is_customer_owner = order.user_id == current_user.id
#     is_restaurant_owner = (
#         current_user.role == UserRole.RESTAURANT_OWNER
#         and order.restaurant.owner_id == current_user.id
#     )
#     if not is_customer_owner and not is_restaurant_owner:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this order")

#     return order


# @router.patch("/{order_id}/status", response_model=OrderOut)
# def update_order_status(
#     order_id: int,
#     status_in: OrderStatusUpdate,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user),
# ):
#     order = db.query(Order).filter(Order.id == order_id).first()
#     if not order:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

#     if current_user.role != UserRole.RESTAURANT_OWNER or order.restaurant.owner_id != current_user.id:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this order")

#     order.status = status_in.status
#     db.commit()
#     db.refresh(order)
#     return order