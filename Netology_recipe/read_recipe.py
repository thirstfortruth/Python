def create recipes(recipe_names, recipe ingredients):
	pass
def read_file(path_to_file):
	recipe_names = []
	number_of_ingredients = []
	recipe_ingedients = [[]]
	with open(path_to_file) as recipe_file:
		for line in recipe_file:
			recipe_name = recipe_file.readline();
			try:
				number_of_ingredients.append(int(line))
				continue;
			except ValueError:
				if '|' in line:
					recipe_ingedients.append(line)
				else:
					number_of_ingredients.append(line)
	print(recipe_names,number_of_ingredients,recipe_ingedients,sep='\n')			
		
file = 'D:\Python\GIT_HUB_repository\Netology - recipe\recipes.txt'
read_file(file)