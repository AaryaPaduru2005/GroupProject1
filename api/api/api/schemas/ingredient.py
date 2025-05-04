from pydantic import BaseModel

class IngredientBase(BaseModel):
    name: str
    quantity_in_stock: float

class IngredientCreate(IngredientBase):
    pass

class IngredientUpdate(IngredientBase):
    pass

class Ingredient(IngredientBase):
    id: int
    class Config:
        orm_mode = True
