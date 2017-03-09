import xml.etree.ElementTree
import json
import xmltodict
import re
import collections
import os
from xml.parsers import expat


class MyParser(object):

    def XmlDecl(self, version, encoding, standalone):
        return encoding

    def Parse(self, data):
        Parser = expat.ParserCreate()
        Parser.XmlDeclHandler = self.XmlDecl
        Parser.Parse(data, 1)


def read_file_xml(xml_path_to_file):
    try:
        tree = xml.etree.ElementTree.parse(xml_path_to_file)
        print(xml.etree.ElementTree.tostring(xml_path_to_file))
        xml_dict = xmltodict.parse(xml.etree.ElementTree.tostring(tree.getroot(), method="xml"))
        return dict(xml_dict)
    except xml.etree.ElementTree.ParseError as exc:
        print(exc)


def read_file_json(path_to_file_json, source_encoding):
    #    try:
    with open(path_to_file_json, 'r', encoding=source_encoding) as data_file_json:
        data = json.load(data_file_json)
    return data


def get_list_of_popular_words(json_data, limit):
    words = json_data.split(' ')
    large_words = []
    for word in words:
        if len(word) > 5:
            large_words.append(word)
    result = collections.Counter(large_words)
    return result.most_common(limit)
    # return result


# filter out tags <> and link on site. Leave only valuable information
def filer_out_trash(input_string):
    # remove tags
    input_string = re.sub('<[^>]*>', '', input_string)
    # remove links like /link.ru/
    input_string = re.sub('/.*/', '', input_string)
    # remove dots commas and other signs
    input_string = re.sub('[,.!?]*', '', input_string)
    return input_string


def get_all_text(json_data):
    channel = json_data.get('rss').get('channel')
    title = channel.get('title')
    description = channel.get('description')
    item = channel.get('item')
    result = title + ' ' + description
    for items in item:
        # had to add try except part because we have newsit.json file which has different structure
        try:
            item_title = filer_out_trash(items.get('title').get('__cdata'))
            item_description = filer_out_trash(items.get('description').get('__cdata'))
        except:
            item_title = filer_out_trash(items.get('title'))
            item_description = filer_out_trash(items.get('description'))
        result = result + ' ' + item_title + ' ' + item_description
    return result


# file = "D:/Python/Netology_python_course/GIT/Python_course/PY1_Lesson_2.3/newsafr.json"
dirname = "D:/Python/Netology_python_course/GIT/Python_course/PY1_Lesson_2.3/"
encodings = {'newsafr.json': 'UTF-8', 'newscy.json': 'koi8_r', 'newsfr.json': 'iso8859_5', 'newsit.json': 'cp1251'}
for filename in os.listdir(dirname):
    print(filename)
    if filename.__contains__(".json") or filename.__contains__(".JSON"):
        file = os.path.join(dirname, filename)
        try:
            data = read_file_json(file, encodings[filename])
            text = get_all_text(data)
            most_common_words = get_list_of_popular_words(text, 5)
            print(file, encodings[filename])
            print(most_common_words)
        except:
            print('Exception appeared')
            continue

# for filename in os.listdir(dirname):
#     if filename.__contains__(".xml") or filename.__contains__(".XML"):
#         file = os.path.join(dirname, filename)
#         print(file)
#         try:
#             data = read_file_xml(file)
#             #print(data)
#             text = get_all_text(data)
#             most_common_words = get_list_of_popular_words(text, 5)
#             print(most_common_words)
#         except:
#             print('Exception appeared')
#             continue
