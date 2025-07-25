from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session

from src.schemas.RegisterSchema import RegisterSchema, RegisterSchemaForUser
from src.schemas.LoginSchema import LoginSchema
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
        response: Response,
        login_data: LoginSchema,
        db: Session = Depends(get_db),
    ):
        auth_service = AuthService(db)

        try:
            user = auth_service.authenticate_user(login_data.email, login_data.password)
        except HTTPException as exception:
            raise exception

        token = create_access_token(user.id)
        response.set_cookie(
            "access_token", token, httponly=True, secure=True, samesite="strict"
        )
        return {"message": f"Hi, {user.name}!"}

    @auth_router.get("/user/credentials")
    async def credentials(self, current_user: User = Depends(get_current_user)):
        return {
            "email": current_user.email,
            "name": current_user.name,
            "family_name": current_user.family_name,
        }

    @auth_router.post("/register", response_model=RegisterSchemaForUser)
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

        return RegisterSchemaForUser(
            email=user.email,
            name=user.name,
            family_name=user.family_name,
        )

    @auth_router.post("/logout", dependencies=[Depends(get_current_user)])
    async def logout(self, response: Response):
        response.delete_cookie("access_token")
        return {"message": "Logged out successfully"}
