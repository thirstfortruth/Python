# parse input lists and create dictionary with recipes
def create_recipes(cr_recipe_names, cr_recipe_ingredients, cr_number_of_ingredients):
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


# reading file and splitting information in 3 main lists - recipe names, number of ingerients, ingrediants themself
def read_file(path_to_file):
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


# file = "D:/Python/GIT_HUB_repository/Netology_recipe/recipes.txt"
print("Please enter path to file:")
file = input()
recipe_names, recipe_ingredients, number_of_ingredients = read_file(file)
recipe_dictionary = create_recipes(recipe_names, recipe_ingredients, number_of_ingredients)

# Show what we got:
for k, v in recipe_dictionary.items():
    print('Recipe name: {0}'.format(k))
    for i in range(len(v)):
        print("Ingredient {0}: ".format(i), end='')
        for value in v[i].values():
            print("{0} ".format(value), end='')
        print('')
# just to see result on cmd screen, freeze program:
while True:
    pass
