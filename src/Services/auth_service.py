from sqlmodel import SQLModel

from AuthService import auth_db, AUTH_SESSION
from src.database.models import *

class AuthService:
    def __init__(self):
        self.engine = auth_db
        self.session = AUTH_SESSION

    def create_db_and_tables(self):
        SQLModel.metadata.create_all(self.engine)

