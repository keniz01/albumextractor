from dataclasses import dataclass

@dataclass
class AudioRecord:
    artist_name: str
    album_title: str
    track_title: str
    track_length: float
    genre_name: str
    track_position: int
    track_year: int
    album_label: str