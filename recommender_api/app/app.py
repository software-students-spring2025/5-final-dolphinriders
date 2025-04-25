
from flask import Flask, request, jsonify, abort
import os

from app.db import (
    get_recipes, 
    get_recipe_by_id, 
    get_ingredients, 
    get_user_ingredients,
    update_user_ingredients
)
from app.models import RecipeFilterParams

app = Flask(__name__, static_folder='static')

@app.route('/')
def root():
    return jsonify({"message": "Welcome to the Recipe Recommender API"})

@app.route('/recipes', methods=['GET'])
def get_all_recipes():
    sort_by = request.args.get('sortBy', 'percent')
    time_cook = int(request.args.get('timeCook', 0))
    total_time = int(request.args.get('totalTime', 0))
    prep_time = int(request.args.get('prepTime', 0))
    ready = request.args.get('ready', 'false').lower() == 'true'
    ingredients_used = request.args.getlist('ingredientsUsed')
    have_some = request.args.get('haveSome', 'true').lower() == 'true'
    user_id = request.args.get('user_id')
    
    user_ingredients = []
    if user_id:
        user_data = get_user_ingredients(user_id)
        if user_data:
            user_ingredients = user_data.get("ingredients", [])
    
    params = RecipeFilterParams(
        sortBy=sort_by,
        timeCook=time_cook,
        totalTime=total_time,
        prepTime=prep_time,
        ready=ready,
        ingredientsUsed=ingredients_used,
        haveSome=have_some
    )
    
    recipes = filter(params, user_ingredients)
    return jsonify(recipes)

@app.route('/recipes/<recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    recipe = get_recipe_by_id(recipe_id)
    if not recipe:
        abort(404, description="Recipe not found")
    return jsonify(recipe)

@app.route('/ingredients', methods=['GET'])
def get_all_ingredients():
    ingredients = get_ingredients()
    return jsonify(ingredients)

@app.route('/user/<user_id>/ingredients', methods=['GET'])
def get_user_available_ingredients(user_id):
    user_data = get_user_ingredients(user_id)
    if not user_data:
        abort(404, description="User not found")
    return jsonify(user_data)

@app.route('/user/<user_id>/ingredients', methods=['PUT'])
def update_user_available_ingredients(user_id):
    ingredients = request.json
    if not isinstance(ingredients, list):
        abort(400, description="Expected a list of ingredients")
    
    success = update_user_ingredients(user_id, ingredients)
    if not success:
        abort(500, description="Failed to update ingredients")
    
    return jsonify({"user_id": user_id, "ingredients": ingredients})

@app.route('/recipe/<recipe_id>/shopping-list', methods=['GET'])
def generate_shopping_list(recipe_id):
    user_id = request.args.get('user_id')
    
    recipe = get_recipe_by_id(recipe_id)
    if not recipe:
        abort(404, description="Recipe not found")
    
    user_ingredients = []
    if user_id:
        user_data = get_user_ingredients(user_id)
        if user_data:
            user_ingredients = user_data.get("ingredients", [])
    
    missing_ingredients = []
    for ingredient in recipe["ingredients"]:
        if ingredient["name"] not in user_ingredients:
            missing_ingredients.append({
                "ingredient": ingredient["name"],
                "quantity": ingredient.get("quantity"),
                "unit": ingredient.get("unit"),
                "estimated_price": None
            })
    
    return jsonify({
        "recipe_id": recipe_id,
        "recipe_name": recipe["name"],
        "missing_ingredients": missing_ingredients,
        "total_estimated_price": None
    })

def create_app():
    return app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)


from app.db import recipe_collection, ingredients_collection, get_recipes, get_ingredients
from app.models import RecipeFilterParams

def filter(sortBy,timeCook,totalTime,prepTime,ready,ingredientsUsed,haveSome):
    ingredientsList = ingredients_collection.get()
    recipeList = recipe_collection.get()
    potentialRecipeIDs = []
    potRecIngredientRatio = {} # structure is _id:{"total":0,"present":0,"ratio":0}

    # DONE add filtering for *specific ingredients*, cook time

    # TOOO add price finding feature

    # DONE mod filter to inclode 0% recipes
    for idnum,recipe in recipeList.items:
        ingredientNames = []
        for ingredient in recipe["ingredients"]:
            ingredientNames.append(recipe["ingredients"]["name"])
        if (haveSome == False):
                potentialRecipeIDs.append(idnum)
                potRecIngredientRatio.append(idnum:{"total":ingredientNames.size,"present":0,"ratio":0})
        for ingredient in ingredientsList:
            if ingredient["name"] in ingredientNames:
                if idnum not in potentialRecipeIDs:
                    potentialRecipeIDs.append(idnum)
                    potRecIngredientRatio.append(idnum:{"total":ingredientNames.size,"present":1,"ratio":0})
                    potRecIngredientRatio[idnum]["ratio"] = potRecIngredientRatio[idnum]["present"]/potRecIngredientRatio[idnum]["total"]
                else:
                    potRecIngredientRatio[idnum]["present"] = potRecIngredientRatio[idnum]["present"]+1
                    potRecIngredientRatio[idnum]["ratio"] = potRecIngredientRatio[idnum]["present"]/potRecIngredientRatio[idnum]["total"]
        if (ingredientsUsed != []):
            allow = False
            for ingredient in ingredientsUsed:
                if ingredient in ingredientNames:
                    allow = True
            if (allow == False):
                potentialRecipeIDs.remove(idnum)
        if (timeCook>0):
            if (recipe["cookTime"]>timeCook):
                potentialRecipeIDs.remove(idnum)
        if (totalTime>0):
            if (recipe["cookTime"]>totalTime):
                potentialRecipeIDs.remove(idnum)
        if (prepTime>0):
            if (recipe["cookTime"]>prepTime):
                potentialRecipeIDs.remove(idnum)


    # potentialRecipeIDs now full of all recipes with at least one present ingredient, and potRecIngredientRatio is a dict of dicts in correct format
    def sortAlpha(n):
        return recipeList[n]["name"]
    def sortPercent(n):
        return potRecIngredientRatio[n]["ratio"]
    def sortPrice(n):



    if (sortBy == "alpha"):
        potentialRecipeIDs.sort(key=sortAlpha)
    elif (sortBy == "price"):
        potentialRecipeIDs.sort(key=sortPrice)
    else:
        potentialRecipeIDs.sort(key=sortPercent)

    # TODO sort dict
    # TODO: sort by price, alphabetical, percent ingredients

    # this code was written by a human goddamn being with a soul and thoughts.

    return potentialRecipeIDs
