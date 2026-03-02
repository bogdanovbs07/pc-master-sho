from pydantic import BaseModel, Field, validator, EmailStr
from typing import Optional, List
from datetime import datetime

# Product схемы
class ProductBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    price: float = Field(..., gt=0, description="Цена должна быть больше 0")
    stock_quantity: int = Field(0, ge=0, description="Количество не может быть отрицательным")
    category_id: Optional[int] = None
    image_url: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True

class ProductDetail(Product):
    category_name: Optional[str] = None

# User схемы
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: Optional[str] = Field(None, max_length=100)

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)
    
    @validator('password')
    def validate_password(cls, v):
        if not any(char.isdigit() for char in v):
            raise ValueError('Пароль должен содержать хотя бы одну цифру')
        return v

class User(UserBase):
    id: int
    is_active: bool
    role: str
    created_at: datetime
    
    class Config:
        orm_mode = True

# Cart схемы
class CartItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(1, ge=1)

class CartItem(BaseModel):
    id: int
    product_id: int
    product_name: str
    quantity: int
    price: float
    
    class Config:
        orm_mode = True

# Order схемы
class OrderCreate(BaseModel):
    shipping_address: str = Field(..., min_length=10)
    phone_number: str = Field(..., regex=r'^\+?[0-9]{10,15}$')
    
    @validator('shipping_address')
    def validate_address(cls, v):
        if len(v.split()) < 3:
            raise ValueError('Укажите полный адрес (город, улица, дом)')
        return v
