import os
from flask import Flask, request, jsonify, abort
from app.db import init_db, get_user_ingredients, get_recipe_by_id, get_ingredients, update_user_ingredients
from app.models import RecipeFilterParams
from app.recommend import recommend_recipes

def create_app():
    # Initialize Flask app and MongoDB
    app = Flask(__name__, static_folder='static')
    app.config['MONGO_URI'] = os.getenv('MONGO_URI', 'mongodb://localhost:27017/recipes')
    app.config['DB_NAME']  = os.getenv('DB_NAME', 'recipes')
    init_db(app)

    @app.route('/')
    def root():
        return jsonify({"message": "Welcome to the Recipe Recommender API"})

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

        user_ings = []
        if user_id:
            user_data = get_user_ingredients(user_id)
            if user_data:
                user_ings = user_data.get('ingredients', [])

        params = RecipeFilterParams(
            sortBy=sort_by,
            timeCook=time_cook,
            totalTime=total_time,
            prepTime=prep_time,
            ready=ready,
            ingredientsUsed=ingredients_used,
            haveSome=have_some
        )

        # recommend_recipes takes inventory list, preferences dict, and params
        recipes = recommend_recipes(user_ings, {}, params)
        return jsonify(recipes)

    @app.route('/recipes/<recipe_id>', methods=["GET"])
    def get_recipe(recipe_id):
        recipe = get_recipe_by_id(recipe_id)
        if not recipe:
            abort(404, description="Recipe not found")
        return jsonify(recipe)

    @app.route('/ingredients', methods=["GET"])
    def all_ingredients():
        return jsonify(get_ingredients())

    @app.route('/user/<user_id>/ingredients', methods=["GET"])
    def user_ingredients(user_id):
        data = get_user_ingredients(user_id)
        if not data:
            abort(404, description="User not found")
        return jsonify(data)

    @app.route('/user/<user_id>/ingredients', methods=["PUT"])
    def update_ingredients(user_id):
        ingredients = request.json
        if not isinstance(ingredients, list):
            abort(400, description="Expected a list of ingredients")
        success = update_user_ingredients(user_id, ingredients)
        if not success:
            abort(500, description="Failed to update ingredients")
        return jsonify({"user_id": user_id, "ingredients": ingredients})

    @app.route('/recipe/<recipe_id>/shopping-list', methods=["GET"])
    def shopping_list(recipe_id):
        user_id = request.args.get('user_id')
        recipe = get_recipe_by_id(recipe_id)
        if not recipe:
            abort(404, description="Recipe not found")
        have = []
        if user_id:
            ud = get_user_ingredients(user_id)
            if ud:
                have = ud.get('ingredients', [])
        missing = []
        for ing in recipe.get('ingredients', []):
            if ing['name'] not in have:
                missing.append({
                    'ingredient': ing['name'],
                    'quantity': ing.get('quantity'),
                    'unit': ing.get('unit'),
                    'estimated_price': None
                })
        return jsonify({
            'recipe_id': recipe_id,
            'recipe_name': recipe.get('name'),
            'missing_ingredients': missing,
            'total_estimated_price': None
        })

    return app


if __name__ == "__main__":
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)