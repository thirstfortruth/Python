import glob
import os.path
import signal
import sys


def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

migrations = './Advanced Migrations/'
list_of_files = set(glob.glob(os.path.join(migrations, "*.sql")))


def read_file(filename):
    with open(filename, 'r') as temp_file:
        data = temp_file.read().replace('\n', '')
    return data


def limit_results(pattern, files):
    out_list = []
    for inner_file in files:
        if pattern in read_file(inner_file):
            out_list.append(inner_file)
    return out_list


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

