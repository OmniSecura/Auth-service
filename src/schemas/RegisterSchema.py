from pydantic import BaseModel
from typing import Dict


class RegisterSchema(BaseModel):
    email: str
    name: str
    family_name: str
    password: str
    passphrase: Dict[str, str]
