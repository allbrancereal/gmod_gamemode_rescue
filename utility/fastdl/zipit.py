import os
import shutil
import tkinter as tk
from tkinter import filedialog

def bzip2_compress(directory, dry_run=False):
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        compressed_filepath = filepath + '.bz2'

        # Compress the file
        if not dry_run:
            with open(filepath, 'rb') as f_in, open(compressed_filepath, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

        print(f'Compressed: {filepath} -> {compressed_filepath}')

        # Remove the original file
        if not dry_run:
            os.remove(filepath)

        print(f'Removed: {filepath}')

def main():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    directory = filedialog.askdirectory()  # Open the file dialog
    bzip2_compress(directory)

if __name__ == '__main__':
    main()
