from pydantic import BaseModel
from typing import List, Optional
from sqlmodel import Field

class RegisterSchema(BaseModel):
    email: str
    name: str
    family_name: str
    password: str
    passphrase: Optional[List[str]] = Field(default=None, max_items=4)

class RegisterSchemaForUser(BaseModel):
    email: str
    name: str
    family_name: str
