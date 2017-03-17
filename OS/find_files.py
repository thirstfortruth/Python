import glob
import os.path
import io
import chardet

SOURCE_DIRECTORY = './Advanced Migrations/'


def detect_encoding(in_string):
    return chardet.detect(in_string)['encoding']


def read_file(filename):
    file = open(filename, 'rb')
    detect_data = file.read(32768)
    encoding = detect_encoding(detect_data)
    try:
        with io.open(filename, 'r', encoding=encoding) as temp_file:
            data = temp_file.read().replace('\n', '')
        return data
    except:
        print('ERROR: autodetected encoding {encoding} is not match for file: {file}'.format(encoding=encoding,
                                                                                             file=filename))
        return ''


def limit_results(pattern, files):
    out_list = []
    for inner_file in files:
        if pattern in read_file(inner_file):
            out_list.append(inner_file)
    return out_list


def main_cycle(source_directory):
    list_of_files = set(glob.glob(os.path.join(source_directory, "*.sql")))
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

main_cycle(SOURCE_DIRECTORY)
