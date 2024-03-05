'''
Program entry - main.py.
'''
from pathlib import Path
import sys
from infrastructure.database_manager import DatabaseManger as dm
from tinytag import TinyTag 
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3

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

    def format_duration(total_length: int) -> str:
        mins, secs = divmod(total_length, 60)
        mins = round(mins)
        secs = round(secs)
        time_format = '{:02d}:{:02d}'.format(mins, secs)
        return time_format

    root_folder = sys.argv[1]

    print('Root path: ', root_folder)

    root = Path(root_folder)
    for path in root.rglob('*'):  # '*' pattern for all files and directories
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
            for key in EasyID3.valid_keys.keys():
                print(key)

            audio = MP3(path, ID3=EasyID3)

            audio.pprint()
            print(audio.info.length)
            print(audio.info.bitrate)

            # audio = TinyTag.get(path)
            # print(f"track_total: {audio.track_total}")
            # print(f"total_discs: {audio.disc_total}")
            # print(f"album: {audio.album}")
            # print(f"Title: {audio.title}")
            # print(f"Genre: {audio.genre}") 
            # print(f"TrackNo: {audio.track}") 
            # print(f"Year Released: {audio.year}") 
            # print(f"Duration: {format_duration(audio.duration)}")

if __name__ == "__main__":
    run()