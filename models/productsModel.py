from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from pydantic import BaseModel

Base = declarative_base()

class Product(Base):
    __tablename__ = 'Products'
    product_id = Column(Integer, primary_key=True, autoincrement=True)
    product_name = Column(String, nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    stock_quantity = Column(Integer, nullable=False)
    supplier_id = Column(Integer, ForeignKey('Suppliers.supplier_id'))

class ProductCreate(BaseModel):
    product_name: str
    description: str | None = None
    price: float
    stock_quantity: int
    supplier_id: int

class ProductUpdate(BaseModel):
    product_name: str | None = None
    description: str | None = None
    price: float | None = None
    stock_quantity: int | None = None
    supplier_id: int | None = None

class ProductRead(BaseModel):
    product_id: int
    product_name: str
    description: str | None = None
    price: float
    stock_quantity: int
    supplier_id: int

    class Config:
        orm_mode = True

class ProductRemove(BaseModel):
    product_id: int