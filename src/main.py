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

class Album():
    def __init__(self, title: str, duration: str, total_tracks: int, year: int) -> None:
        self.title = title
        self.duration = format_duration(duration)
        self.total_tracks = total_tracks
        self.year = year

class Track():
    def __init__(self, title: str, duration: str, position: int, year: int) -> None:
        self.title = title
        self.duration = format_duration(duration)
        self.position = position
        self.year = year

class Compilation():
    def __init__(self) -> None:
        self.album = Album()
        self.tracks = List[Track]

    def add_album(self, album: Album):
        self.album = album
    
    def add_track(self, track: Track):
        self.tracks.append(track)

def run():
    root_folder = sys.argv[1]
    root = Path(root_folder)

    for index, path in enumerate(root.rglob('*')):  # '*' pattern for all files and directories
        if path.is_dir():
            files = [file for file in path.rglob('*.mp3')]
            
            if(len(files) > 0):
                artist = TinyTag.get(files[0]).artist

                # insert into artists table
                album = TinyTag.get(files[0]).album
                print(f"Album: {album}")
                total_discs = TinyTag.get(files[0]).disc_total
                print(f"total_discs: {total_discs}")
                track_total = TinyTag.get(files[0]).track_total
                print(f"track_total: {track_total}")
                # insert into album table

                for file in files:
                    audio = TinyTag.get(file)
                    print("Title:" + audio.title)
                    print("Genre:" + audio.genre) 
                    print(f"TrackNo: {audio.track}") 
                    print("Year Released: " + audio.year) 
                    print(f"Duration: {audio.duration:.2f} seconds") 
                    print(f"DiscNo: {audio.dics}") 
        else:

            if path.suffix != '.mp3':
                continue;

            audio = TinyTag.get(path)

            if index == 0:
                library.add_album(
                    title=audio.album,
                    duration=None,
                    year=audio.year,
                    track_total=audio.track_total
                )

            library.add_track(
                title=audio.title,
                duration=format_duration(audio.duration),
                year=audio.year,
                position=audio.track
            )

            library.add_genre(name=audio.genre)
            # print(f"track_total: {audio.track_total}")
            # print(f"total_discs: {audio.disc_total}")
            # print(f"album: {audio.album}")
            # print(f"Title: {audio.title}")
            # print(f"Genre: {audio.genre}") 
            # print(f"TrackNo: {audio.track}") 
            # print(f"Year Released: {audio.year}") 
            # print(f"Duration: {format_duration(audio.duration)}")

    print(library)

if __name__ == "__main__":
    run()