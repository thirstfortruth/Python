import json
file = input('Please enter filename:')
# 'D:/Python/GIT_HUB_repository/Netology_recipe/recipes.json'
with open(file, 'r') as json_data_file:
    data = json.load(json_data_file)
print(data)