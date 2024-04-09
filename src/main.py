from itertools import chain
from pathlib import Path
import sys
from time import time
from database.extract_tags_from_files import extract_tags_from_files
from database.save_tags_to_database import save_tags_to_database
from formatters.time_formatter import duration_formatter

def get_folder_root() -> Path:
    folder_root = sys.argv[1]    
    path = Path(folder_root)    
    return path

def get_files_from_all_folders(folder_root: Path) -> chain[Path]:
    return chain(folder_root.rglob("*.mp3"), folder_root.rglob("*.wma"))

if __name__ == "__main__":
    folder_root = get_folder_root()
    print(f"\n1. Extracting files from {folder_root.absolute()} .............", end=" ")
    start_time = time()
    files = get_files_from_all_folders(folder_root)

    # file_count = len(list(files))
    # if file_count == 0:
    #     print("\n2. 0 files found.")
    #     sys.exit()

    # print(f'Found {file_count} files')

    print("\n2. Extracting tags from files .......... ", end=" ")
    audio_tags = extract_tags_from_files(files)
    print("DONE")  

    print("\n3. Saving to database ........ ", end=" ")
    saved_rows = save_tags_to_database(audio_tags)
    if saved_rows > 0:
        print("DONE") 
    else:
        print("0 records saved")
        sys.exit()

    stop_time = time()
    print(f"\n4. Processed {saved_rows} files in {duration_formatter(stop_time - start_time)} minutes.")