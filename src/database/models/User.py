from sqlalchemy import Integer
from sqlmodel import SQLModel, Column, String,Integer
from typing import Dict

class User(SQLModel, table=True):
    __tablename__ = 'users'
    id: int = Column(Integer, primary_key=True)
    email: str = Column(String, unique=True, nullable=False)
    name: str = Column(String, nullable=False)
    password: str = Column(String, nullable=False)
    passphrase: Dict[str, str] = Column(String)
