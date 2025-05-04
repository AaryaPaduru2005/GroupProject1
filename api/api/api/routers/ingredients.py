from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from api.dependencies.database import get_db
from api.schemas.ingredient import Ingredient, IngredientCreate, IngredientUpdate
from api.controllers.ingredient import get_ingredients, get_ingredient, create_ingredient, update_ingredient, delete_ingredient

router = APIRouter(prefix="/ingredients", tags=["ingredients"])

@router.get("/", response_model=List[Ingredient])
def read_ingredients(db: Session = Depends(get_db)):
    return get_ingredients(db)

@router.get("/{ing_id}", response_model=Ingredient)
def read_ingredient(ing_id: int, db: Session = Depends(get_db)):
    return get_ingredient(db, ing_id)

@router.post("/", response_model=Ingredient, status_code=201)
def add_ingredient(data: IngredientCreate, db: Session = Depends(get_db)):
    return create_ingredient(db, data)

@router.put("/{ing_id}", response_model=Ingredient)
def edit_ingredient(ing_id: int, data: IngredientUpdate, db: Session = Depends(get_db)):
    return update_ingredient(db, ing_id, data)

@router.delete("/{ing_id}", status_code=204)
def remove_ingredient(ing_id: int, db: Session = Depends(get_db)):
    delete_ingredient(db, ing_id)
