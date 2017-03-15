import glob
import os.path
import signal
import sys
import io
import codecs


def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

migrations = './Advanced Migrations/'


def read_file(filename):
    try:
        with io.open(filename, 'r', encoding='utf8') as temp_file:
            data = temp_file.read().replace('\n', '')
    except:
        with io.open(filename, 'r', encoding='cp1251') as temp_file:
            data = temp_file.read().replace('\n', '')
    finally:
        print('ERROR: encoding is not defined. Exiting...')
        exit(1)
    return data


def read_file_coded(filename):
    try:
        with codecs.open(filename, 'r', encoding='utf8') as temp_file:
            data = temp_file.read().replace('\n', '')
    except:
        with io.open(filename, 'r', encoding='cp1251') as temp_file:
            data = temp_file.read().replace('\n', '')
    finally:
        print('ERROR: encoding is not defined. Exiting...')
        exit(1)
    return data


def limit_results(pattern, files):
    out_list = []
    for inner_file in files:
        if pattern in read_file_coded(inner_file):
            out_list.append(inner_file)
    return out_list


def main_cycle():
    list_of_files = set(glob.glob(os.path.join(migrations, "*.sql")))
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

main_cycle()