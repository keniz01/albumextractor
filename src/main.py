from itertools import chain
from pathlib import Path
import sys
from psycopg2 import OperationalError
from tinytag import TinyTag, TinyTagException
from sqlalchemy import UniqueConstraint, create_engine, Column, Integer, String
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import declarative_base
import pandas as pd
from dotenv import load_dotenv
import os
from time import time
import concurrent.futures
from mutagen.mp3 import MP3

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

def format_duration(total_length: float) -> str:
    
    minutes, seconds = divmod(total_length, 60)
    hours, minutes = divmod(minutes, 60)

    seconds = round(seconds)
    minutes = round(minutes)
    hours = round(hours)        
    
    if hours == 0:
        return "%02d:%02d" % (minutes, seconds)
    
    return "%02d:%02d:%02d" % (hours, minutes, seconds)

def sanitize_data(data, data_type):
    '''
    Sanitizes input based on data type.
    \nint defaults to 0
    \nfloat defaults to 0.0
    \nstring defaults to ""
    '''
    def strip_characters(data):
        return data.replace('\0x00', '').replace('\0', '').strip()
    
    if data_type is str:
        return strip_characters(data) if(data) else ""
    elif data_type is int or data_type is float:
        try:
            return float(data) if data_type is float else int(data) if data_type is int else 0
        except:
            return 0.0 if data_type is float else 0
    else:
        return data

def read_file_tags(file: Path) -> MP3:   
    try:
        return MP3(file)
    except Exception as error:
        print(error)
        print(f"\n\tFailed to extract ID3 tags from:  {file.name}")
            
def run():
    # Get file path
    folder_path = sys.argv[1]    
    path = Path(folder_path)
    print(f"\n1. Extracting files from {path.absolute()} .............", end="")
    start_time = time()
    files = chain(path.rglob("*.mp3"),path.rglob("*.wma"))
    print("DONE")

    print("\n2. Extracting tags from files.......... ", end="")

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(read_file_tags, file) for file in files]
        audio_tags = [future.result() for future in concurrent.futures.as_completed(futures)]
        print("DONE")    

    print("\n3. Creating album collection .............", end="")

    albums = []
    for tag in audio_tags:

        if not tag:
            continue

        album = {
            "artist_name": tag["TPE1"].text[0] if "TPE1" in tag else tag["TPE2"].text[0] if "TPE2" in tag else "",
            "album_title": tag["TALB"].text[0] if "TALB" in tag else "",
            "track_title": tag["TIT2"].text[0] if "TIT2" in tag else "", 
            "track_length": utils.format_duration(tag["TLEN"].text[0]) if "TLEN" in tag else 0,
            "genre_name": tag["TCON"].text[0] if "TCON" in tag else "",
            "track_position": tag["TRCK"].text[0] if "TRCK" in tag else 0,
            "track_year": tag["TORY"].text[0] if "TORY" in tag else 0,        
        }

        sampe: list[int] = ['a',2, "23"]
        albums.append(album)

    print("DONE")

    def insert_on_conflict_nothing(table, conn, keys, data_iter):
        data = [dict(zip(keys, row)) for row in data_iter]
        stmt = insert(table.table).values(data).on_conflict_do_nothing(index_elements=['artist_name', 'album_title', 'track_title'])
        result = conn.execute(stmt)       
        return result.rowcount
    
    df = pd.DataFrame(albums).fillna("")

    print("\n4. Saving to database ........", end="")
    row_count = df.to_sql('tbl_song', engine, if_exists='append', index=False, method=insert_on_conflict_nothing)
    print("DONE") if row_count > 0 else print("Nothing to save")

    stop_time = time()
    print(f"\nProcessed {len(albums)} files in {utils.format_duration(stop_time - start_time)} minutes.")
    
if __name__ == "__main__":
    run()