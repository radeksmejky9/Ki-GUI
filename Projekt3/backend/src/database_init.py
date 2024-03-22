from database import engine
from sqlmodel import SQLModel
from models import Test


def initialize_database():
    SQLModel.metadata.create_all(engine)
