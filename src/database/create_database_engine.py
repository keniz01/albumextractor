from psycopg2 import OperationalError
from sqlalchemy import Engine, create_engine

from database.get_database_url import get_database_url

def create_database_engine() -> Engine:
    try:
        database_url = get_database_url()
        engine = create_engine(database_url)
        return engine
    except OperationalError as error:
        print(f"Error: {error.pgerror}")