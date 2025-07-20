from fastapi import APIRouter, Depends, HTTPException
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session

from src.schemas.RegisterSchema import RegisterSchema
from src.security.exceptions import user_policies
from src.database.models.User import User
from src.database.db_connection import get_db
from src.services.AuthService import register_user

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
        try:
            user_policies(
                register_data.email,
                register_data.name,
                register_data.family_name,
                register_data.password,
                register_data.clue,
                register_data.passphrase,
            )
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        user = register_user(register_data, db)
        return RegisterSchema(
            email=user.email,
            name=user.name,
            family_name=user.family_name,
            password=user.password,
            passphrase=user.passphrase,
            clue=user.clue
        )
