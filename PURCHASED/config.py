from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


db_string = "postgresql://postgres:123@localhost:5432/Purchased"
engine = create_engine(db_string)
session = sessionmaker(bind=engine)
base = declarative_base()

SECRET_KEY = 'thisissecret'