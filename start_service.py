import os
import time
import psycopg2
from psycopg2 import OperationalError
import uvicorn

HOST = os.getenv('POSTGRES_HOST', 'db')
PORT = int(os.getenv('POSTGRES_PORT', '5432'))
USER = os.getenv('AUTH_USERNAME', 'user')
PASSWORD = os.getenv('AUTH_PASSWORD', 'pass')
DATABASE = os.getenv('POSTGRES_DB', 'database')


def wait_for_db():
    while True:
        try:
            conn = psycopg2.connect(
                host=HOST, port=PORT, user=USER, password=PASSWORD, dbname=DATABASE
            )
            conn.close()
            break
        except OperationalError:
            print("Waiting for database...")
            time.sleep(1)


if __name__ == "__main__":
    wait_for_db()
    uvicorn.run("src.server:app", host="0.0.0.0", port=8000)
