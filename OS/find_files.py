import glob
import os.path
import signal
import sys


def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

migrations = 'D:/Python/jmistx_repo/PY1_Lesson_2.4/homework/Advanced Migrations/'
list_of_files = set(glob.glob(os.path.join(migrations, "*.sql")))


def limit_results(pattern, files):
    limited_files = set()
    for file in files:
        file_base = os.path.basename(file)
        if file_base.__contains__(pattern):
            limited_files.add(file)
    return limited_files


for file in list_of_files:
    print(file)
print('Total:', len(list_of_files))
while True:
    print('Enter pattern to search')
    pattern_to_search = input()
    list_of_files = limit_results(pattern_to_search, list_of_files)
    for file in list_of_files:
        print(file)
    print('Total:', len(list_of_files))




