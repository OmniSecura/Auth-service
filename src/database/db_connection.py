import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DatabaseConnector:
    """Factory for SQLAlchemy engines.

    The connector type is selected via the ``DB_CONNECTOR`` environment
    variable. Database credentials are read from ``USERNAME`` and ``PASSWORD``
    environment variables for non-SQLite backends.
    """

    def __init__(self):
        self.connector = os.getenv("DB_CONNECTOR", "sqlite").lower()
        self._engine = None

    def get_engine(self):
        if self._engine:
            return self._engine

        user = os.getenv("USERNAME", "user")
        password = os.getenv("PASSWORD", "password")

        if self.connector == "sqlite":
            db_path = os.getenv("SQLITE_PATH", "database.db")
            url = f"sqlite:///{db_path}"
        elif self.connector in {"mysql", "msql"}:
            host = os.getenv("MYSQL_HOST", "localhost")
            port = os.getenv("MYSQL_PORT", "3306")
            db = os.getenv("MYSQL_DB", "database")
            url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{db}"
        elif self.connector in {"postgres", "postgresql"}:
            host = os.getenv("POSTGRES_HOST", "localhost")
            port = os.getenv("POSTGRES_PORT", "5432")
            db = os.getenv("POSTGRES_DB", "database")
            url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"
        else:
            raise ValueError(f"Unsupported DB_CONNECTOR: {self.connector}")

        self._engine = create_engine(url, pool_pre_ping=True)
        return self._engine

    def get_session(self):
        engine = self.get_engine()
        return sessionmaker(autocommit=False, autoflush=False, bind=engine)()

db_connector = DatabaseConnector()
engine = db_connector.get_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()