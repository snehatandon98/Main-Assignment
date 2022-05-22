from enum import unique
from sqlalchemy import Column, String, Integer, Date
from config import base, engine

class Purchased(base):  
    __tablename__ = 'purchased'

    invoice_id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False)
    prod_name = Column(String, nullable = False, unique=True)
    prod_quantity=Column(String,nullable=False)
    total_amount_paid = Column(Integer, nullable=False)

    def __init__(self, user_id, invoice_id, prod_name, prod_quantity, total_amount_paid):
        self.invoice_id = invoice_id
        self.user_id = user_id
        self.prod_name = prod_name
        self.prod_quantity = prod_quantity
        self.total_amount_paid = total_amount_paid

base.metadata.create_all(engine)