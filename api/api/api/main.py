from fastapi import FastAPI
from api.routers import menu, ingredients, promotions, reviews, orders

app = FastAPI(title="OROS API")

app.include_router(menu.router)
app.include_router(ingredients.router)
app.include_router(promotions.router)
app.include_router(reviews.router)
app.include_router(orders.router)
