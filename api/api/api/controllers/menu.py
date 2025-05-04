from sqlalchemy.orm import Session
from fastapi import HTTPException
from api.models.menu_item import MenuItem
from api.models.menu_item_ingredient import MenuItemIngredient
from api.schemas.menu_item import MenuItemCreate, MenuItemUpdate

def get_menu_items(db: Session):
    return db.query(MenuItem).all()

def get_menu_item(db: Session, item_id: int):
    item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return item

def create_menu_item(db: Session, item: MenuItemCreate):
    db_item = MenuItem(
        name=item.name,
        description=item.description,
        price=item.price,
        category=item.category
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    # ingredients
    for iq in item.ingredients:
        mm = MenuItemIngredient(
            menu_item_id=db_item.id,
            ingredient_id=iq.ingredient_id,
            quantity_required=iq.quantity_required
        )
        db.add(mm)
    db.commit()
    return db_item

def update_menu_item(db: Session, item_id: int, data: MenuItemUpdate):
    item = get_menu_item(db, item_id)
    for field, value in data.dict(exclude_unset=True).items():
        setattr(item, field, value)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

def delete_menu_item(db: Session, item_id: int):
    item = get_menu_item(db, item_id)
    db.delete(item)
    db.commit()
