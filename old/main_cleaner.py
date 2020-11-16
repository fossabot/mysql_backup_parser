import os 
import glob

USELESS_FILE_EXTENSIONS = [
    '.txt',
    '.lookup',
    '.temp',
]

def main():
    for extension in USELESS_FILE_EXTENSIONS:
        for file in glob.glob('*' + extension):
            print(f"removing file: {file}")
            os.remove(file)

if __name__ == "__main__":
    main()
    