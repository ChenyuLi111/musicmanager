# playlist.py
import os
import shutil
from mutagen import File

UNKNOWN_ALBUM_DIR_NAME = "UnknownAlbum"

def create_playlist(name, songs, base_directory):
    unknown_album_dir = os.path.join(
        base_directory, UNKNOWN_ALBUM_DIR_NAME
    )
    playlist_dir = os.path.join(unknown_album_dir, name)
    os.makedirs(playlist_dir, exist_ok=True)
    for song in songs:
        source_path = os.path.join(base_directory, song['file_path'])
        destination_path = os.path.join(
            playlist_dir, os.path.basename(song['file_path'])
        )
        if not os.path.exists(destination_path):
            shutil.copy2(source_path, destination_path)

def load_playlists(base_directory):
    playlists = {}
    unknown_album_dir = os.path.join(
        base_directory, UNKNOWN_ALBUM_DIR_NAME
    )
    if not os.path.exists(unknown_album_dir):
        return playlists
    # 列出 UnknownAlbum 目录下的所有子文件夹，作为播放列表
    for item in os.listdir(unknown_album_dir):
        playlist_path = os.path.join(unknown_album_dir, item)
        if os.path.isdir(playlist_path):
            # 获取该播放列表文件夹内的所有音乐文件
            songs = []
            for root, dirs, files in os.walk(playlist_path):
                for file in files:
                    if file.endswith(('.mp3', '.flac', '.wav', '.m4a')):
                        song_path = os.path.join(root, file)
                        relative_path = os.path.relpath(
                            song_path, base_directory
                        )
                        audio = File(song_path)
                        if audio is None:
                            continue
                        title = audio.get(
                            'title', [os.path.splitext(file)[0]]
                        )[0]
                        artist = audio.get('artist', ['Unknown Artist'])[0]
                        genre = audio.get('genre', ['Unknown Genre'])[0]
                        decade = extract_decade(audio)
                        song = {
                            'title': title,
                            'artist': artist,
                            'genre': genre.lower(),
                            'decade': decade,
                            'file_path': relative_path
                        }
                        songs.append(song)
            playlists[item] = songs
    return playlists

def extract_decade(audio):
    year = audio.get('date', ['Unknown'])[0]
    try:
        year = int(year[:4])
        decade = (year // 10) * 10
        return f"{decade}s"
    except:
        return 'Unknown'
