import subprocess
import os
import glob
import re

# initialize global variables
program, source_dir, results = '', '', ''


def check_directory(directory):
    if not os.path.isdir(directory):
        print('Directory does not exist: "{dir}". Creating....'.format(dir=directory))
        os.makedirs(directory)


def process_files(input_files):
    for file in input_files:
        file_extension = re.split('\.', file)
        output_file = re.sub('(.[^.]*$)', '_output.' + file_extension[len(file_extension) - 1], file)
        output_file = os.path.join(results, os.path.basename(output_file))
        output_file = os.path.normpath(output_file)
        program_norm = os.path.normpath(program)
        file = os.path.normpath(file)
        # print([program, '-resize 200', file, output_file])
        e = subprocess.run([program_norm, '-resize', '200', file, output_file])
        print(e.returncode)


def multythreaded_processing(num_of_threads, input_files):
    files_threaded = [[] for i in range(num_of_threads)]
    for cur_num in range(len(input_files)):
        thread = cur_num % num_of_threads
        files_threaded[thread].append(input_files[cur_num])
    for thread in range(num_of_threads):
        print('Processing thread:', thread)
        process_files(files_threaded[thread])


# get required variables
while True:
    program = 'D:/Python/jmistx_repo/PY1_Lesson_2.5/homework/convert.exe'
    #source_dir = 'D:/Python/GIT_HUB_repository/2.5/Source'
    input('Please enter source directory:', source_dir)
    files = glob.glob(os.path.join(source_dir, "*.jpg"))
    #results = 'D:/Python/GIT_HUB_repository/2.5/Result'
    input('Please enter source directory:', results)
    check_directory(results)
    if len(files) == 0:
        print('No files found. Please try again')
        continue
    break

multythreaded_processing(2, files)
