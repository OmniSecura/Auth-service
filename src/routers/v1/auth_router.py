from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv
from src.schemas.RegisterSchema import RegisterSchema
from src.security.secure import hash_password
from typing import Optional
from src.database.db_connection import AUTH_SESSION

auth_router = APIRouter(prefix="/auth", tags=["Auth"])

@cbv(auth_router)
class AuthorizationRouter:

    session = AUTH_SESSION

    @auth_router.post("/login")
    async def login(self, username: str, password: str):
        return {"message": f"Logged in as {username}"}

    @auth_router.post("/register", response_model=RegisterSchema)
    async def register(self, email: str, name: str,
                       family_name: str, password: str,
                       clue: Optional[str] = None, passphrase: Optional[str] = None):
        hashed_password = hash_password(password)
        return RegisterSchema(email=email, name=name, family_name=family_name,
                              password=hashed_password, passphrase={clue : passphrase})

