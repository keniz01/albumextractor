from formatters.data_sanitizers import sanitize_data
from formatters.time_formatter import duration_formatter
from models.audio_record import AudioRecord

def model_to_table_mapper(audio_records: list[AudioRecord]):
    records = []

    for audio_record in audio_records:

        if audio_record is None:
            continue

        record = {
            "artist_name": sanitize_data(audio_record.artist_name, str),
            "album_title": sanitize_data(audio_record.album_title, str),
            "track_title": sanitize_data(audio_record.track_title, str),
            "track_length": duration_formatter(sanitize_data(audio_record.track_length, float)),
            "genre_name": sanitize_data(audio_record.genre_name, str),
            "track_position": sanitize_data(audio_record.track_position, int),
            "track_year": sanitize_data(audio_record.track_year, int),
            "album_label": sanitize_data(audio_record.album_label, str)
        }  

        records.append(record)

    return records