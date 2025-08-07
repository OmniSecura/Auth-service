from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from src.schemas.RegisterSchema import RegisterSchema
from src.database.models.User import User
from src.security.secure import hash_password, password_verify
from src.security.rate_limiter import (
    is_locked,
    record_failed_attempt,
    reset_attempts,
)


class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def hash_password(self, password: str) -> str:
        return hash_password(password)

    def register_user(self, register_data: RegisterSchema) -> User:
        if self.db.query(User).filter(User.email == register_data.email).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        hashed = self.hash_password(register_data.password)

        processed_clue = None
        hashed_passphrase = None
        if register_data.passphrase:
            processed_clue = "".join(word[0] for word in register_data.passphrase)
            hashed_passphrase = [self.hash_password(passphrase) for passphrase in register_data.passphrase]

        user = User(
            email=register_data.email,
            name=register_data.name,
            family_name=register_data.family_name,
            password=hashed,
            clue=processed_clue,
            passphrase=hashed_passphrase,
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def authenticate_user(self, email: str, password: str, passphrase: list[str] | None) -> User:
        if is_locked(email):
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Account temporarily locked due to failed login attempts",
            )
        user = self.db.query(User).filter(User.email == email).first()

        if not user or not password_verify(password, user.password):
            record_failed_attempt(email)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Insufficient email or password",
            )
        if user.passphrase:
            if not passphrase or len(passphrase) != len(user.passphrase) or not all(
                password_verify(word, stored) for word, stored in zip(passphrase, user.passphrase)
            ):
                record_failed_attempt(email)
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid passphrase",
                )

        reset_attempts(email)
        return user
