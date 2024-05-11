import json
import tkinter as tk
from tkinter import filedialog

# Open file dialog
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename()

# Read data from file
with open(file_path, 'r') as file:
    data = json.load(file)

# Process data
result = {'Male': {}, 'Female': {}}
for name, path in data.items():
    parts = name.split()
    if parts[0] in ['Male', 'Female']:
        number = parts[1].zfill(2)  # Keep leading zeros
        model = ' '.join(parts[2:])
        if number not in result[parts[0]]:
            result[parts[0]][number] = []
        result[parts[0]][number].append({'name': model, 'path': path})

# Write result to new file
with open('output.json', 'w') as file:
    json.dump(result, file, indent=2)
