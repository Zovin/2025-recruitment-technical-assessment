from dataclasses import dataclass
from typing import List, Dict, Union
from flask import Flask, request, jsonify
import re

# ==== Type Definitions, feel free to add or modify ===========================
@dataclass
class CookbookEntry:
	name: str
	type: str

@dataclass
class RequiredItem():
	name: str
	quantity: int

@dataclass
class Recipe(CookbookEntry):
	required_items: List[RequiredItem]

@dataclass
class Ingredient(CookbookEntry):
	cook_time: int

class Summary(CookbookEntry):
	required_items: List[RequiredItem]
	cook_time: int

# =============================================================================
# ==== HTTP Endpoint Stubs ====================================================
# =============================================================================
app = Flask(__name__)

# Store your recipes here!
cookbook = []

# Task 1 helper (don't touch)
@app.route("/parse", methods=['POST'])
def parse():
	data = request.get_json()
	recipe_name = data.get('input', '')
	parsed_name = parse_handwriting(recipe_name)
	if parsed_name is None:
		return 'Invalid recipe name', 400
	return jsonify({'msg': parsed_name}), 200

# [TASK 1] ====================================================================
# Takes in a recipeName and returns it in a form that 
def parse_handwriting(recipeName: str) -> Union[str | None]:
	recipeName = re.sub('[-_]', ' ', recipeName)
	recipeName = recipeName.lower()
	recipeName = re.sub('[^a-z ]', "", recipeName)
	recipeName = re.sub(' +', " ", recipeName)
	recipeName = recipeName.title()
	recipeName = recipeName.strip()
	
	if len(recipeName) == 0 :
		return None
	 
	return recipeName


# [TASK 2] ====================================================================
# Endpoint that adds a CookbookEntry to your magical cookbook
@app.route('/entry', methods=['POST'])
def entry():
	data = request.get_json()
	# recipe_name = data.get('input', '')
	entry = createCookbookEntry(data)
	if entry is not None:
		return entry, 400	 
	return jsonify({}), 200

# Takes in a input and either returns an error or adds the entry to input
def createCookbookEntry(input: CookbookEntry):
	if not (input['type'] == 'recipe' or input['type'] == 'ingredient'):	
		return "Input type is invalid"
	elif any(entry for entry in cookbook if entry['name'] == input['name']):
		return "Entry already exists"

	if input['type'] == 'recipe':
		input['required_items'] = input['requiredItems']
		del input['requiredItems']

		temp = [entry['name'] for entry in input['required_items']]
		if len(temp) != len(set(temp)):
			return 'required Items can only have one element per name'
	elif input['type'] == 'ingredient':
		input['cook_time'] = input['cookTime']
		del input['cookTime']

		if input['cook_time'] < 0:
			return 'cook_Time cannot be negative'

	cookbook.append(input)
	return None

# [TASK 3] ====================================================================
# Endpoint that returns a summary of a recipe that corresponds to a query name
@app.route('/summary', methods=['GET'])
def summary():
	name = request.args.get('name')

	summary = create_summary(name)
	if type(summary) is str:
		return summary, 400	 
	return jsonify(summary), 200

# Takes in a recipeName and returns an a summary of the recipe
def create_summary(name: str) -> Summary:
	recipe: CookbookEntry = next(iter([entry for entry in cookbook if entry['name'] == name]), None)

	if recipe == None:
		return "recipe does not exist"
	elif recipe['type'] == 'ingredient':
		return "searched name is not a recipe name"
	
	summary: Summary = recipe
	temp: Union[str | Summary]  = recursive_summary(recipe['required_items'])

	if type(temp) == str:
		return temp

	summary['required_items'] = temp
	summary['cook_time'] = 0
	
	# sums up cookTime for every item in required_items
	for item in summary['required_items']: 
		ingredient: Ingredient = next(iter([entry for entry in cookbook if entry['name'] == name]))
		recipe['cook_time'] += item['quantity'] * ingredient['cook_time']

	return summary

def recursive_summary(required_items: List[RequiredItem]) -> Union[str | Summary]:
	result: List[RequiredItem] = required_items.copy()

	for item in result:
		cookbook_entry: CookbookEntry = next(iter([x for x in cookbook if x['name'] == item['name']]), None)
		
		if cookbook_entry == None:
			return "recipe contains recipe or ingredients that don't exist"
		elif cookbook_entry['type'] == 'ingredient':
			continue
		
		# recursively finds and adds ingredients from recipe
		temp: Union[str | Summary] = recursive_summary(cookbook_entry['required_items'])
		
		if type(temp) == str:
			return temp
		
		merge_required_item(result, temp, item['quantity'])
		
		# remove recipe from result array
		result = [x for x in result if x['name'] != item['name']]

	return result

# merges the required items of 2 different recipes 
def merge_required_item(arr1: List[RequiredItem], arr2: List[RequiredItem], quantity: int):
	for entry in arr2:
		item = None

		for x in arr1:
			if x['name'] == entry['name']:
				item = x
				break
		
		if item == None:
			item = entry.copy()
			item['quantity'] = entry['quantity'] * quantity
			arr1.append(item)
		else:
			item['quantity'] += entry['quantity'] * quantity


# =============================================================================
# ==== DO NOT TOUCH ===========================================================
# =============================================================================

if __name__ == '__main__':
	app.run(debug=True, port=8080)
