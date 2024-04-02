from itertools import chain
from pathlib import Path
from mappers.model_to_table_mapper import model_to_table_mapper
from metadata_helpers.audio_metadata_extracters import get_audio_meta_data
from models.audio_record import AudioRecord
import concurrent.futures

def extract_tags_from_files(files: chain[Path]) -> list[AudioRecord]:
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(get_audio_meta_data, file) for file in files]
        audio_tags = [future.result() for future in concurrent.futures.as_completed(futures)] 
        return model_to_table_mapper(audio_tags)