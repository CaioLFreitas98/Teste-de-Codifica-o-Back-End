from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.schemas.product import ProductCreate, ProductOut, ProductUpdate
from app.db.models.product import Product
from app.core.security import get_current_active_user, get_current_active_admin_user
from app.db.session import get_db

router = APIRouter(prefix="/products", tags=["products"])

@router.get("", response_model=List[ProductOut])
def list_products(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 10,
    category: Optional[str] = Query(None),  # category = section
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    available: Optional[bool] = Query(None),
):
    query = db.query(Product)
    if category:
        query = query.filter(Product.section.ilike(f"%{category}%"))
    if min_price is not None:
        query = query.filter(Product.sale_price >= min_price)
    if max_price is not None:
        query = query.filter(Product.sale_price <= max_price)
    if available is not None:
        if available:
            query = query.filter(Product.current_stock > 0)
        else:
            query = query.filter(Product.current_stock == 0)
    products = query.offset(skip).limit(limit).all()
    return products

@router.post("", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def create_product(
    product_in: ProductCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_admin_user),
):

    if db.query(Product).filter(Product.barcode == product_in.barcode).first():
        raise HTTPException(status_code=400, detail="Código de barras já existe")
    product = Product(
        description=product_in.description,
        sale_price=product_in.sale_price,
        barcode=product_in.barcode,
        section=product_in.section,
        initial_stock=product_in.initial_stock,
        current_stock=product_in.initial_stock,
        expiration_date=product_in.expiration_date,
        image_url=product_in.image_url,
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

@router.get("/{product_id}", response_model=ProductOut)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user),
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return product

@router.put("/{product_id}", response_model=ProductOut)
def update_product(
    product_id: int,
    product_in: ProductUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_admin_user),
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    for field, value in product_in.dict(exclude_unset=True).items():
        if field == "initial_stock":

            diff = value - product.initial_stock
            product.current_stock += diff
            product.initial_stock = value
        else:
            setattr(product, field, value)
    db.commit()
    db.refresh(product)
    return product

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_admin_user),
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    db.delete(product)
    db.commit()
    return
