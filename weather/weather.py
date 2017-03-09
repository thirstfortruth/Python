import xml.etree.ElementTree
from xml.dom.minidom import parseString
import dicttoxml
import json
import xmltodict
import re
import collections
import os

a = [1, 2, 3,
     4]
a = (1 + 2 + 3 + 4 + 5
     + 6 + 7 + 8 + 9 + 10)


def read_file_xml(xml_path_to_file):
    try:
        tree = xml.etree.ElementTree.parse(xml_path_to_file)
        xml_dict = xmltodict.parse(xml.etree.ElementTree.tostring(tree.getroot(), method="xml"))
        return dict(xml_dict)
    except xml.etree.ElementTree.ParseError as exc:
        print(exc)


def save_file_xml(tree_xml, path_to_file_xml, source_encoding):
    try:
        with open(path_to_file_xml, 'w', encoding=source_encoding) as data_file_xml:
            xml_string = dicttoxml.dicttoxml(tree_xml)  # .decode("utf-8")
            dom = parseString(xml_string)
            data_file_xml.write(dom.toprettyxml())
    except IOError as e:
        print("Could not fine file: ", path_to_file_xml)
        print(e)


def read_file_json(path_to_file_json, source_encoding):
    #    try:
    with open(path_to_file_json, 'r', encoding=source_encoding) as data_file_json:
        data = json.load(data_file_json)
    return data


#    except json.JSONDecodeError as exc:
#        print(exc)
#        return -1


def save_file_json(data, json_path_to_file, source_encoding):
    try:
        with open(json_path_to_file, 'w', encoding=source_encoding) as outfile:
            json.dump(data, outfile)
    except json.JSONDecodeError as exc:
        print(exc)
        return -1


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
    input_string = re.sub('<[^>]*>', '', input_string) + re.sub('/.*/', '', input_string) + re.sub('/.*/', '',
                                                                                                   input_string)
    input_string = re.sub('/.*/', '', input_string)
    input_string = re.sub('[,.]*', '', input_string)
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
# encodings = ('KOI8-R', 'UTF-8', 'ISO 8859-5', 'Windows-1251')
# ['newsafr.json', 'newscy.json', 'newsfr.json', 'newsit.json']
encodings = ['koi8_r', 'cp1251', 'UTF-8', 'iso8859_5']
for filename in os.listdir(dirname):
    if filename.__contains__(".json") or filename.__contains__(".JSON"):
        file = os.path.join(dirname, filename)
        for encoding in encodings:
            try:
                print("1", file, encoding)
                data = read_file_json(file, encoding)
                text = get_all_text(data)
                most_common_words = get_list_of_popular_words(text, 5)
                print(file, encoding)
                print(most_common_words)
                break
            except:
                print('except')
                continue

                # KOI8-R
                # UTF-8
                # ISO 8859-5
                # Windows-1251
