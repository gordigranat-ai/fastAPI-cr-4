from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class Product(Base):
    """
    Модель продукта в базе данных
    """
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), index=True, nullable=False)
    price = Column(Float, nullable=False)
    count = Column(Integer, nullable=False)
    description = Column(String(500), nullable=False, default="")

    def __repr__(self):
        return f"<Product(id={self.id}, title='{self.title}', price={self.price})>"