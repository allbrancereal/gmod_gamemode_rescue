
import json
import os
import tkinter as tk
from tkinter import filedialog
import pprint

def get_user_input():
    includes = []
    excludes = []

    while True:
        user_input = input("Enter include() or exclude() statements, or 'go' to proceed: ")

        if user_input.lower() in ['go', 'done', 'yes', 'quit']:
            break
        elif user_input.lower() == 'print':
            return 'print', includes, excludes

        statements = user_input.split(',')
        for statement in statements:
            if 'include(' in statement and ')' in statement:
                includes.extend([i.strip() for i in statement.split('include(')[1].split(')')[0].split('|')])
            elif 'exclude(' in statement and ')' in statement:
                excludes.extend([e.strip() for e in statement.split('exclude(')[1].split(')')[0].split('|')])

    return 'continue', includes, excludes

def filter_models():
    # Create a root window and hide it
    root = tk.Tk()
    root.withdraw()

    # Open a file dialog starting in the script's directory
    filepath = filedialog.askopenfilename(initialdir=os.path.dirname(os.path.realpath(__file__)), title="Select playermodels.json", filetypes=(("JSON files", "*.json"), ("all files", "*.*")))

    # Load all models
    with open(filepath, 'r') as f:
        all_models = json.load(f)
        
    # Print all models to the console
    print("All models:")
    pprint.pprint(all_models)
    
    # Check if the whitelist file exists
    whitelist = []
    if os.path.exists('whitelist.json'):
        # Ask the user if they want to read the current whitelist
        read_whitelist = input("Do you want to read the current whitelist? (yes/no): ")
        if read_whitelist.lower() == 'yes':
            with open('whitelist.json', 'r') as f:
                whitelist = json.load(f)

    includes = []
    excludes = []

    while True:
        action, new_includes, new_excludes = get_user_input()
        includes.extend(new_includes)
        excludes.extend(new_excludes)

        if action == 'print':
            print('-' * 40)  # Print delimiter line
            print([model for model in all_models if not any(exclude in model.lower() for exclude in excludes) and any(include in model.lower() for include in includes)])
            print('-' * 40)  # Print delimiter line
        elif action == 'continue':
            break

    # Apply exclude filter
    models_after_excludes = [model for model in all_models if not any(exclude in model.lower() for exclude in excludes)]

    # Apply include filter
    final_models = [model for model in models_after_excludes if any(include in model.lower() for include in includes)]

    # Add whitelist items not in exclude list
    final_models += [model for model in whitelist if not any(exclude in model.lower() for exclude in excludes)]

    # Remove duplicates
    final_models = list(set(final_models))

    # Ask the user if they want to print or write the final models
    action = input("Do you want to print or write the final models to a file? (print/write): ")
    if action.lower() == 'print':
        print(final_models)
    elif action.lower() == 'write':
        # Save final models to new JSON file
        with open('whitelist.json', 'w') as f:
            json.dump(final_models, f, indent=4)

# Usage
filter_models()
