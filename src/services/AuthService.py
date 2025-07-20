from sqlalchemy.orm import Session
from src.schemas.RegisterSchema import RegisterSchema
from src.database.models.User import User
from src.security.secure import hash_password

def register_user(register_data: RegisterSchema, db: Session) -> User:
    hashed_password = hash_password(register_data.password)
    user = User(
        email=register_data.email,
        name=register_data.name,
        family_name=register_data.family_name,
        password=hashed_password,
        passphrase=register_data.passphrase,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
