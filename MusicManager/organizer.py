# organizer.py
import os

def get_music_files(directory):
    supported_formats = ('.mp3', '.flac', '.wav', '.m4a')
    music_files = []
    unknown_album_dir = os.path.join(directory, "UnknownAlbum")
    for root, dirs, files in os.walk(unknown_album_dir):
        # 只遍历 UnknownAlbum 根目录下的文件，不包括子文件夹（播放列表）
        if root != unknown_album_dir:
            continue
        for file in files:
            if file.endswith(supported_formats):
                file_path = os.path.join(root, file)
                music_files.append(os.path.relpath(file_path, directory))
    return music_files

def delete_music_file(file_path):
    try:
        full_path = os.path.join(os.getcwd(), file_path)
        # 删除文件
        os.remove(full_path)

        # 删除播放列表中对应的歌曲文件
        base_directory = os.getcwd()
        unknown_album_dir = os.path.join(base_directory, 'UnknownAlbum')
        for playlist in os.listdir(unknown_album_dir):
            playlist_path = os.path.join(unknown_album_dir, playlist)
            if os.path.isdir(playlist_path):
                song_in_playlist = os.path.join(
                    playlist_path, os.path.basename(file_path)
                )
                if os.path.exists(song_in_playlist):
                    os.remove(song_in_playlist)
        return True
    except Exception as e:
        print(f"Error deleting file {file_path}: {e}")
        return False
