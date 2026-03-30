import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, doc="Наименование товара")
    category = Column(String, nullable=False, doc="Категория")
    store_name = Column(String, nullable=False, doc="Название супермаркета")
    base_weight = Column(Float, nullable=False, doc="Вес q0")
    
    url = Column(String, nullable=False, doc="URL страницы товара")
    css_selector = Column(String, nullable=False, doc="CSS-селектор")

    prices = relationship("PriceHistory", back_populates="product", cascade="all, delete-orphan")

class PriceHistory(Base):
    __tablename__ = 'price_history'

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    date = Column(DateTime, default=datetime.utcnow, nullable=False)
    current_price = Column(Float, nullable=False)

    product = relationship("Product", back_populates="prices")

def get_engine(db_url: str = "sqlite:///baku_cpi.db"):
    engine = create_engine(db_url, echo=False)
    Base.metadata.create_all(engine)
    return engine

def get_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()