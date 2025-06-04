from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from pydantic import BaseModel

Base = declarative_base()

class Customer(Base):
    __tablename__ = 'Customers'
    customer_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone_number = Column(String, nullable=True)
    address = Column(Text, nullable=True)

class CustomerCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str | None = None
    address: str | None = None

class CustomerUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    phone_number: str | None = None
    address: str | None = None

class CustomerRead(BaseModel):
    customer_id: int
    first_name: str
    last_name: str
    email: str
    phone_number: str | None = None
    address: str | None = None

    class Config:
        orm_mode = True

class CustomerRemove(BaseModel):
    customer_id: int