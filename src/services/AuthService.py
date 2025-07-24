from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from src.schemas.RegisterSchema import RegisterSchema
from src.database.models.User import User
from src.security.secure import hash_password, password_verify


class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def hash_password(self, password: str) -> str:
        return hash_password(password)

    def register_user(self, register_data: RegisterSchema) -> User:
        hashed = self.hash_password(register_data.password)

        user = User(
            email=register_data.email,
            name=register_data.name,
            family_name=register_data.family_name,
            password=hashed,
            passphrase=register_data.passphrase
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def authenticate_user(self, email: str, password: str) -> User:
        user = self.db.query(User).filter(User.email == email).first()

        if not user or not password_verify(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Insufficient email or password",
            )

        return user
