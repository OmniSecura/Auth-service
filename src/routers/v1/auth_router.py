from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session
import json

from src.schemas.RegisterSchema import RegisterSchema
from src.security.secure import hash_password
from src.database.models.User import User
from src.database.db_connection import get_db

auth_router = APIRouter(prefix="/auth", tags=["Auth"])

@cbv(auth_router)
class AuthorizationRouter:

    @auth_router.post("/login")
    async def login(self, username: str, password: str):
        return {"message": f"Logged in as {username}"}

    @auth_router.post("/register", response_model=RegisterSchema)
    async def register(
        self,
        register_data: RegisterSchema,
        db: Session = Depends(get_db),
    ):
        hashed_password = hash_password(register_data.password)
        user = User(
            email=register_data.email,
            name=register_data.name,
            family_name=register_data.family_name,
            password=hashed_password,
            passphrase=json.dumps(register_data.passphrase),
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return RegisterSchema(
            email=user.email,
            name=user.name,
            family_name=user.family_name,
            password=user.password,
            passphrase=register_data.passphrase,
        )

