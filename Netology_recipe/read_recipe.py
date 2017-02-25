import xml.etree.ElementTree
from xml.dom.minidom import parseString
import dicttoxml
import yaml
import json
import xmltodict
from pprint import pprint


# parse input lists and create dictionary with recipes
def create_recipes_custom(cr_recipe_names, cr_recipe_ingredients, cr_number_of_ingredients):
    recipe_book = {}
    ingredient_pointer = 0
    for recipe in range(len(cr_recipe_names)):
        recipe_name = cr_recipe_names[recipe]
        ingredients_list = []
        for x in range(cr_number_of_ingredients[recipe]):
            ingredient = list(map(lambda y: y.strip(), cr_recipe_ingredients[ingredient_pointer].split('|')))
            ingredients_list.append(
                {'product': ingredient[0], 'quantity': ingredient[1], 'unit_of_measure': ingredient[2]})
            ingredient_pointer += 1
        recipe_book[recipe_name] = ingredients_list
    return recipe_book


# reading file and splitting information in 3 main lists - recipe names, number of ingredients, ingredients them self
def read_file_custom(path_to_file):
    rf_recipe_names = []
    rf_number_of_ingredients = []
    rf_recipe_ingredients = []
    with open(path_to_file) as recipe_file:
        for line in recipe_file:
            line = line.strip()
            try:
                rf_number_of_ingredients.append(int(line))
                continue
            except ValueError:
                if '|' in line:
                    rf_recipe_ingredients.append(line)
                else:
                    rf_recipe_names.append(line)
        result = [rf_recipe_names, rf_recipe_ingredients, rf_number_of_ingredients]
    return result


def print_custom(pc_recipe_dictionary):
    # Show what we got:
    for k, v in pc_recipe_dictionary.items():
        print('Recipe name: {0}'.format(k))
        for i in range(len(v)):
            print("Ingredient {0}: ".format(i), end='')
            for value in v[i].values():
                print("{0} ".format(value), end='')
            print('')


def read_file_xml(xml_path_to_file):
    try:
        tree = xml.etree.ElementTree.parse(xml_path_to_file)
        xml_dict = xmltodict.parse(xml.etree.ElementTree.tostring(tree.getroot(), method="xml"))
        return dict(xml_dict)
    except xml.etree.ElementTree.ParseError as exc:
        print(exc)


def save_file_xml(tree_xml, path_to_file_xml):
    try:
        with open(path_to_file_xml, 'w') as data_file_xml:
            xml_string = dicttoxml.dicttoxml(tree_xml).decode("utf-8")
            dom = parseString(xml_string)
            data_file_xml.write(dom.toprettyxml())
    except IOError as e:
        print("Could not fine file: ", path_to_file_xml)
        print(e)


def read_file_json(path_to_file_json):
    try:
        with open(path_to_file_json, 'r') as data_file_json:
            data = json.load(data_file_json)
        return data
    except json.JSONDecodeError as exc:
        print(exc)
        return -1


def save_file_json(data, json_path_to_file):
    try:
        with open(json_path_to_file, 'w') as outfile:
            json.dump(data, outfile)
    except json.JSONDecodeError as exc:
        print(exc)
        return -1


def read_file_yaml(path_to_file_yaml):
    with open(path_to_file_yaml, 'r') as stream:
        try:
            return yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            return -1


def save_file_yaml(data_yaml, path_to_file_yaml):
    with open(path_to_file_yaml, 'w') as stream:
        try:
            yaml.dump(data_yaml, stream)
        except yaml.YAMLError as exc:
            print(exc)
            return -1


while True:
    print("Please enter path to recipe file (.ya, .xml, . json):")
    read_file = input()
    print("Please enter file type (YAML, XML, JSON, CUSTOM):")
    file_type = input()
    if file_type == "YAML":
        recipe_dictionary = read_file_yaml(read_file)
    elif file_type == "XML":
        recipe_dictionary = read_file_xml(read_file)
    elif file_type == "JSON":
        recipe_dictionary = read_file_json(read_file)
    elif file_type == "CUSTOM":
        recipe_names, recipe_ingredients, number_of_ingredients = read_file_custom(read_file)
        recipe_dictionary = create_recipes_custom(recipe_names, recipe_ingredients, number_of_ingredients)
    else:
        print("Invalid file type. Please try again.")
        continue
    print("Recipes are: ")
    pprint(recipe_dictionary)
    print("Please enter path to save results:")
    file_save = input()
    print("Please file format :")
    print("Please enter file type (YAML, XML, JSON, CUSTOM):")
    file_type = input()
    if file_type == "YAML":
        save_file_yaml(recipe_dictionary, file_save)
    elif file_type == "XML":
        save_file_xml(recipe_dictionary, file_save)
    elif file_type == "JSON":
        save_file_json(recipe_dictionary, file_save)
    else:
        print("Invalid file type. Please try again.")
        continue
    exit(0)

# file = "D:/Python/GIT_HUB_repository/Netology_recipe/recipes.txt"
# file_yaml = "D:/Python/GIT_HUB_repository/Netology_recipe/recipes.yaml"
# file_json = "D:/Python/GIT_HUB_repository/Netology_recipe/recipes.json"
# file_xml = "D:/Python/GIT_HUB_repository/Netology_recipe/recipes.xml"
# print("Please enter path to file:")
# file = input()
# recipe_names, recipe_ingredients, number_of_ingredients = read_file_custom(file)
# recipe_dictionary = create_recipes_custom(recipe_names, recipe_ingredients, number_of_ingredients)
# print_custom(recipe_dictionary)
# save_file_yaml(recipe_dictionary, file_yaml)
# pprint(read_file_yaml(file_yaml))
# save_file_json(recipe_dictionary, file_json)
# pprint(read_file_yaml(file_json))
# save_file_xml(recipe_dictionary, file_xml)
# pprint(read_file_xml(file_xml))
