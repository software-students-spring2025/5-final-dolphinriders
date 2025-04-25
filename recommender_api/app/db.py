import os
from pymongo import MongoClient
from dotenv import load_dotenv
from bson.objectid import ObjectId

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

recipe_collection = db.recipes
ingredients_collection = db.ingredients
user_ingredients_collection = db.user_ingredients

def get_recipes(filter_query=None, sort_by=None, limit=None):
    """
    Retrieve recipes from MongoDB with optional filtering, sorting, and limiting
    """
    query = filter_query or {}
    cursor = recipe_collection.find(query)
    
    if sort_by:
        cursor = cursor.sort(sort_by)
        
    if limit:
        cursor = cursor.limit(limit)
    
    recipes = []
    for recipe in cursor:
        recipe['_id'] = str(recipe['_id'])
        recipes.append(recipe)
    
    return recipes

def get_recipe_by_id(recipe_id):
    """
    Retrieve a single recipe by its ID
    """
    try:
        recipe = recipe_collection.find_one({"_id": ObjectId(recipe_id)})
        if recipe:
            recipe['_id'] = str(recipe['_id'])
        return recipe
    except:
        return None

def get_ingredients(filter_query=None):
    """
    Retrieve ingredients from MongoDB with optional filtering
    """
    query = filter_query or {}
    cursor = ingredients_collection.find(query)
    
    ingredients = []
    for ingredient in cursor:
        ingredient['_id'] = str(ingredient['_id'])
        ingredients.append(ingredient)
    
    return ingredients

def get_user_ingredients(user_id):
    """
    Retrieve ingredients that a user has on hand
    """
    user_ingredients = user_ingredients_collection.find_one({"user_id": user_id})
    if user_ingredients:
        user_ingredients['_id'] = str(user_ingredients['_id'])
    return user_ingredients

def update_user_ingredients(user_id, ingredients):
    """
    Update or insert a user's ingredients
    """
    result = user_ingredients_collection.update_one(
        {"user_id": user_id},
        {"$set": {"ingredients": ingredients}},
        upsert=True
    )
    return result.acknowledged

def add_recipe(recipe_data):
    """
    Add a new recipe to the database
    """
    result = recipe_collection.insert_one(recipe_data)
    return str(result.inserted_id)

def add_ingredient(ingredient_data):
    """
    Add a new ingredient to the database
    """
    result = ingredients_collection.insert_one(ingredient_data)
    return str(result.inserted_id)