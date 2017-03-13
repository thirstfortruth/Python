import sys
import requests
import os
import io

KEY = 'trnsl.1.1.20170312T195442Z.59050bd09458c68c.5a0d57c236667d6f8a883aa1a8d99642f6800167'
URL_TRANSLATE = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
URL_GET_LANGS = 'https://translate.yandex.net/api/v1.5/tr.json/getLangs'
URL_DETECT_LANG = 'https://translate.yandex.net/api/v1.5/tr.json/detect'
USAGE = 'USAGE: translater.py SOURCE_FILE RESULT_FILE FROM_LANG [ TO_LANG (default=ru) ]'

if len(sys.argv) < 4 or len(sys.argv) > 5:
    print('ERROR: please define all mandatory arguments')
    print(USAGE)
    exit(1)
if len(sys.argv) == 5:
    TO_LANG = sys.argv[4]
else:
    TO_LANG = 'ru'

SOURCE_FILE = sys.argv[1]
RESULT_FILE = sys.argv[2]
FROM_LANG = sys.argv[3]


def translate(text, direction):
    params = {
        'key': KEY,
        'text': text,
        'lang': direction}
    response = requests.get(URL_TRANSLATE, params=params)
    return response.json()


def get_langs():
    params = {'key': KEY}
    response = requests.get(URL_GET_LANGS, params=params)
    return response.json()


def validate_direction(dirs, direction):
    if direction in dirs['dirs']:
        return True
    return False


def get_direction(from_lang, to_lang):
    from_lang = from_lang.lower().strip()
    to_lang = to_lang.lower().strip()
    direction = from_lang+'-'+to_lang
    return direction


def check_file(file):
    if os.path.isfile(file):
        return True
    return False


def read_file(file):
    with open(file, 'r') as r_file:
        data = r_file.read().replace('\n', '')
    return data


def write_file(file, text):
    '''with open(file, 'w') as w_file:
        w_file.write(str(text.encode('cp1251'))'''
    with io.open(file, 'w', encoding='utf8') as w_file:
        w_file.write(text)


available_directions = get_langs()
translate_direction = get_direction(FROM_LANG, TO_LANG)

if not validate_direction(available_directions, translate_direction):
    print('Error: translate direction {direction} is not supported.'.format(direction=translate_direction))
    exit(2)
if not check_file(SOURCE_FILE):
    print('Error: file does not exist: "{file}". Creating....'.format(file=SOURCE_FILE))
    exit(3)

source_text = read_file(SOURCE_FILE)
translated_text = translate(source_text, translate_direction)
translated_text = str(translated_text['text'][0])
write_file(RESULT_FILE, translated_text)
