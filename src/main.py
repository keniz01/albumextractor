from pathlib import Path
import sys
from psycopg2 import OperationalError
from tinytag import TinyTag 
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
import pandas as pd
from utilities import DateTimeUtilities as utils
from dotenv import load_dotenv
import os

# Load environment variables.
load_dotenv()

username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
server = os.getenv("SERVER")
port = os.getenv("PORT")
database = os.getenv("DATABASE")

DATABASE_URL = f'postgresql://{username}:{password}@{server}:{port}/{database}'

try:
    engine = create_engine(DATABASE_URL)
except OperationalError as error:
    print(error.pgerror)

Base = declarative_base()

class Song(Base):
    __tablename__ = 'tbl_song'

    id = Column(Integer, primary_key=True, autoincrement="auto")
    artist_name = Column(String, nullable=True)
    album_title = Column(String, nullable=True)   
    track_title = Column(String, nullable=True)
    track_length = Column(String, nullable=True)
    genre_name = Column(String, nullable=True)
    track_position = Column(Integer, nullable=True)
    track_total = Column(Integer, nullable=True)
    track_year = Column(Integer, nullable=True)
 
Base.metadata.create_all(engine)

def run():
    # Get file path
    folder_path = sys.argv[1]
    print(f"\nScanning ${folder_path} for music files ...... \n")

    path = Path(folder_path)

    files = path.rglob("**/*.mp3")

    audio_tags = [TinyTag.get(file) for file in files]
    albums = [{
        "artist_name": tag.artist, 
        "album_title": tag.album,
        "track_title": tag.title, 
        "track_length": utils.format_duration(tag.duration),
        "genre_name": tag.genre,
        "track_position": tag.track,
        "track_total": tag.track_total,
        "track_year": tag.year        
    } for tag in audio_tags]

    df = pd.DataFrame(albums)
    df.to_sql('tbl_song', engine, if_exists='append', index=False)
    result_df = pd.read_sql_query('SELECT * FROM tbl_song', engine)
    print(result_df)
    
if __name__ == "__main__":
    run()