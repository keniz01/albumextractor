class AudioComposition:

    def __init__(self):
        self.tracks = []
        self.artist = {}
        self.album = {}
        self.label = {}
        self.genre = {}

    def add_artist(self, name: str):
        self.artist = { name }

    def add_label(self, name: str):
        self.label = { name } 

    def add_genre(self, name: str):
        self.genre = { name }   

    def add_album(self, title: str, duration: str, year: int, track_total: int):
        self.album = {
            title,
            duration,
            year,
            track_total 
        }

    def add_track(self, title: str, duration: str, year: int, position: int): 
        self.tracks.append({ title, duration, year, position })                    
