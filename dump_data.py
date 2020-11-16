import ast
import glob
import re

SETTINGS = {
    'encoding': 'utf-8',
    'file_list': [],
}

STATE = {
    'table_name': "",
    'keys': [],
    'comments': ''
}


def line_preformatter(line: str) -> str:
    """Preformats a line to be better readable by `ast.literal_eval()`

    Args:
        line (str): Input String from SQL File

    Returns:
        str: Formatted string with special replacements
    """
    # <!-- Clear comments -->
    #line = line[:line.find('--')]
    # <!-- Clear \r and \n -->
    line = line.strip()
    # <!-- Replace backticks -->
    line = line.replace("`", "'")
    # <!-- Replaces SQL null with Python null -->
    line = line.replace("NULL", "None")
    # <!-- Remove line terminator (;) to directly pass it to AST -->
    line = line.strip(';')
    
    return line

def insert_line_handler(line: str) -> dict:
    """Parses a `INSERT INTO` (SQL) statement to return a dict with all the values

    Args:
        line (str): The line containing the `INSERT INTO` statement

    Returns:
        dict: A dict with `{'key':'value'}` for every key in the SQL Statement
    """
    # <!-- INSERT INTO 'table' (keys) VALUES (values) -->
    alpha, beta = line.split('VALUES')
    # <!-- Alpha (Keys) Processing -->
    _, alpha = alpha.split('INSERT INTO')
    table_name = alpha.split(' ')[1]
    _, alpha = alpha.split(table_name)
    KEYS = ast.literal_eval(alpha.strip())
    TABLE = ast.literal_eval(table_name.strip())
    # <!-- Alpha (Keys) Processing -->
    VALUES = ast.literal_eval(beta.strip())
    
    RETURN = {}
    for iteration in range(len(KEYS)):
        RETURN[KEYS[iteration]] = VALUES[iteration]
    return {
        'values':RETURN,
        'table':TABLE
    }

def table_definition_handler(line: str) -> dict:
    """Creates a `dict` with the data of the given CREATE TABLE string.

    Args:
        line (str): Input String

    Returns:
        dict: dict with all the relevant data
    """


def main():
    """main event function
    """
    global STATE
    for file_name in SETTINGS['file_list']:
        f_read = open(file_name, 'r', encoding=SETTINGS['encoding'])
        f_write = open(file_name + ".dump", "w", encoding=SETTINGS['encoding'])
        create_table_loop = False
        table_desc = ""
        for line in f_read:
            if line.startswith('#'): continue
            elif (create_table_loop):
                table_desc = table_desc + line.strip()
                if line.find(';') != -1: create_table_loop = False
            elif (line.startswith('CREATE')):
                create_table_loop = True
                table_desc =  table_desc + "<!>" +line.strip()
            elif (line.startswith('INSERT')):
                line = line_preformatter(line)
                data = insert_line_handler(line)
                print(
                    f"{data['table']}<!>{data['values']}", 
                    file=f_write
                )
                f_write.flush()
        print(table_desc, file=open('comments.dump', 'w'))

def init():
    """Populates the SQL files to be processed
    """
    global SETTINGS
    for file in glob.glob('*.sql'):
        SETTINGS['file_list'].append(file)


if __name__ == "__main__":
    init()
    main()
