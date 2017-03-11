import subprocess
import os
import glob
import re

program, source_dir, results = '', '', ''


def check_directory(directory):
    if not os.path.isdir(directory):
        print('Directory does not exist: "{dir}". Creating....'.format(dir=directory))
        os.makedirs(directory)

while True:
    program = 'D:/Python/jmistx_repo/PY1_Lesson_2.5/homework/convert.exe'
    source_dir = 'D:/Python/GIT_HUB_repository/2.5/Source'
    # input('Please enter source directory:', source_dir)
    files = glob.glob(os.path.join(source_dir, "*.jpg"))
    results = 'D:/Python/GIT_HUB_repository/2.5/Result'
    # input('Please enter source directory:', result)
    check_directory(results)
    if len(files) == 0:
        print('No files found. Please try again')
        continue
    break

for file in files:
    file_extension = re.split('\.', file)
    output_file = re.sub('(.[^.]*$)', '_output.' + file_extension[len(file_extension) - 1], file)
    output_file = os.path.join(results, os.path.basename(output_file))
    output_file = os.path.normpath(output_file)
    program = os.path.normpath(program)
    file = os.path.normpath(file)

    print([program, '-resize 200', file, output_file])
    e = subprocess.run([program, '-resize', '200', file, output_file])
    print(e.returncode)

