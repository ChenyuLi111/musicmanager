# main.py
import tkinter as tk
from gui import MusicManagerGUI

def main():
    root = tk.Tk()
    app = MusicManagerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
