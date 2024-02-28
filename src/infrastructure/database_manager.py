""" 
Create a database connection string.
"""
import os
from dotenv import load_dotenv
from domain.services.database_manager_abstract import DatabaseManagerAbstract

load_dotenv()

class DatabaseManger(DatabaseManagerAbstract):

    DB_USER = os.getenv("DATABASE_USER")
    DB_PASS = os.getenv("DATABASE_PASSWORD")
    DB_NAME = os.getenv("DATABASE_NAME")
    DB_HOST = os.getenv("DATABASE_HOST")
    DB_PORT = os.getenv("DATABASE_PORT")

    def get_connection_string(self) -> str:
        return f"postgresql://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"