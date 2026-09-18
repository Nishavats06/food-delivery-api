from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.models.cart import Cart, CartItem
from app.models.menu_item import MenuItem
from app.schemas.cart import CartItemAdd, CartItemUpdate, CartOut, CartItemOut
from app.schemas.response import ResponseWrapper
from app.api.deps import get_current_user

router = APIRouter(prefix="/cart", tags=["Cart"])

DELIVERY_FEE = 40.0
TAX_RATE = 0.05


def get_or_create_cart(db: Session, user: User) -> Cart:
    cart = db.query(Cart).filter(Cart.user_id == user.id).first()
    if not cart:
        cart = Cart(user_id=user.id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    return cart


def build_cart_response(cart: Cart) -> CartOut:
    items_out = []
    subtotal = 0.0

    for item in cart.items:
        item_total = item.menu_item.price * item.quantity
        subtotal += item_total
        items_out.append(CartItemOut(
            id=item.id,
            menu_item_id=item.menu_item_id,
            name=item.menu_item.name,
            price=item.menu_item.price,
            quantity=item.quantity,
            item_total=item_total,
        ))

    taxes = round(subtotal * TAX_RATE, 2)
    delivery_fee = DELIVERY_FEE if items_out else 0.0
    total = round(subtotal + delivery_fee + taxes, 2)

    return CartOut(
        id=cart.id,
        items=items_out,
        subtotal=round(subtotal, 2),
        delivery_fee=delivery_fee,
        taxes=taxes,
        total=total,
    )


@router.get("", response_model=ResponseWrapper[CartOut])
def get_cart(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    cart = get_or_create_cart(db, current_user)
    return ResponseWrapper(success=True, message="success", data=build_cart_response(cart))


@router.post("/items", response_model=ResponseWrapper[CartOut], status_code=status.HTTP_201_CREATED)
def add_item_to_cart(
    item_in: CartItemAdd,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    menu_item = db.query(MenuItem).filter(MenuItem.id == item_in.menu_item_id).first()
    if not menu_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not found")
    if not menu_item.is_available:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Menu item is not available")

    cart = get_or_create_cart(db, current_user)

    existing_item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.menu_item_id == item_in.menu_item_id,
    ).first()

    if existing_item:
        existing_item.quantity += item_in.quantity
    else:
        new_item = CartItem(
            cart_id=cart.id,
            menu_item_id=item_in.menu_item_id,
            quantity=item_in.quantity,
        )
        db.add(new_item)

    db.commit()
    db.refresh(cart)
    return ResponseWrapper(success=True, message="Item added to cart", data=build_cart_response(cart))


@router.patch("/items/{item_id}", response_model=ResponseWrapper[CartOut])
def update_cart_item(
    item_id: int,
    item_in: CartItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    cart = get_or_create_cart(db, current_user)
    item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.cart_id == cart.id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")

    item.quantity = item_in.quantity
    db.commit()
    db.refresh(cart)
    return ResponseWrapper(success=True, message="Cart item updated", data=build_cart_response(cart))


@router.delete("/items/{item_id}", response_model=ResponseWrapper[CartOut])
def remove_cart_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    cart = get_or_create_cart(db, current_user)
    item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.cart_id == cart.id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")

    db.delete(item)
    db.commit()
    db.refresh(cart)
    return ResponseWrapper(success=True, message="Item removed from cart", data=build_cart_response(cart))


@router.delete("", response_model=ResponseWrapper[None])
def clear_cart(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    cart = get_or_create_cart(db, current_user)
    for item in cart.items:
        db.delete(item)
    db.commit()
    return ResponseWrapper(success=True, message="Cart cleared successfully", data=None)






# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session

# from app.db.session import get_db
# from app.models.user import User
# from app.models.cart import Cart, CartItem
# from app.models.menu_item import MenuItem
# from app.schemas.cart import CartItemAdd, CartItemUpdate, CartOut, CartItemOut
# from app.api.deps import get_current_user

# router = APIRouter(prefix="/cart", tags=["Cart"])

# DELIVERY_FEE = 40.0
# TAX_RATE = 0.05


# def get_or_create_cart(db: Session, user: User) -> Cart:
#     cart = db.query(Cart).filter(Cart.user_id == user.id).first()
#     if not cart:
#         cart = Cart(user_id=user.id)
#         db.add(cart)
#         db.commit()
#         db.refresh(cart)
#     return cart


# def build_cart_response(cart: Cart) -> CartOut:
#     items_out = []
#     subtotal = 0.0

#     for item in cart.items:
#         item_total = item.menu_item.price * item.quantity
#         subtotal += item_total
#         items_out.append(CartItemOut(
#             id=item.id,
#             menu_item_id=item.menu_item_id,
#             name=item.menu_item.name,
#             price=item.menu_item.price,
#             quantity=item.quantity,
#             item_total=item_total,
#         ))

#     taxes = round(subtotal * TAX_RATE, 2)
#     delivery_fee = DELIVERY_FEE if items_out else 0.0
#     total = round(subtotal + delivery_fee + taxes, 2)

#     return CartOut(
#         id=cart.id,
#         items=items_out,
#         subtotal=round(subtotal, 2),
#         delivery_fee=delivery_fee,
#         taxes=taxes,
#         total=total,
#     )


# @router.get("", response_model=CartOut)
# def get_cart(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
#     cart = get_or_create_cart(db, current_user)
#     return build_cart_response(cart)


# @router.post("/items", response_model=CartOut, status_code=status.HTTP_201_CREATED)
# def add_item_to_cart(
#     item_in: CartItemAdd,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user),
# ):
#     menu_item = db.query(MenuItem).filter(MenuItem.id == item_in.menu_item_id).first()
#     if not menu_item:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not found")
#     if not menu_item.is_available:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Menu item is not available")

#     cart = get_or_create_cart(db, current_user)

#     existing_item = db.query(CartItem).filter(
#         CartItem.cart_id == cart.id,
#         CartItem.menu_item_id == item_in.menu_item_id,
#     ).first()

#     if existing_item:
#         existing_item.quantity += item_in.quantity
#     else:
#         new_item = CartItem(
#             cart_id=cart.id,
#             menu_item_id=item_in.menu_item_id,
#             quantity=item_in.quantity,
#         )
#         db.add(new_item)

#     db.commit()
#     db.refresh(cart)
#     return build_cart_response(cart)


# @router.patch("/items/{item_id}", response_model=CartOut)
# def update_cart_item(
#     item_id: int,
#     item_in: CartItemUpdate,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user),
# ):
#     cart = get_or_create_cart(db, current_user)
#     item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.cart_id == cart.id).first()
#     if not item:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")

#     item.quantity = item_in.quantity
#     db.commit()
#     db.refresh(cart)
#     return build_cart_response(cart)


# @router.delete("/items/{item_id}", response_model=CartOut)
# def remove_cart_item(
#     item_id: int,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user),
# ):
#     cart = get_or_create_cart(db, current_user)
#     item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.cart_id == cart.id).first()
#     if not item:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")

#     db.delete(item)
#     db.commit()
#     db.refresh(cart)
#     return build_cart_response(cart)


# @router.delete("", status_code=status.HTTP_204_NO_CONTENT)
# def clear_cart(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
#     cart = get_or_create_cart(db, current_user)
#     for item in cart.items:
#         db.delete(item)
#     db.commit()
#     return None