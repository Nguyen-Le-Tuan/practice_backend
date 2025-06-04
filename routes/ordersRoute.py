from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from database import get_db
from models.ordersModel import (
    Order, OrderCreate, OrderItem
)
from models.productsModel import Product
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/orders/")
async def create_order(order_data: OrderCreate, db: Session = Depends(get_db)):
    # Step 2: Process order items
    total_price = 0
    order_items = List[OrderItem]

    for item in order_data.items:
        stmt = select(Product).where(Product.product_id == item.product_id)
        result = await db.execute(stmt)
        product = result.scalar_one_or_none()

        if not product:
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")
        if product.stock_quantity < item.quantity:
            raise HTTPException(status_code=400, detail=f"Insufficient stock for product {product.product_name}")

        product.stock_quantity -= item.quantity  # Update stock
        item_total = product.price * item.quantity
        total_price += item_total

        order_items.append(OrderItem(
            product_id=product.product_id,
            quantity=item.quantity,
            unit_price=product.price
            
        ))

    # Step 3: Create and save order
    new_order = Order(
        total_amount=total_price,
        status="Pending",
        items=order_items
    )

    db.add(new_order)
    await db.commit()
    await db.refresh(new_order)

    return {
        "order_id": new_order.id,
        "total_amount": new_order.total_amount,
        "status": new_order.status
    }