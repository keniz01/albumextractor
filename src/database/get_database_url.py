import os
from dotenv import load_dotenv

load_dotenv()

def get_database_url() -> str:
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")
    server = os.getenv("SERVER")
    port = os.getenv("PORT")
    database = os.getenv("DATABASE")
    
    return f'postgresql://{username}:{password}@{server}:{port}/{database}'