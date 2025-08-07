from pydantic import BaseModel
from typing import List, Optional


class LoginSchema(BaseModel):
    email: str
    password: str
    passphrase: Optional[List[str]] = None
