from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from api.models.order import Order
from api.models.order_item import OrderItem
from api.models.menu_item import MenuItem
from api.models.menu_item_ingredient import MenuItemIngredient
from api.models.ingredient import Ingredient
from api.models.promotion import Promotion
from api.schemas.order import OrderCreate
from sqlalchemy import func
from datetime import date, datetime

def create_order(db: Session, data: OrderCreate):
    # Promo validation
    discount = 0.0
    if data.promo_code:
        promo = db.query(Promotion).filter(Promotion.code == data.promo_code).first()
        if not promo or promo.expires_at < datetime.utcnow():
            raise HTTPException(status_code=400, detail="Invalid or expired promo code")
        discount = promo.discount

    total = 0.0
    # Check inventory
    for item in data.items:
        menu_item = db.query(MenuItem).filter(MenuItem.id == item.menu_item_id).first()
        if not menu_item:
            raise HTTPException(status_code=404, detail=f"Menu item {item.menu_item_id} not found")
        recipe = db.query(MenuItemIngredient).filter(MenuItemIngredient.menu_item_id == item.menu_item_id).all()
        for ri in recipe:
            ing = db.query(Ingredient).filter(Ingredient.id == ri.ingredient_id).first()
            req = ri.quantity_required * item.quantity
            if ing.quantity_in_stock < req:
                raise HTTPException(status_code=400, detail=f"Insufficient {ing.name}")
        total += menu_item.price * item.quantity

    # Deduct inventory
    for item in data.items:
        recipe = db.query(MenuItemIngredient).filter(MenuItemIngredient.menu_item_id == item.menu_item_id).all()
        for ri in recipe:
            ing = db.query(Ingredient).filter(Ingredient.id == ri.ingredient_id).first()
            ing.quantity_in_stock -= ri.quantity_required * item.quantity
            db.add(ing)
    db.commit()

    total *= (1 - discount)

    # Create order
    order = Order(
        customer_name=data.customer_name,
        phone=data.phone,
        address=data.address,
        order_type=data.order_type or "takeout",
        status="placed",
        total=total,
        created_at=datetime.utcnow()
    )
    db.add(order)
    db.commit()
    db.refresh(order)

    # Order items
    for item in data.items:
        oi = OrderItem(order_id=order.id, menu_item_id=item.menu_item_id, quantity=item.quantity)
        db.add(oi)
    db.commit()
    return order

def get_orders(db: Session, start_date: date = None, end_date: date = None):
    q = db.query(Order)
    if start_date:
        q = q.filter(func.date(Order.created_at) >= start_date)
    if end_date:
        q = q.filter(func.date(Order.created_at) <= end_date)
    return q.all()

def get_order(db: Session, order_id: int):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

def get_revenue(db: Session, target_date: date):
    total = db.query(func.sum(Order.total)).filter(func.date(Order.created_at) == target_date).scalar() or 0.0
    return {"date": target_date, "total_revenue": total}
