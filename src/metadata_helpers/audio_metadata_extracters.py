from pathlib import Path
from models.audio_record import AudioRecord
from mutagen.mp3 import MP3
from mutagen.asf import ASF


def get_wma_audio_meta_data(file: Path) -> AudioRecord:   
    try:
        audio = ASF(file)
        artist = audio['WM/AlbumArtist'][0].value if 'WM/AlbumArtist' in audio else ""
        album = audio['WM/AlbumTitle'][0].value if 'WM/AlbumTitle' in audio else ""
        title = audio['Title'][0].value if 'Title' in audio else ""
        year = audio['WM/Year'][0].value if 'WM/Year' in audio else ""
        duration = audio.info.length if hasattr(audio, 'info') and hasattr(audio.info, 'length') else 0
        genre = audio['WM/Genre'][0].value if 'WM/Genre' in audio else ""
        return AudioRecord(artist, album, title, duration, genre, 0, year) 
    except Exception as error:
        print(f"WMA error: {file.name} <-----> {error}")

def get_mp3_audio_meta_data(file: Path) -> AudioRecord:   
    try:
        audio = MP3(file)
        artist = audio["TPE1"].text[0] if "TPE1" in audio else audio["TPE2"].text[0] if "TPE2" in audio else ""
        album = audio["TALB"].text[0] if "TALB" in audio else ""
        title = audio["TIT2"].text[0] if "TIT2" in audio else ""
        duration = audio.info.length if hasattr(audio, 'info') and hasattr(audio.info, 'length') else 0
        genre = audio["TCON"].text[0] if "TCON" in audio and len(audio["TCON"].text) > 0 else ""
        position = audio["TRCK"].text[0] if "TRCK" in audio else 0
        year = audio["TORY"].text[0] if "TORY" in audio else 0
        return AudioRecord(artist, album, title, duration, genre, position, year) 
    except Exception as error:
        print(f"MP3 error: {file.name} <-----> {error}")

def get_audio_meta_data(file: Path) -> AudioRecord:   
    if file.suffix == '.mp3':
        return get_mp3_audio_meta_data(file)
    else:
        return get_wma_audio_meta_data(file)