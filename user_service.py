from config import session, engine, base
from model import Credentials

base.metadata.create_all(engine)
session=session()