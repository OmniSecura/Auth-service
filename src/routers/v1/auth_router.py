from fastapi import APIRouter
from fastapi_utils.cbv import cbv

auth_router = APIRouter(prefix="/auth", tags=["Auth"])

@cbv(auth_router)
class AuthorizationRouter():
    @auth_router.post("/login")
    async def login(self, username: str, password: str):
        return {"message": f"Logged in as {username}"}

    @auth_router.post("/register")
    async def register(self, username: str, password: str):
        return {"message": f"Logged in as {username}"}

