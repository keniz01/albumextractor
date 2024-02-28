'''
Program entry - main.py.
'''
from pathlib import Path
import sys
from infrastructure.database_manager import DatabaseManger as dm
import mutagen
from tinytag import TinyTag 

def run():
    '''
    Triggers/starts the extraction process.
    1. Prompt for file parent folder.
        1.1 Scan parent folder for sub folders (recursive)
        1.2 Scand for files (mp3, wma)
        1.3 For each file, extract meta data
        1.4 Model extract meta data into domain model
        1.5 Insert data model into database
    '''
    root_folder = sys.argv[1]

    print('Root path: ', root_folder)

    root = Path(root_folder)
    for path in root.rglob('*'):  # '*' pattern for all files and directories
        if path.is_dir():
            files = [file for file in path.rglob('*.mp3')]
            album = TinyTag.get(files[0]).album
            for file in files:
                audio = TinyTag.get(file)
                print("Title:" + audio.title) 
                print("Artist: " + audio.artist) 
                print("Genre:" + audio.genre) 
                print("Year Released: " + audio.year) 
                print("Duration: " + str(audio.duration) + " seconds") 
                print("TrackTotal: " + str(audio.track_total)) 


if __name__ == "__main__":
    run()