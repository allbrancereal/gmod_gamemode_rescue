import os
import shutil
import tkinter as tk
from tkinter import filedialog

def copy_and_move_directories(layer0_path):
    # Keep track of all .lua files
    lua_files = set()

    # First pass: Copy and rename .lua files
    for dirpath, dirnames, filenames in os.walk(layer0_path):
        for filename in filenames:
            if filename.endswith('.lua') or filename.endswith(".txt") or filename.endswith('json'):
                # If a file with the same name already exists in lua_files
                if filename in lua_files:
                    base, ext = os.path.splitext(filename)
                    i = 1
                    # Find a new filename
                    while True:
                        new_filename = f"{base}_{i}{ext}"
                        if new_filename not in lua_files:
                            break
                        i += 1
                    filename = new_filename
                lua_files.add(filename)
                # Copy .lua file to layer 0
                shutil.copy(os.path.join(dirpath, filename), os.path.join(layer0_path, filename))

    # Second pass: Move original .lua files and delete old directories
    for dirpath, dirnames, filenames in os.walk(layer0_path):
        for filename in filenames:
            if filename.endswith('.lua'):
                # Move .lua file to layer 0
                shutil.move(os.path.join(dirpath, filename), os.path.join(layer0_path, filename))
        # Delete old directories
        for dirname in dirnames:
            shutil.rmtree(os.path.join(dirpath, dirname))

def select_directory():
    root = tk.Tk()
    root.withdraw()  # Hide the main window