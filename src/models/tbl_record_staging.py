from sqlalchemy import Column, Integer, String, UniqueConstraint
from constants.table_constants import TBL_RECORD_IMPORT
from sqlalchemy.orm import declarative_base

Base = declarative_base
class RecordStagingTable(Base):
    __tablename__ = TBL_RECORD_IMPORT

    id = Column(Integer, primary_key=True, autoincrement="auto")
    artist_name = Column(String, nullable=True)
    album_title = Column(String, nullable=True)
    track_title = Column(String, nullable=True)
    track_length = Column(String, nullable=True)
    genre_name = Column(String, nullable=True)
    track_position = Column(Integer, nullable=True)
    track_year = Column(Integer, nullable=True)
    album_label = Column(String, nullable=True)

    __table_args__ = (UniqueConstraint('artist_name', 'album_title', 'track_title'),)