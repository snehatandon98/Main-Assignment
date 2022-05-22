from enum import unique
from sqlalchemy import Column, Float, String, Integer, Date, column
from config import base, engine

class Products(base):  
    __tablename__ = 'products'

    prod_id = Column(String, primary_key=True)
    prod_name = Column(String, nullable = False, unique=True)
    prod_quantity=Column(Integer,nullable=False)
    prod_price = Column(Integer, nullable = False)
    prod_category = Column(String, nullable=False)
    prod_rating = Column(Float,nullable=True)

    def __init__(self, prod_id, prod_name, prod_quantity, prod_price, prod_category, prod_rating):
        self.prod_id = prod_id
        self.prod_name = prod_name
        self.prod_quantity = prod_quantity
        self.prod_price = prod_price
        self.prod_category = prod_category
        self.prod_rating = prod_rating

base.metadata.create_all(engine)