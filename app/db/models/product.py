from sqlalchemy import Column, Integer, String, Float, Date, DateTime, func, Index
from sqlalchemy.orm import relationship
from app.db.session import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String(255), nullable=False)
    sale_price = Column(Float, nullable=False)
    barcode = Column(String(50), unique=True, nullable=False)
    section = Column(String(50), nullable=False)
    initial_stock = Column(Integer, default=0)
    current_stock = Column(Integer, default=0)
    expiration_date = Column(Date, nullable=True)
    image_url = Column(String(255), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    order_items = relationship("OrderItem", back_populates="product")

    __table_args__ = (
        Index("ix_products_section", "section"),
        Index("ix_products_barcode", "barcode", unique=True),
    )
