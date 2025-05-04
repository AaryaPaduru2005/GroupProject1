from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from api.dependencies.database import Base

class Ingredient(Base):
    __tablename__ = "ingredients"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    quantity_in_stock = Column(Float, nullable=False)
    recipe = relationship("MenuItemIngredient", back_populates="ingredient")
