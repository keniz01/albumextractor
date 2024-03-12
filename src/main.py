from pathlib import Path
import sys
from tinytag import TinyTag 
from typing import List
import pandas as pd
from utilities import DateTimeUtilities as utils

def run():
    # Get file path
    folder_path = sys.argv[1]
    print(f"\nScanning ${folder_path} for music files ...... \n")

    path = Path(folder_path)

    files = path.rglob("**/*.mp3", case_sensitive=False)

    audio_tags = [TinyTag.get(file) for file in files]
    albums = [{
        "Artist": tag.artist, 
        "Album": tag.album,
        "Track": tag.title, 
        "TrackLength": utils.format_duration(tag.duration),
        "Genre": tag.genre,
        "TrackPosition": tag.track,
        "TrackTotal": tag.track_total,
        "Year": tag.year        
    } for tag in audio_tags]

    df = pd.DataFrame(albums).sort_values(by="Album")  
    print(df)
    print(len(df))

if __name__ == "__main__":
    run()