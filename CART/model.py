from enum import unique
from sqlalchemy import Column, Float, String, Integer, Date, column
from config import base, engine

class Cart(base):  
    __tablename__ = 'cart'

    user_id = Column(String, nullable = False)
    item_name = Column(String, primary_key=True)
    item_quantity=Column(Integer,nullable=False)
    item_price = Column(Integer, nullable = False)

    def __init__(self, user_id, item_name, item_quantity, item_price):
        self.user_id = user_id
        self.item_name = item_name
        self.item_quantity = item_quantity
        self.item_price = item_price
        

base.metadata.create_all(engine)