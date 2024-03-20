from pathlib import Path
import sys
from psycopg2 import OperationalError
from tinytag import TinyTag, TinyTagException
from sqlalchemy import UniqueConstraint, create_engine, Column, Integer, String
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import declarative_base
import pandas as pd
from utilities import DateTimeUtilities as utils
from dotenv import load_dotenv
import os
import time

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
    print(f"Error: {error.pgerror}")

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
    track_year = Column(Integer, nullable=True)
    __table_args__ = (UniqueConstraint('artist_name', 'album_title', 'track_title'),)
 
Base.metadata.create_all(engine)

def run():
    # Get file path
    folder_path = sys.argv[1]
    print(f"\nScanning ${folder_path} for music files ...... \n")

    path = Path(folder_path)

    start_time = time.time()
    files = path.rglob("*.mp3")

    audio_tags = []
    
    for file in files:
        try:
            audio_tag = TinyTag.get(file)
            audio_tags.append(audio_tag)
        except TinyTagException:
            print(f"Failed to process ==> {file.name}")

    albums = [{
        "artist_name": tag.artist if tag.artist is not None else "",
        "album_title": tag.album if tag.album is not None else "",
        "track_title": tag.title if tag.title is not None else "", 
        "track_length": utils.format_duration(tag.duration) if tag.duration is not None else 0.0,
        "genre_name": tag.genre if tag.genre is not None else "",
        "track_position": tag.track if tag.track else 0,
        "track_year": tag.year if tag.year else 0,        
    } for tag in audio_tags]

    def insert_on_conflict_nothing(table, conn, keys, data_iter):
        data = [dict(zip(keys, row)) for row in data_iter]
        stmt = insert(table.table).values(data).on_conflict_do_nothing(index_elements=['artist_name', 'album_title', 'track_title'])
        print(stmt)
        result = conn.execute(stmt)       
        return result.rowcount
    
    df = pd.DataFrame(albums)
    df.to_sql('tbl_song', engine, if_exists='append', index=False, method=insert_on_conflict_nothing)

    stop_time = time.time()
    print(f"Processed {len(albums)} files in {utils.format_duration(stop_time - start_time)} minutes.")
    
if __name__ == "__main__":
    run()