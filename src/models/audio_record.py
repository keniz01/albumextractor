class AudioRecord:
    def __init__(self, artist_name: str, album_title: str, track_title: str, 
                 track_length: float, genre_name: str, track_position: int, track_year: int):
        self.artist_name = artist_name
        self.album_title = album_title
        self.track_title = track_title
        self.track_length = track_length
        self.genre_name = genre_name
        self.track_position = track_position
        self.track_year = track_year