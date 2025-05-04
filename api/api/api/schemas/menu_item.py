from pydantic import BaseModel
from typing import List

class IngredientQuantity(BaseModel):
    ingredient_id: int
    quantity_required: float

class MenuItemBase(BaseModel):
    name: str
    description: str | None = None
    price: float
    category: str | None = None

class MenuItemCreate(MenuItemBase):
    ingredients: List[IngredientQuantity]

class MenuItemUpdate(MenuItemBase):
    pass

class MenuItem(MenuItemBase):
    id: int
    ingredients: List[IngredientQuantity]
    class Config:
        orm_mode = True
