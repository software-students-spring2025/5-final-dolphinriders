import os
from pymongo import MongoClient
from dotenv import load_dotenv
from bson.objectid import ObjectId
from flask import current_app

load_dotenv()


def init_db(app):
    """
    Initialize MongoDB connection and attach the database handle to app.db.
    Expects 'MONGO_URI' and optional 'DB_NAME' in app.config or environment.
    """
    mongo_uri = app.config.get('MONGO_URI') or os.getenv('MONGO_URI', 'mongodb://localhost:27017/recipes')
    client = MongoClient(mongo_uri)

    # Attempt to pick up default database from URI, fallback to DB_NAME
    default_db = client.get_default_database()
    if default_db is not None:
        db = default_db
    else:
        db_name = app.config.get('DB_NAME') or os.getenv('DB_NAME', 'recipes')
        db = client[db_name]

    # Attach to Flask app
    app.db = db
    return db


# CRUD helpers using current_app.db

def get_recipes(filter_query=None, sort_by=None, limit=None):
    db = current_app.db
    query = filter_query or {}
    cursor = db.recipes.find(query)
    if sort_by:
        cursor = cursor.sort(sort_by)
    if limit:
        cursor = cursor.limit(limit)

    recipes = []
    for recipe in cursor:
        recipe['id'] = str(recipe.get('_id'))
        recipes.append(recipe)
    return recipes


def get_recipe_by_id(recipe_id):
    db = current_app.db
    try:
        doc = db.recipes.find_one({"_id": ObjectId(recipe_id)})
        if not doc:
            return None
        doc['id'] = str(doc.get('_id'))
        return doc
    except Exception:
        return None


def get_ingredients(filter_query=None):
    db = current_app.db
    query = filter_query or {}
    cursor = db.ingredients.find(query)

    ingredients = []
    for ing in cursor:
        ing['id'] = str(ing.get('_id'))
        ingredients.append(ing)
    return ingredients


def get_user_ingredients(user_id):
    db = current_app.db
    doc = db.user_ingredients.find_one({"user_id": user_id})
    if not doc:
        return None
    doc['id'] = str(doc.get('_id'))
    return doc


def update_user_ingredients(user_id, ingredients):
    db = current_app.db
    result = db.user_ingredients.update_one(
        {"user_id": user_id},
        {"$set": {"ingredients": ingredients}},
        upsert=True
    )
    return result.acknowledged


def add_recipe(recipe_data):
    db = current_app.db
    result = db.recipes.insert_one(recipe_data)
    return str(result.inserted_id)


def add_ingredient(ingredient_data):
    db = current_app.db
    result = db.ingredients.insert_one(ingredient_data)
    return str(result.inserted_id)
