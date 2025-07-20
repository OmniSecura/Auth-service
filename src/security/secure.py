from argon2 import PasswordHasher

def hash_password(password: str) -> str:
    return PasswordHasher().hash(password)

def password_verify(password: str, hashed_password: str) -> bool:
    return PasswordHasher().verify(password, hashed_password)
