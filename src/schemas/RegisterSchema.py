from pydantic import BaseModel
from typing import List
from sqlmodel import Field

class RegisterSchema(BaseModel):
    email: str
    name: str
    family_name: str
    password: str
    clue: str
    passphrase: List[str] = Field(..., max_items=4)
