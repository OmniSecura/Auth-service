from sqlalchemy import JSON
from sqlmodel import SQLModel, Column, String, Field
from typing import List, Optional

class User(SQLModel, table=True):
    __tablename__ = 'users'
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(String, unique=True, nullable=False)
    name: str = Field(String, nullable=False)
    family_name: str = Field(String, nullable=False)
    password: str = Field(String, nullable=False)
    clue: str = Field(String, nullable=False)
    passphrase: List[str] = Field(sa_column=Column(JSON))

