# gui.py
import tkinter as tk
from tkinter import messagebox, simpledialog
from organizer import get_music_files, delete_music_file
from search import parse_query, search_music
from playlist import create_playlist, load_playlists
import os
import pygame  # 用于音乐播放

class MusicManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Manager")
        self.root.geometry("800x600")

        # 初始化Pygame Mixer用于音乐播放
        pygame.mixer.init()

        # 定义莫兰迪色系
        self.colors = {
            "main": "#E4D6C0",
            "organizer": "#C5C3C6",
            "search": "#D1CFCF",
            "playlist": "#D8C3A5",
        }

        # 基础目录是项目目录
        self.base_directory = os.getcwd()

        # 加载音乐库
        self.music_library = self.load_music_library()

        # 加载播放列表
        self.playlists = load_playlists(self.base_directory)

        # 创建主菜单
        self.create_main_menu()

    def create_main_menu(self):
        # 清除当前窗口内容
        for widget in self.root.winfo_children():
            widget.destroy()

        # 设置背景颜色
        self.root.configure(bg=self.colors["main"])

        # 标题
        tk.Label(
            self.root,
            text="Music Manager",
            bg=self.colors["main"],
            font=("Helvetica", 24),
            fg="black"
        ).pack(pady=40)

        # 导航框架
        self.nav = tk.Frame(self.root, bg=self.colors["main"])
        self.nav.pack(pady=20)

        # Organizer 按钮
        self.organize_btn = tk.Button(
            self.nav,
            text="Organizer",
            bg="#A89F94",
            fg="black",
            activebackground="#B4AFA7",
            command=self.organizer_view,
            width=15,
            height=2
        )
        self.organize_btn.pack(side=tk.LEFT, padx=10)

        # Search 按钮
        self.search_btn = tk.Button(
            self.nav,
            text="Search",
            bg="#A89F94",
            fg="black",
            activebackground="#B4AFA7",
            command=self.search_music_view,
            width=15,
            height=2
        )
        self.search_btn.pack(side=tk.LEFT, padx=10)

        # Playlist 按钮
        self.playlist_btn = tk.Button(
            self.nav,
            text="Playlist",
            bg="#A89F94",
            fg="black",
            activebackground="#B4AFA7",
            command=self.playlist_view,
            width=15,
            height=2
        )
        self.playlist_btn.pack(side=tk.LEFT, padx=10)

    def organizer_view(self):
        # 清除当前窗口内容
        for widget in self.root.winfo_children():
            widget.destroy()

        # 设置背景颜色
        self.root.configure(bg=self.colors["organizer"])

        # 标题
        tk.Label(
            self.root,
            text="Music Files",
            bg=self.colors["organizer"],
            font=("Helvetica", 16),
            fg="black"
        ).pack(pady=10)

        # 列表框架
        list_frame = tk.Frame(self.root, bg=self.colors["organizer"])
        list_frame.pack(fill=tk.BOTH, expand=True)

        # 获取音乐文件列表
        music_files = get_music_files(self.base_directory)

        # 滚动条
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 列表框
        self.file_listbox = tk.Listbox(
            list_frame, yscrollcommand=scrollbar.set, width=80
        )
        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.file_listbox.yview)

        # 填充列表框
        for file in music_files:
            self.file_listbox.insert(tk.END, file)

        # 删除按钮
        delete_btn = tk.Button(
            self.root,
            text="Delete Selected",
            bg="#A89F94",
            fg="black",
            command=self.delete_selected_file
        )
        delete_btn.pack(pady=5)

        # 返回按钮
        back_btn = tk.Button(
            self.root,
            text="Back",
            bg="#A89F94",
            fg="black",
            command=self.create_main_menu
        )
        back_btn.pack(pady=10)

    def delete_selected_file(self):
        selected_index = self.file_listbox.curselection()
        if selected_index:
            selected_file = self.file_listbox.get(selected_index)
            confirm = messagebox.askyesno(
                "Confirm Delete",
                f"Are you sure you want to delete '{selected_file}'?"
            )
            if confirm:
                success = delete_music_file(selected_file)
                if success:
                    messagebox.showinfo(
                        "Success", f"Deleted '{selected_file}' successfully."
                    )
                    self.organizer_view()  # 刷新视图
                else:
                    messagebox.showerror(
                        "Error", f"Failed to delete '{selected_file}'."
                    )
        else:
            messagebox.showwarning(
                "No Selection", "Please select a file to delete."
            )

    def search_music_view(self):
        # 清除当前窗口内容
        for widget in self.root.winfo_children():
            widget.destroy()

        # 设置背景颜色
        self.root.configure(bg=self.colors["search"])

        # 标题
        tk.Label(
            self.root,
            text="Search Music",
            bg=self.colors["search"],
            font=("Helvetica", 16),
            fg="black"
        ).pack(pady=10)

        # 查询输入框
        self.search_entry = tk.Entry(self.root, width=40)
        self.search_entry.pack(pady=5)

        # 搜索按钮
        search_btn = tk.Button(
            self.root,
            text="Search",
            bg="#A89F94",
            fg="black",
            command=self.execute_search
        )
        search_btn.pack(pady=5)

        # 搜索结果列表框
        self.search_results_listbox = tk.Listbox(self.root)
        self.search_results_listbox.pack(
            fill=tk.BOTH, expand=True, padx=20, pady=10
        )

        # 播放按钮
        play_btn = tk.Button(
            self.root,
            text="Play Selected",
            bg="#A89F94",
            fg="black",
            command=self.play_selected_search_result
        )
        play_btn.pack(pady=5)

        # 停止按钮
        stop_btn = tk.Button(
            self.root,
            text="Stop",
            bg="#A89F94",
            fg="black",
            command=self.stop_playback
        )
        stop_btn.pack(pady=5)

        # 返回按钮
        back_btn = tk.Button(
            self.root,
            text="Back",
            bg="#A89F94",
            fg="black",
            command=self.create_main_menu
        )
        back_btn.pack(pady=10)

    def execute_search(self):
        query = self.search_entry.get()
        if query:
            parsed = parse_query(query)
            results = search_music(self.music_library, parsed)
            self.display_search_results(results)
        else:
            messagebox.showwarning(
                "Input Required", "Please enter a search query."
            )

    def display_search_results(self, results):
        self.search_results_listbox.delete(0, tk.END)
        self.search_results = results  # 存储结果以便播放
        if not results:
            self.search_results_listbox.insert(tk.END, "No results found.")
            return
        for song in results:
            display_text = f"{song.get('title', 'Unknown Title')} - " \
                           f"{song.get('artist', 'Unknown Artist')}"
            self.search_results_listbox.insert(tk.END, display_text)

    def play_selected_search_result(self):
        selected_index = self.search_results_listbox.curselection()
        if selected_index:
            song_info = self.search_results[selected_index[0]]
            song_path = song_info.get('file_path')
            if song_path:
                full_path = os.path.join(self.base_directory, song_path)
                if os.path.exists(full_path):
                    try:
                        pygame.mixer.music.load(full_path)
                        pygame.mixer.music.play()
                    except Exception as e:
                        messagebox.showerror(
                            "Error", f"Unable to play song: {e}"
                        )
                else:
                    messagebox.showerror(
                        "Error", "Song file not found."
                    )
            else:
                messagebox.showerror(
                    "Error", "Song path not specified."
                )
        else:
            messagebox.showwarning(
                "No Selection", "Please select a song to play."
            )

    def playlist_view(self):
        # 清除当前窗口内容
        for widget in self.root.winfo_children():
            widget.destroy()

        # 设置背景颜色
        self.root.configure(bg=self.colors["playlist"])

        # 标题
        tk.Label(
            self.root,
            text="Your Playlists",
            bg=self.colors["playlist"],
            font=("Helvetica", 16),
            fg="black"
        ).pack(pady=10)

        # 列表框架
        playlist_frame = tk.Frame(self.root, bg=self.colors["playlist"])
        playlist_frame.pack(fill=tk.BOTH, expand=True)

        # 列表框
        self.playlist_listbox = tk.Listbox(playlist_frame)
        self.playlist_listbox.pack(
            side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20
        )

        # 填充列表框
        self.playlist_listbox.delete(0, tk.END)
        self.playlists = load_playlists(self.base_directory)
        for name in self.playlists:
            self.playlist_listbox.insert(tk.END, name)

        # 按钮
        open_btn = tk.Button(
            playlist_frame,
            text="Open Playlist",
            bg="#A89F94",
            fg="black",
            command=self.open_playlist
        )
        open_btn.pack(pady=5)

        create_btn = tk.Button(
            playlist_frame,
            text="Create Playlist",
            bg="#A89F94",
            fg="black",
            command=self.create_new_playlist
        )
        create_btn.pack(pady=5)

        # 返回按钮
        back_btn = tk.Button(
            self.root,
            text="Back",
            bg="#A89F94",
            fg="black",
            command=self.create_main_menu
        )
        back_btn.pack(pady=10)

    def open_playlist(self):
        selected_index = self.playlist_listbox.curselection()
        if selected_index:
            playlist_name = self.playlist_listbox.get(selected_index)
            songs = self.playlists.get(playlist_name, [])
            self.playlist_songs_view(playlist_name, songs)
        else:
            messagebox.showwarning(
                "No Selection", "Please select a playlist to open."
            )

    def playlist_songs_view(self, playlist_name, songs):
        # 清除当前窗口内容
        for widget in self.root.winfo_children():
            widget.destroy()

        # 设置背景颜色
        self.root.configure(bg=self.colors["playlist"])

        # 标题
        tk.Label(
            self.root,
            text=f"Playlist: {playlist_name}",
            bg=self.colors["playlist"],
            font=("Helvetica", 16),
            fg="black"
        ).pack(pady=10)

        # 歌曲列表框架
        songs_frame = tk.Frame(self.root, bg=self.colors["playlist"])
        songs_frame.pack(fill=tk.BOTH, expand=True)

        # 列表框
        self.songs_listbox = tk.Listbox(songs_frame)
        self.songs_listbox.pack(
            side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20
        )

        # 填充列表框
        for song in songs:
            display_text = f"{song.get('title', 'Unknown Title')} - " \
                           f"{song.get('artist', 'Unknown Artist')}"
            self.songs_listbox.insert(tk.END, display_text)

        # 播放按钮
        play_btn = tk.Button(
            songs_frame,
            text="Play Selected",
            bg="#A89F94",
            fg="black",
            command=lambda: self.play_selected_song(songs)
        )
        play_btn.pack(pady=5)

        # 停止按钮
        stop_btn = tk.Button(
            songs_frame,
            text="Stop",
            bg="#A89F94",
            fg="black",
            command=self.stop_playback
        )
        stop_btn.pack(pady=5)

        # 返回按钮
        back_btn = tk.Button(
            self.root,
            text="Back",
            bg="#A89F94",
            fg="black",
            command=self.playlist_view
        )
        back_btn.pack(pady=10)

    def play_selected_song(self, songs):
        selected_index = self.songs_listbox.curselection()
        if selected_index:
            song_info = songs[selected_index[0]]
            song_path = song_info.get('file_path')
            if song_path:
                full_path = os.path.join(self.base_directory, song_path)
                if os.path.exists(full_path):
                    try:
                        pygame.mixer.music.load(full_path)
                        pygame.mixer.music.play()
                    except Exception as e:
                        messagebox.showerror(
                            "Error", f"Unable to play song: {e}"
                        )
                else:
                    messagebox.showerror(
                        "Error", "Song file not found."
                    )
            else:
                messagebox.showerror(
                    "Error", "Song path not specified."
                )
        else:
            messagebox.showwarning(
                "No Selection", "Please select a song to play."
            )

    def stop_playback(self):
        pygame.mixer.music.stop()

    def create_new_playlist(self):
        name = simpledialog.askstring("Create Playlist", "Enter playlist name:")
        if name:
            # 允许用户选择歌曲
            selected_songs = self.select_songs()
            if selected_songs:
                create_playlist(name, selected_songs, self.base_directory)
                messagebox.showinfo(
                    "Success", f"Playlist '{name}' created successfully!"
                )
                self.playlists = load_playlists(self.base_directory)
                self.playlist_view()
            else:
                messagebox.showwarning(
                    "No Songs Selected", "Please select songs for the playlist."
                )

    def select_songs(self):
        select_window = tk.Toplevel(self.root)
        select_window.title("Select Songs")
        select_window.geometry("500x400")
        select_window.configure(bg=self.colors["playlist"])

        tk.Label(
            select_window,
            text="Select songs for the playlist:",
            bg=self.colors["playlist"],
            fg="black"
        ).pack(pady=10)

        songs_listbox = tk.Listbox(select_window, selectmode=tk.MULTIPLE)
        songs_listbox.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        for song in self.music_library:
            song_display = f"{song.get('title', 'Unknown Title')} - " \
                           f"{song.get('artist', 'Unknown Artist')}"
            songs_listbox.insert(tk.END, song_display)

        selected_songs = []

        def add_selected():
            indices = songs_listbox.curselection()
            for i in indices:
                selected_songs.append(self.music_library[i])
            select_window.destroy()

        add_btn = tk.Button(
            select_window,
            text="Add Selected",
            bg="#A89F94",
            fg="black",
            command=add_selected
        )
        add_btn.pack(pady=10)

        select_window.grab_set()
        self.root.wait_window(select_window)

        return selected_songs

    def load_music_library(self):
        music_library = []
        supported_formats = ('.mp3', '.flac', '.wav', '.m4a')
        unknown_album_dir = os.path.join(self.base_directory, "UnknownAlbum")
        for root, dirs, files in os.walk(unknown_album_dir):
            for file in files:
                if file.endswith(supported_formats):
                    path = os.path.join(root, file)
                    relative_path = os.path.relpath(path, self.base_directory)
                    from mutagen import File
                    audio = File(path)
                    if audio is None:
                        continue
                    # 如果元数据中没有标题，则使用文件名（去除扩展名）
                    title = audio.get('title', [os.path.splitext(file)[0]])[0]
                    artist = audio.get('artist', ['Unknown Artist'])[0]
                    genre = audio.get('genre', ['Unknown Genre'])[0]
                    decade = self.extract_decade(audio)
                    song = {
                        'title': title,
                        'artist': artist,
                        'genre': genre.lower(),
                        'decade': decade,
                        'file_path': relative_path
                    }
                    music_library.append(song)
        return music_library

    def extract_decade(self, audio):
        year = audio.get('date', ['Unknown'])[0]
        try:
            year = int(year[:4])
            decade = (year // 10) * 10
            return f"{decade}s"
        except:
            return 'Unknown'
