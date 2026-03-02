from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
import models
import schemas
from database import SessionLocal, engine

# Создание таблиц в БД
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="ПК мастер - Интернет-магазин")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Эндпоинт 1: Получение списка товаров
@app.get("/products", response_model=List[schemas.Product])
def get_products(skip: int = 0, limit: int = 100, category_id: int = None, db: Session = Depends(get_db)):
    query = db.query(models.Product)
    if category_id:
        query = query.filter(models.Product.category_id == category_id)
    products = query.offset(skip).limit(limit).all()
    return products

# Эндпоинт 2: Получение информации о конкретном товаре
@app.get("/products/{product_id}", response_model=schemas.ProductDetail)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return product

# Эндпоинт 3: Добавление товара в корзину
@app.post("/cart/add", response_model=schemas.CartItem)
def add_to_cart(cart_item: schemas.CartItemCreate, db: Session = Depends(get_db)):
    # Упрощенная версия для первого спринта
    return {
        "id": 1,
        "product_id": cart_item.product_id,
        "product_name": "Тестовый товар",
        "quantity": cart_item.quantity,
        "price": 1000
    }

# Эндпоинт 4: Создание заказа
@app.post("/orders")
def create_order(order_data: schemas.OrderCreate, db: Session = Depends(get_db)):
    return {"message": "Заказ создан", "data": order_data}

# Эндпоинт 5: Получение заказов пользователя
@app.get("/orders/my", response_model=List[schemas.OrderCreate])
def get_my_orders(db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    return []
