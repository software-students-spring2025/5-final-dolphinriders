from flask import Flask, request, render_template, redirect, url_for
import requests
import os

app = Flask(__name__)

# Get the recipe service URL from environment variables
RECIPE_SERVICE_URL = os.environ.get('RECIPE_SERVICE_URL', 'http://localhost:3000')

@app.route('/')
def index():
    # Get user ID from query params (in a real app, this would come from auth)
    user_id = request.args.get('user_id')
    if not user_id:
        return "Please provide a user_id parameter", 400
    
    # Get cheapest recipes from the recipe service
    try:
        response = requests.get(
            f"{RECIPE_SERVICE_URL}/recipes",
            params={
                'user_id': user_id,
                'sortBy': 'price',
                'haveSome': 'true'
            }
        )
        response.raise_for_status()
        recipes = response.json()
    except requests.exceptions.RequestException as e:
        return f"Error connecting to recipe service: {str(e)}", 500
    
    return render_template('index.html', recipes=recipes, user_id=user_id)

@app.route('/generate-list', methods=['POST'])
def generate_list():
    user_id = request.form.get('user_id')
    recipe_id = request.form.get('recipe_id')
    
    if not user_id or not recipe_id:
        return "Missing user_id or recipe_id", 400
    
    # Get shopping list from recipe service
    try:
        response = requests.get(
            f"{RECIPE_SERVICE_URL}/recipe/{recipe_id}/shopping-list",
            params={'user_id': user_id}
        )
        response.raise_for_status()
        shopping_list = response.json()
    except requests.exceptions.RequestException as e:
        return f"Error generating shopping list: {str(e)}", 500
    
    return render_template('shopping_list.html', shopping_list=shopping_list)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)