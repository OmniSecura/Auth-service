from sqlalchemy.orm import sessionmaker

from src.database.db_connection import engine

auth_db = engine
AUTH_SESSION = sessionmaker(bind=auth_db, autoflush=False, autocommit=False)
