from enum import unique
from sqlalchemy import Column, String, Integer, Date
from config import base, engine

class Credentials(base):  
    __tablename__ = 'credentials'

    user_id = Column(String, primary_key=True)
    username = Column(String, nullable = False, unique=True)
    password = Column(String, nullable = False)

    def __init__(self, user_id, username, password):
        self.user_id=user_id
        self.username=username
        self.password=password

base.metadata.create_all(engine)