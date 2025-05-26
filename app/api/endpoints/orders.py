from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from app.schemas.order import OrderCreate, OrderOut, OrderUpdate
from app.db.models.order import Order, OrderItem, OrderStatus
from app.db.models.client import Client
from app.db.models.product import Product
from app.db.models.user import User
from app.core.security import get_current_active_user, get_current_active_admin_user
from app.db.session import get_db

router = APIRouter(prefix="/orders", tags=["orders"])

@router.get("", response_model=List[OrderOut])
def list_orders(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 10,
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    section: Optional[str] = Query(None),
    order_id: Optional[int] = Query(None),
    status: Optional[OrderStatus] = Query(None),
    client_id: Optional[int] = Query(None),
):
    query = db.query(Order).join(Client).join(User)
    if start_date:
        query = query.filter(Order.created_at >= start_date)
    if end_date:
        query = query.filter(Order.created_at <= end_date)
    if section:
        query = query.join(OrderItem).join(Product).filter(Product.section.ilike(f"%{section}%"))
    if order_id:
        query = query.filter(Order.id == order_id)
    if status:
        query = query.filter(Order.status == status)
    if client_id:
        query = query.filter(Order.client_id == client_id)
    orders = query.offset(skip).limit(limit).all()
    return orders

@router.post("", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
def create_order(
    order_in: OrderCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user),
):
  
    client = db.query(Client).filter(Client.id == order_in.client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    order = Order(client_id=order_in.client_id, user_id=current_user.id, status=OrderStatus.PENDING)
    db.add(order)
    db.flush()

    total_price = 0.0
    for item in order_in.items:
        product = db.query(Product).filter(Product.id == item.product_id).with_for_update().first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Produto {item.product_id} não encontrado")
        if product.current_stock < item.quantity:
            raise HTTPException(status_code=400, detail=f"Estoque insuficiente para produto {product.id}")

        product.current_stock -= item.quantity
        unit_price = product.sale_price
        total_price += unit_price * item.quantity

        order_item = OrderItem(order_id=order.id, product_id=product.id, quantity=item.quantity, unit_price=unit_price)
        db.add(order_item)

    order.total_price = total_price
    db.commit()
    db.refresh(order)
    return order

@router.get("/{order_id}", response_model=OrderOut)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user),
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return order

@router.put("/{order_id}", response_model=OrderOut)
def update_order(
    order_id: int,
    order_in: OrderUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user),
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    if order_in.status:
        order.status = order_in.status
    db.commit()
    db.refresh(order)
    return order

@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_admin_user),
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    for item in order.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        product.current_stock += item.quantity
    db.delete(order)
    db.commit()
    return
