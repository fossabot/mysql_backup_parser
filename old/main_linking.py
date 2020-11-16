import ast
import main_lookups
import base64

VIDEO_FILE = 'videos.txt'
CHAPTER_LOOKUP = main_lookups.CHAPTER
SUB_SUBJECT_LOOKUP = main_lookups.SUB_SUBJECT
SUBJECT_LOOKUP = main_lookups.SUBJECT

FILE_ENCODING = 'utf-8'

OUTPUT_FILE = VIDEO_FILE.removesuffix('.txt') + '.linked' 



def main():
    read_file = open(VIDEO_FILE, encoding=FILE_ENCODING)
    write_file = open(OUTPUT_FILE, 'w', encoding=FILE_ENCODING)
    for line in read_file:
        line_data = ast.literal_eval(line)
        chapter_id = line_data['chapter_id']
        sub_subject_id = line_data['sub_subject_id']
        subject_id = line_data['subject_id']
        
        
        try: chapter = CHAPTER_LOOKUP[int(chapter_id)] 
        except KeyError: chapter = 'OTHER'
        try: sub_subject = SUB_SUBJECT_LOOKUP[int(sub_subject_id)] 
        except KeyError: sub_subject = 'OTHER'
        try: subject = SUBJECT_LOOKUP[int(subject_id)] 
        except KeyError: subject = 'OTHER'
        
        
        data_dict = {}
        # this is the required params
        data_dict['type'] = line_data['type']
        data_dict['subject'] = subject 
        data_dict['sub_subject'] = sub_subject 
        data_dict['chapter'] = chapter 
        data_dict['video_id'] = line_data['video_id']
        data_dict['video_title'] = line_data['video_title']
        data_dict['media_id'] = line_data['media_id']
        data_dict['chapter_id'] = line_data['chapter_id']
        data_dict['video_url'] = f"https://iitsafalta.in/video/watch/{line_data['type']}/{base64.b64encode(str(line_data['video_id']).encode('utf-8')).decode('utf-8')}"
        print(data_dict.__str__(), file=write_file)
        write_file.flush()

if __name__ == "__main__":
    main()

