import lupa
from lupa import LuaRuntime
import os
import pandas as pd
import textwrap
import json
import re
class FileParser:
    def __init__(self, file_path):
        self.file_path = file_path


    def parse_file(self):
        encodings = ['utf-8', 'cp1252', 'iso-8859-1', 'latin1']
        for encoding in encodings:
            try:
                with open(self.file_path, 'r', encoding=encoding) as file:
                    lines = file.readlines()
                # If the file was successfully read, break out of the loop
                break
            except UnicodeDecodeError:
                print(f"Failed to read file {self.file_path} with {encoding} encoding. Trying next encoding.")
        else:
            # If all encodings failed, print a message and return None
            print(f"Failed to read file {self.file_path} with all tried encodings. Skipping this file.")
            return None

        return lines

    def write_unreadable_files_to_json(self, json_file_path=None):
        # If no file path is provided, write the JSON file to the directory where the script is running
        json_file_path = json_file_path if json_file_path else os.path.join(os.path.dirname(os.path.realpath(__file__)), 'unreadable_files.json')
        with open(json_file_path, 'w') as json_file:
            json.dump(self.unreadable_files, json_file, indent=4)
        print(f"Unreadable files written to: {json_file_path}")

class Stack:
    def __init__(self):
        self.stack = []

    def clear(self):
        self.stack = []
    def push(self, variable_type):
        level = self.get_level() + 1
        self.stack.append((variable_type, level))

    def pop(self):
        if self.stack:
            self.stack.pop()

    def get_level(self):
        if self.stack:
            return self.stack[-1][1]
        else:
            return 0

    def get_top(self):
        if self.stack:
            return self.stack[-1][0]
        else:
            return None
    def is_empty(self):
        return len(self.stack) == 0

    def get_stack(self):
        return self.stack
    




class LuaFileParser(FileParser):
    def __init__(self, file_path):
        super().__init__(file_path)

    def get_variables(self, file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()

        variables = []
        for i, line in enumerate(lines, start=1):
            if '=' in line:  # Simple condition for variable assignment
                name = line.split('=')[0].strip()  # Get the variable name
                variables.append([f"{os.path.basename(self.file_path)}:{i}", None, None, line])

        return pd.DataFrame(variables, columns=['FileName', 'Extension', 'Type', 'LiteralLine'])
    
    def parse_file(self):
        lines = super().parse_file()
        if lines is None:
            return None

        data = []
        stack = Stack()
        for line_number, line in enumerate(lines, start=1):
            # Split the line into statements
            statements = line.split(';')

            for statement in statements:
                variable_type, stack = self.determine_variable_type(statement.strip(), stack)
                if variable_type is not None:
                    name = f"{os.path.basename(self.file_path)}:{line_number}"
                    data.append([name, ".lua", variable_type, line])

        return pd.DataFrame(data, columns=['FileName', 'Extension', 'Type', 'LiteralLine'])
    

    def determine_variable_type(self, line, stack):
        if 'function' in line:
            stack.push('function')
            return f'f (sl {stack.get_level()})', stack
        elif 'if' in line:
            stack.push('if')
            return f'if (sl {stack.get_level()})', stack
        elif 'elseif' in line:
            stack.pop()
            stack.push('elseif')
            return f'elseif (sl {stack.get_level()})', stack
        elif 'else' in line:
            stack.pop()
            stack.push('else')
            return f'else (sl {stack.get_level()})', stack
        elif 'end' in line:
            stack.pop()
            return f'end {stack.get_top()} (sl {stack.get_level()})', stack
        elif '{' in line and '}' in line:  # Table initialization in the same line
            return f'tb (sl {stack.get_level()})', stack
        elif '{' in line:
            stack.push('table')
            return f'tb (sl {stack.get_level()})', stack
        elif '}' in line:
            stack.pop()
            return f'eof tb (sl {stack.get_level()})', stack
        elif 'local' in line and '=' in line:
            return f'var (fsl {stack.get_level()})', stack
        elif 'require' in line:
            return f'require (sl {stack.get_level()})', stack
        elif 'for' in line:
            stack.push('for')
            return f'for (sl {stack.get_level()})', stack
        elif '(' in line:
            stack.push('parenthesis')
        elif ')' in line:
            stack.pop()
            return None, stack

        return None, stack

        return None, stack
  
class SQLCollector:
    def __init__(self, directory=None):
        # If no directory is provided, use the directory where the script is running
        self.directory = directory if directory else os.path.dirname(os.path.realpath(__file__))
        self.sql_statements = []
        self.unreadable_files = []

    def collect_sql(self):
        for root, dirs, files in os.walk(self.directory):
            for file in files:
                if file.endswith('.lua'):
                    file_path = os.path.join(root, file)
                    print(f"Processing file: {file_path}")
                    parser = LuaFileParser(file_path)
                    df = parser.parse_file()
                    if df is None:
                        self.unreadable_files.append(file_path)
                    else:
                        for index, row in df.iterrows():
                            line = row['LiteralLine']
                            sql_statement = self.extract_sql_statement(line)
                            if sql_statement:
                                self.sql_statements.append(sql_statement)
                                print(f"Found SQL statement: {sql_statement}")
                                
    def extract_sql_statement(self, line):
        # This is a more robust check for SQL statements. It checks for a string that starts with a SQL keyword and ends with a semicolon.
        match = re.search(r'(\"|\')(SELECT|INSERT|UPDATE|DELETE).*;(\"|\')', line, re.IGNORECASE)
        return match.group(0) if match else None

    def write_to_json(self, json_file_path=None):
        # If no file path is provided, write the JSON file to the directory where the script is running
        json_file_path = json_file_path if json_file_path else os.path.join(self.directory, 'sql_statements.json')
        with open(json_file_path, 'w') as json_file:
            json.dump(self.sql_statements, json_file, indent=4)
        print(f"SQL statements written to: {json_file_path}")
        
    def write_unreadable_files_to_json(self, json_file_path=None):
        # If no file path is provided, write the JSON file to the directory where the script is running
        json_file_path = json_file_path if json_file_path else os.path.join(os.path.dirname(os.path.realpath(__file__)), 'unreadable_files.json')
        with open(json_file_path, 'w') as json_file:
            json.dump(self.unreadable_files, json_file, indent=4)
        print(f"Unreadable files written to: {json_file_path}")

# Usage:
collector = SQLCollector()
collector.collect_sql()
collector.write_to_json()
collector.write_unreadable_files_to_json()
