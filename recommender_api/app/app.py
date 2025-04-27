# recommender_api/app/app.py

import os
from flask import Flask, request, jsonify, abort
import app.db as db
from app.models import RecipeFilterParams
from app.recommend import filter

app = Flask(__name__, static_folder='static')

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/recipes', methods=["GET"])
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
        user_data = db.get_user_ingredients(user_id)
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

@app.route('/recipes/<recipe_id>', methods=["GET"])
def get_recipe(recipe_id):
    recipe = db.get_recipe_by_id(recipe_id)
    if not recipe:
        abort(404, description="Recipe not found")
    return jsonify(recipe)

@app.route('/ingredients', methods=["GET"])
def get_all_ingredients():
    ingredients = db.get_ingredients()
    return jsonify(ingredients)

@app.route('/user/<user_id>/ingredients', methods=["GET"])
def get_user_available_ingredients(user_id):
    user_data = db.get_user_ingredients(user_id)
    if not user_data:
        abort(404, description="User not found")
    return jsonify(user_data)

@app.route('/user/<user_id>/ingredients', methods=["PUT"])
def update_user_available_ingredients(user_id):
    ingredients = request.json
    if not isinstance(ingredients, list):
        abort(400, description="Expected a list of ingredients")

    success = db.update_user_ingredients(user_id, ingredients)
    if not success:
        abort(500, description="Failed to update ingredients")

    return jsonify({"user_id": user_id, "ingredients": ingredients})

@app.route('/recipe/<recipe_id>/shopping-list', methods=["GET"])
def generate_shopping_list(recipe_id):
    user_id = request.args.get('user_id')

    recipe = db.get_recipe_by_id(recipe_id)
    if not recipe:
        abort(404, description="Recipe not found")

    user_ingredients = []
    if user_id:
        user_data = db.get_user_ingredients(user_id)
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