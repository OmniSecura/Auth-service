from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session

from src.schemas.RegisterSchema import RegisterSchema
from src.security.exceptions import user_policies
from src.database.db_connection import get_db
from src.services.AuthService import AuthService
from src.security.auth import create_access_token, get_current_user
from src.database.models.User import User

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@cbv(auth_router)
class AuthorizationRouter:

    @auth_router.post("/login")
    async def login(
        self,
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db),
    ):
        auth_service = AuthService(db)

        try:
            user = auth_service.authenticate_user(form_data.username, form_data.password)
        except HTTPException as e:
            raise e

        token = create_access_token({"sub": str(user.id)})
        return {"access_token": token, "token_type": "bearer"}

    @auth_router.get("/me")
    async def read_me(
            self,
            current_user: User = Depends(get_current_user),
    ):
        return {
            "email": current_user.email,
            "name": current_user.name,
            "family_name": current_user.family_name,
            "role": current_user.role,
        }

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
                register_data.passphrase,
            )
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        auth_service = AuthService(db)
        user = auth_service.register_user(register_data)

        return RegisterSchema(
            email=user.email,
            name=user.name,
            family_name=user.family_name,
            password=user.password,
            passphrase=user.passphrase
        )
