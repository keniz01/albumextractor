from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

'''
Album
'''
class Album(Base):
    __tablename__ = 'albums'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False, unique=True)
    duration = Column(String)
    total_songs = Column(Integer)
    year = Column = (String)

    artist_id = Column(Integer, ForeignKey('artists.id'))
    artist = relationship("Artist", back_populates="albums")
    genre_id = Column(Integer, ForeignKey('genres.id'))
    genre = relationship("Genre", back_populates="albums")
    label_id = Column(Integer, ForeignKey('labels.id'))
    label = relationship("Label", back_populates="albums")