import os
import shutil
import tkinter as tk
from tkinter import filedialog

def copy_and_move_files(layer0_path):
    # Keep track of all files
    files = set()

    # First pass: Copy and rename files
    for dirpath, dirnames, filenames in os.walk(layer0_path):
        for filename in filenames:
            src = os.path.join(dirpath, filename)
            dst = os.path.join(layer0_path, filename)
            # If a file with the same name already exists in files
            if filename in files:
                base, ext = os.path.splitext(filename)
                i = 1
                # Find a new filename
                while True:
                    new_filename = f"{base}_{i}{ext}"
                    dst = os.path.join(layer0_path, new_filename)
                    if new_filename not in files:
                        break
                    i += 1
                filename = new_filename
            files.add(filename)
            # Copy file to layer 0
            if not os.path.exists(dst):
                shutil.copy(src, dst)

    # Second pass: Move original files and delete old directories
    for dirpath, dirnames, filenames in os.walk(layer0_path):
        for filename in filenames:
            src = os.path.join(dirpath, filename)
            dst = os.path.join(layer0_path, filename)
            # Move file to layer 0
            if not os.path.exists(dst):
                shutil.move(src, dst)
        # Delete old directories
        for dirname in dirnames:
            shutil.rmtree(os.path.join(dirpath, dirname))

def select_directory():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    layer0_path = filedialog.askdirectory()  # Show the directory dialog
    copy_and_move_files(layer0_path)

# Call the function to select your layer 0 directory
select_directory()
