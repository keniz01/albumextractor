from itertools import chain
from pathlib import Path
import sys
from psycopg2 import OperationalError
from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import declarative_base
import pandas as pd
from dotenv import load_dotenv
import os
from time import time
import concurrent.futures
from formatters.time_formatter import duration_formatter
from mappers.model_to_table_mapper import model_to_table_mapper
from metadata_helpers.audio_metadata_extracters import get_audio_meta_data

# Load environment variables.
load_dotenv()

def make_database_url() -> str:
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")
    server = os.getenv("SERVER")
    port = os.getenv("PORT")
    database = os.getenv("DATABASE")
    
    return f'postgresql://{username}:{password}@{server}:{port}/{database}'

try:
    database_url = make_database_url()
    engine = create_engine(database_url)
except OperationalError as error:
    print(f"Error: {error.pgerror}")

Base = declarative_base() 
Base.metadata.create_all(engine)

def run():
    # Get file path
    folder_path = sys.argv[1]    
    path = Path(folder_path)
    print(f"\n1. Extracting files from {path.absolute()} .............", end="")
    start_time = time()
    files = chain(path.rglob("*.mp3"), path.rglob("*.wma"))
    print("DONE")

    print("\n2. Extracting tags from files.......... ", end="")

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(get_audio_meta_data, file) for file in files]
        audio_tags = [future.result() for future in concurrent.futures.as_completed(futures)]
        audio_rows = model_to_table_mapper(audio_tags)
        print("DONE")    

    def insert_on_conflict_nothing(table, conn, keys, data_iter):
        data = [dict(zip(keys, row)) for row in data_iter]
        stmt = insert(table.table).values(data).on_conflict_do_nothing(index_elements=['artist_name', 'album_title', 'track_title'])
        result = conn.execute(stmt)       
        return result.rowcount
    
    df = pd.DataFrame(audio_rows).fillna("")

    print("\n3. Saving to database ........", end="")
    row_count = df.to_sql('tbl_song', engine, if_exists='append', index=False, method=insert_on_conflict_nothing)
    print("DONE") if row_count > 0 else print("Nothing to save")

    stop_time = time()
    print(f"\nProcessed {len(audio_rows)} files in {duration_formatter(stop_time - start_time)} minutes.")
    
if __name__ == "__main__":
    run()