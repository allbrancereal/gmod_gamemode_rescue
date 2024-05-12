import os
import shutil

filter_dirs = {"maps", "materials", "models", "sound", "particles", "resource"}
filter_exts = {".bsp", ".vmt", ".vtf", ".png", ".vtx", ".mdl", ".phy", ".vvd", ".mp3", ".wav", ".pcf", ".ttf"}
# Get the directory of the current script
script_dir = os.path.dirname(os.path.realpath(__file__))

# Step 1: Make an index of all the folders in the script's directory
folders = [f for f in os.listdir(script_dir) if os.path.isdir(os.path.join(script_dir, f))]
print(f"Found folders: {folders}")
# Step 2: Go through each one of them, if they have a filter_dirs matching folder then move that matching folder up to root
for folder in folders:
    full_folder_path = os.path.join(script_dir, folder)
    subfolders = [f for f in os.listdir(full_folder_path) if os.path.isdir(os.path.join(full_folder_path, f))]
    for subfolder in subfolders:
        if subfolder in filter_dirs:
            src = os.path.join(full_folder_path, subfolder)
            dst = os.path.join(script_dir, subfolder)
            if not os.path.exists(dst):
                shutil.move(src, dst)
            else:
                for dirpath, dirnames, filenames in os.walk(src):
                    dst_dir = dirpath.replace(src, dst)
                    if not os.path.exists(dst_dir):
                        os.mkdir(dst_dir)
                    for file in filenames:
                        shutil.move(os.path.join(dirpath, file), os.path.join(dst_dir, file))
            print(f"Moved {subfolder} to root")



# Step 3: After going through all the folders and moving, remove all files that do not have the filetype in filter_exts
for folder in filter_dirs:
    if os.path.exists(folder):
        for file in os.listdir(folder):
            if not os.path.splitext(file)[1] in filter_exts:
                os.remove(os.path.join(folder, file))
                print(f"Removed file {file}")

print("Operation completed")
