from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from models.productsModel import (
    Product, ProductCreate, ProductRead, ProductUpdate, ProductRemove 
)
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/products", response_model=list[ProductRead])
async def get_products(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(Product))
        products = result.scalars().all()
        return products
    except Exception as e:
        logger.error(f"Error fetching products: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/products", response_model=ProductRead)
async def create_Product(Product: ProductCreate, db: AsyncSession = Depends(get_db)):
    try:        
        result = await db.execute(
            select(Product).where(Product.email == Product.email)
        )
        existing_Product = result.scalar_one_or_none()
        if existing_Product:
            raise HTTPException(status_code=400, detail="Product already exists.") 
        new_Product = Product(
            name = Product.name,
            email = Product.email
        )
        db.add(new_Product)
        await db.commit()
        await db.refresh(new_Product)
        return new_Product
    except Exception as e:
        await db.rollback()
        logger.error(f"Error creating Product: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@router.get("/products/{Product_id}", response_model=ProductRead)
async def get_Product(Product_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(Product).where(Product.Product_id == Product_id))
        Product = result.scalar_one_or_none()
        if Product is None:
            raise HTTPException(status_code=404, detail="Product not found")
        return Product
    except Exception as e:
        logger.error(f"Error fetching Product with ID {Product_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.put("/products/{Product_id}", response_model=ProductRead)
async def update_Product(Product_id: int, Product: ProductUpdate, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(Product).where(Product.Product_id == Product_id))
        existing_Product = result.scalar_one_or_none()
        if existing_Product is None:
            raise HTTPException(status_code=404, detail="Product not found")
        
        for key, value in Product.dict(exclude_unset=True).items():
            setattr(existing_Product, key, value)
        
        await db.commit()
        await db.refresh(existing_Product)
        return existing_Product
    except Exception as e:
        logger.error(f"Error updating Product with ID {Product_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@router.delete("/products/{Product_id}", response_model=ProductRemove)
async def delete_Product(Product_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(Product).where(Product.Product_id == Product_id))
        existing_Product = result.scalar_one_or_none()
        if existing_Product is None:
            raise HTTPException(status_code=404, detail="Product not found")
        
        await db.delete(existing_Product)
        await db.commit()
        return ProductRemove(Product_id=Product_id)
    except Exception as e:
        logger.error(f"Error deleting Product with ID {Product_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

