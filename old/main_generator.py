import os
import glob
import ast

FILE_EXCLUSIONS = [
    'videos.txt',
    'topics.txt'
]

MAIN_LOOKUP_FILE = 'main_lookups.py'

FILE_LIST = []
def init():
    global FILE_LIST
    for file in glob.glob('*.txt'):
        if file not in FILE_EXCLUSIONS: FILE_LIST.append(file)


def generate_id_name_links(file: str):
    data_dict = {}
    id_field = file.removesuffix('s.txt') + '_id'
    name_field = file.removesuffix('s.txt') + '_name'
    for line in open(file, encoding='utf-8'):
        line_data = ast.literal_eval(line)
        data_dict[line_data[id_field]] = line_data[name_field]
    return data_dict


def main():
    init()
    print(f"Merging and updating {MAIN_LOOKUP_FILE}")
    main_lookup = open(MAIN_LOOKUP_FILE,'w',encoding='utf-8')
    
    for file in FILE_LIST:
        to_process_file = file
        output_file = to_process_file.split('.')[0] + '.lookup'
        generated_lookup_dict = generate_id_name_links(to_process_file)
        with open(output_file, 'w', encoding='utf-8') as write_file:
            print(to_process_file.split('s.')[0].upper(), '= ', end="", file=main_lookup)
            main_lookup.write(str(generated_lookup_dict))
            main_lookup.write('\n\n')
            write_file.write(str(generated_lookup_dict))
            print(f"Wrote Temp File {output_file}")
        
    

if __name__ == "__main__":
    main()