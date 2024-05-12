import os
import glob

def delete_files_and_empty_dirs(start_path):
    for dirpath, dirnames, filenames in os.walk(start_path, topdown=False):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            if not file_path.endswith(('.lua', '.txt', '.json')):
                os.remove(file_path)
        if not os.listdir(dirpath):
            os.rmdir(dirpath)

# Call the function with the path to the current directory
delete_files_and_empty_dirs(os.path.dirname(os.path.realpath(__file__)))
