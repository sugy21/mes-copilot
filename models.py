from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
import datetime

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    order_name = Column(String, nullable=False)
    product_code = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    results = relationship("WorkResult", back_populates="order")

class WorkResult(Base):
    __tablename__ = "work_results"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    status = Column(String, nullable=False)
    worker = Column(String, nullable=True)
    inspector = Column(String, nullable=True)  # 추가된 필드
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    order = relationship("Order", back_populates="results")