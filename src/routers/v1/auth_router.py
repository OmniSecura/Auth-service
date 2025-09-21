from fastapi import APIRouter, Depends, HTTPException, Response, Request
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session

from src.schemas.RegisterSchema import RegisterSchema, RegisterSchemaForUser
from src.schemas.LoginSchema import LoginSchema
from src.security.exceptions import user_policies
from src.database.db_connection import get_db
from src.services.AuthService import AuthService
from src.security.auth import create_access_token, get_current_user
from src.database.models.User import User
from src.routers.v1.websockets import manager
auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@cbv(auth_router)
class AuthorizationRouter:

    @auth_router.post("/login")
    async def login(
        self,
        request: Request,
        response: Response,
        db: Session = Depends(get_db),
    ):
        if request.headers.get("content-type", "").startswith("application/x-www-form-urlencoded"):
            form = await request.form()
            email = form.get("username")
            password = form.get("password")
            passphrase = None
        else:
            body = await request.json()
            login_data = LoginSchema(**body)
            email = login_data.email
            password = login_data.password
            passphrase = login_data.passphrase

        auth_service = AuthService(db)

        try:
            user = auth_service.authenticate_user(
                email,
                password,
                passphrase,
            )
        except HTTPException as exception:
            await manager.send_personal_message(exception.detail, email)
            raise exception

        token = create_access_token(user.id)
        response.set_cookie(
            "access_token",
            token,
            httponly=True,
            secure=True,
            samesite="strict",
        )
        await manager.send_personal_message(f"Hi, {user.name}!", user.email)
        return {"access_token": token, "token_type": "bearer", "message": f"Hi, {user.name}!"}

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
            await user_policies(
                register_data.email,
                register_data.name,
                register_data.family_name,
                register_data.password,
                register_data.passphrase,
            )
        except ValueError as exception:
            await manager.send_personal_message(str(exception), register_data.email)
            raise HTTPException(status_code=400, detail=str(exception))

        auth_service = AuthService(db)
        try:
            user = auth_service.register_user(register_data)
        except HTTPException as exception:
            await manager.send_personal_message(exception.detail, register_data.email)
            raise exception

        await manager.send_personal_message(f"Hi, {user.name}!", user.email)

        return RegisterSchemaForUser(
            email=user.email,
            name=user.name,
            family_name=user.family_name,
        )

    @auth_router.post("/logout", dependencies=[Depends(get_current_user)])
    async def logout(self, response: Response):
        response.delete_cookie(
            "access_token",
            httponly=True,
            secure=True,
            samesite="strict",
        )
        return {"message": "Logged out successfully"}

    @auth_router.get("/role")
    async def role(self, current_user: User = Depends(get_current_user)):
        return {"role": current_user.role}

    @auth_router.post("/language/{lang}")
    async def language_choice(
            self,
            lang: str,
            current_user: User = Depends(get_current_user),
            db: Session = Depends(get_db),
    ):
        auth_service = AuthService(db)
        user = auth_service.language_choice(lang, current_user.id)
        return {"message": f"Language set to {user.language}"}

    @auth_router.get("/language")
    async def get_language(
            self,
            current_user: User = Depends(get_current_user),
            db: Session = Depends(get_db),
    ):
        auth_service = AuthService(db)
        lang = auth_service.get_language(current_user.id)

        if not lang:
            raise HTTPException(status_code=404, detail="Language not set")

        return lang
