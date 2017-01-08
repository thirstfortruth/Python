#parse input lists and create dictionary with recipes
def create_recipes(recipe_names, recipe_ingredients, number_of_ingredients):
	recipe_book = {}
	ingredient_pointer = 0
	for recipe in range(len(recipe_names)):
		recipe_name = recipe_names[recipe]
		ingredients_list = []
		for x in range(number_of_ingredients[recipe]):
			ingredient = list(map(lambda x: x.strip(),recipe_ingredients[ingredient_pointer].split('|')))
			ingredients_list.append({'product' : ingredient[0], 'quantity' : ingredient[1], 'unit_of_measure' : ingredient[2]})
			ingredient_pointer += 1
		recipe_book[recipe_name] = ingredients_list
	return recipe_book
#reading file and splitting information in 3 main lists - recipe names, number of ingerients, ingrediants themself	
def read_file(path_to_file):
	recipe_names = []
	number_of_ingredients = []
	recipe_ingredients = []
	with open(path_to_file) as recipe_file:
		for line in recipe_file:
			line = line.strip();
			try:
				number_of_ingredients.append(int(line))
				continue;
			except ValueError:
				if '|' in line:
					recipe_ingredients.append(line)
				else:
					recipe_names.append(line)
	return(recipe_names, recipe_ingredients, number_of_ingredients)					
file = "D:/Python/GIT_HUB_repository/Netology_recipe/recipes.txt"
print("Please enter path to file:")
#file = input()
recipe_names, recipe_ingredients, number_of_ingredients = read_file(file)
recipe_dictionary = create_recipes(recipe_names, recipe_ingredients, number_of_ingredients)
for k, v in recipe_dictionary.items():
	print('Recipe name: {0}'.format(k))
	for i in range(len(v)):
		for value in v[i].values():
			print(value, end = ' ')
		print('\n')
file = input()