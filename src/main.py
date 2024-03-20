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

def sanitize_data(data, data_type):

    def strip_characters(data):
        return data.replace('\0x00', '').replace('\0', '').strip()
    
    if data_type == str:
        return strip_characters(data) if(data) else ""
    elif data_type == int or data_type == float:
        return data if(data) else 0
    else:
        return data

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
        "artist_name": sanitize_data(tag.artist, str),
        "album_title": sanitize_data(tag.album, str),
        "track_title": sanitize_data(tag.title, str), 
        "track_length": utils.format_duration(sanitize_data(tag.duration, float)),
        "genre_name": sanitize_data(tag.genre, str),
        "track_position": sanitize_data(tag.track, int),
        "track_year": sanitize_data(tag.year, int),        
    } for tag in audio_tags]

    def insert_on_conflict_nothing(table, conn, keys, data_iter):
        data = [dict(zip(keys, row)) for row in data_iter]
        stmt = insert(table.table).values(data).on_conflict_do_nothing(index_elements=['artist_name', 'album_title', 'track_title'])
        print(data)
        result = conn.execute(stmt)       
        return result.rowcount
    
    df = pd.DataFrame(albums)
    df.to_sql('tbl_song', engine, if_exists='append', index=False, method=insert_on_conflict_nothing)

    stop_time = time.time()
    print(f"Processed {len(albums)} files in {utils.format_duration(stop_time - start_time)} minutes.")
    
if __name__ == "__main__":
    run()