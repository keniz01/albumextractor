from pathlib import Path
import sys
from tinytag import TinyTag 
from typing import List

def format_duration(total_length: int) -> str:

    mins, secs = divmod(total_length, 60)
    mins = round(mins)
    secs = round(secs)
    time_format = '{:02d}:{:02d}'.format(mins, secs)
    return time_format

class Genre():
    def __init__(self, name: str) -> None:
        self.name = name

class Album():
    def __init__(self, title: str, duration: float, track_total: int, year: int) -> None:
        self.title = title
        self.duration = format_duration(duration)
        self.track_total = track_total
        self.year = year

class Track():
    def __init__(self, title: str, duration: str, position: int, year: int, genre: Genre) -> None:
        self.title = title
        self.duration = format_duration(duration)
        self.position = position
        self.year = year
        self.genre = genre

class Compilation():
    def __init__(self) -> None:
        self.album = Album(title="", duration=0.0, track_total=0,year=0)
        self.tracks = []

    def add_album(self, album: Album):
        self.album = album
    
    def add_track(self, track: Track):
        self.tracks.append(track)

def get_parent_folder_path() -> str:
    parent_folder_path = sys.argv[1]
    pure_path = Path(parent_folder_path)
    return pure_path

def run():

    parent_folder_path = get_parent_folder_path()
    files = [r for r in Path(parent_folder_path).rglob('**/*.mp3')]

    compilation = Compilation()

    for file in files:
        audio = TinyTag.get(file)

        if compilation.album.title != audio.album:
            album = Album(title="", duration=0.0, track_total=0,year=0)
            album.title=audio.album
            album.duration=None
            album.year=audio.year
            album.track_total=audio.track_total

            compilation.add_album(album)
        
        
        track = Track(title="",duration=0.0, position=0, year=0, genre=Genre(name=""))
        track.title=audio.title
        track.duration=format_duration(audio.duration)
        track.year=audio.year
        track.position=audio.track
        track.genre = Genre(audio.genre)

        compilation.add_track(track)

    print(compilation)

if __name__ == "__main__":
    run()