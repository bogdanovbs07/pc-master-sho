from fastapi.testclient import TestClient
from main import app
import pytest

client = TestClient(app)

def test_get_products():
    """Тест получения списка товаров"""
    response = client.get("/products")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_product_not_found():
    """Тест получения несуществующего товара"""
    response = client.get("/products/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Товар не найден"

def test_create_order():
    """Тест создания заказа"""
    order_data = {
        "shipping_address": "Москва, ул. Тестовая, д. 1",
        "phone_number": "+79991234567"
    }
    response = client.post("/orders", json=order_data)
    assert response.status_code == 200
    assert response.json()["message"] == "Заказ создан"
