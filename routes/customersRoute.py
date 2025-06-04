from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from models.customersModel import (
    Customer, CustomerCreate, CustomerRead, CustomerUpdate, CustomerRemove 
)
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/customers", response_model=list[CustomerRead])
async def get_customers(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(Customer))
        customers = result.scalars().all()
        return customers
    except Exception as e:
        logger.error(f"Error fetching customers: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/customers", response_model=CustomerRead)
async def create_Customer(Customer: CustomerCreate, db: AsyncSession = Depends(get_db)):
    try:        
        result = await db.execute(
            select(Customer).where(Customer.email == Customer.email)
        )
        existing_Customer = result.scalar_one_or_none()
        if existing_Customer:
            raise HTTPException(status_code=400, detail="Customer already exists.") 
        new_Customer = Customer( 
            first_name = Customer. first_name,
            last_name = Customer. last_name,
            email = Customer.email,
            phone_number =  Customer.phone_number,
            address =  Customer.address,
        )
        db.add(new_Customer)
        await db.commit()
        await db.refresh(new_Customer)
        return new_Customer
    except Exception as e:
        await db.rollback()
        logger.error(f"Error creating Customer: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@router.get("/customers/{Customer_id}", response_model=CustomerRead)
async def get_Customer(Customer_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(Customer).where(Customer.Customer_id == Customer_id))
        Customer = result.scalar_one_or_none()
        if Customer is None:
            raise HTTPException(status_code=404, detail="Customer not found")
        return Customer
    except Exception as e:
        logger.error(f"Error fetching Customer with ID {Customer_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.put("/customers/{Customer_id}", response_model=CustomerRead)
async def update_Customer(Customer_id: int, Customer: CustomerUpdate, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(Customer).where(Customer.Customer_id == Customer_id))
        existing_Customer = result.scalar_one_or_none()
        if existing_Customer is None:
            raise HTTPException(status_code=404, detail="Customer not found")
        
        for key, value in Customer.dict(exclude_unset=True).items():
            setattr(existing_Customer, key, value)
        
        await db.commit()
        await db.refresh(existing_Customer)
        return existing_Customer
    except Exception as e:
        logger.error(f"Error updating Customer with ID {Customer_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@router.delete("/customers/{Customer_id}", response_model=CustomerRemove)
async def delete_Customer(Customer_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(Customer).where(Customer.Customer_id == Customer_id))
        existing_Customer = result.scalar_one_or_none()
        if existing_Customer is None:
            raise HTTPException(status_code=404, detail="Customer not found")
        
        await db.delete(existing_Customer)
        await db.commit()
        return CustomerRemove(Customer_id=Customer_id)
    except Exception as e:
        logger.error(f"Error deleting Customer with ID {Customer_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

