import ast
import glob
import os


DELETE_PREVIOUS_RUNS = False
FILE_ENCODING = 'utf-8'



file_list : list = [ ]
current_state : dict = {'table_name':"unknown", 'keys':[], 'extra_comments':""}

def non_insert_line_handler(line):
    line = line.replace('`', "'")
    if line.startswith('DROP TABLE IF EXISTS'):
        global current_state
        current_state = ast.literal_eval(line.split('DROP TABLE IF EXISTS')[1].strip().strip(';'))
        return current_state
    else:
        return None

def insert_line_handler(line):
    "INSERT INTO 'admin' ('admin_id', 'username', 'email', 'password', 'status', 'created_at', 'updated_at') VALUES (1, 'admin', 'admin@gmail.com', 'b79cd395f3a6ca252d09222a9230322a', 1, '2019-12-12 00:00:00', '2019-12-12 00:00:00'); -- PW Unknown"
    # this is the expected input statement for this
    line = line.replace('`', "'")
    # convert to single quotes
    line_split_values = line.split('VALUES')
    # we now have 2 strings one with key names the other with the values
    keys_str = "(" + line_split_values[0].split('(')[1].strip()
    #we remove the INSERT INTO table and clean up whitespace, the ( needs to be added to since split removes it
    values_str = line_split_values[1].strip().replace(';', "")
    # we remove the ending ; and the extra whitespace in the string
    values_str = values_str.replace('NULL', "'None'")
    keys = ast.literal_eval(keys_str)
    # the keys are obtained here
    values = ast.literal_eval(values_str)
    # the values are obtained here
    
    return_dict = {}
    for i in range(len(keys)):
        return_dict[keys[i]] = values[i]
    #<file> # placeholder for all files
    with open(str(current_state) + ".txt", 'a', encoding='utf-8') as write_file:
        print(return_dict, file = write_file)
        write_file.flush()
    return(return_dict)


def init():
    #this checks for all the files in the current folder.
    global file_list
    for file in glob.glob('*.sql'):
        file_list.append(file)



def main():
    init()
    for file in file_list:
        print(f"Processing {file} now...")
        choice = input(f"Do you want to parse this file? [Y/N]: ")
        if choice in ["N", "n", "No", "no", "nO"]: continue
        file_object = open(file, encoding='utf-8')
        for line in file_object:
            if line.startswith('INSERT INTO'):
                insert_line_handler(line)
            else:
                non_insert_line_handler(line)


if __name__ == "__main__":
    try:
        input("Waiting for User Input to Begin main() ...")
        main()
    except KeyboardInterrupt:
        print('The program was interrupted in between. The files may not be correct')
        
