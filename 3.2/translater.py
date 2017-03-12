import requests
# key:
# trnsl.1.1.20170312T195442Z.59050bd09458c68c.5a0d57c236667d6f8a883aa1a8d99642f6800167
# Detect:
# https://translate.yandex.net/api/v1.5/tr.json/detect ?
# key=<API-ключ>
#  & text=<текст>
#  & [hint=<список вероятных языков текста>]
#  & [callback=<имя callback-функции>]
#
# translate request
# https://translate.yandex.net/api/v1.5/tr.json/translate ?
# key=<API-ключ>
#  & text=<переводимый текст>
#  & lang=<направление перевода>
#  & [format=<формат текста>]
#  & [options=<опции перевода>]
#  & [callback=<имя callback-функции>]

KEY = 'trnsl.1.1.20170312T195442Z.59050bd09458c68c.5a0d57c236667d6f8a883aa1a8d99642f6800167'
URL = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
params = {
    'key': KEY,
    'text': 'Some common text',
    'lang': 'en-ru'}
response = requests.get(URL, params=params)
data = response.json()
translated = ''.join(data['text'])
print(translated)
