from sqlalchemy.dialects.postgresql import insert
from constants.table_constants import TBL_RECORD_IMPORT
import pandas as pd
from database.create_database_engine import create_database_engine

def save_tags_to_database(audio_tags: list) -> int:
    
    def insert_on_conflict_nothing(table, conn, keys, data_iter):
        data = [dict(zip(keys, row)) for row in data_iter]
        stmt = insert(table.table).values(data).on_conflict_do_nothing(index_elements=['artist_name', 'album_title', 'track_title'])
        result = conn.execute(stmt)       
        return result.rowcount
    
    df = pd.DataFrame(audio_tags).fillna("")
    engine = create_database_engine()
    row_count = df.to_sql(TBL_RECORD_IMPORT, engine, if_exists='append', index=False, method=insert_on_conflict_nothing)
    return row_count