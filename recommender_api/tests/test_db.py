# recommender_api/tests/test_db.py

import os
import sys
import pytest
import mongomock
from bson.objectid import ObjectId

# Ensure app package is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import app.db as db

@pytest.fixture(autouse=True)
def mock_mongo(monkeypatch):
    # Setup a fake MongoDB in-memory instance
    fake_client = mongomock.MongoClient()
    fake_db = fake_client['testdb']
    # Monkey-patch client and db
    monkeypatch.setattr(db, 'client', fake_client)
    monkeypatch.setattr(db, 'db', fake_db)
    # Patch collections
    monkeypatch.setattr(db, 'recipe_collection', fake_db.recipes)
    monkeypatch.setattr(db, 'ingredients_collection', fake_db.ingredients)
    monkeypatch.setattr(db, 'user_ingredients_collection', fake_db.user_ingredients)

def test_add_and_get_recipe():
    # Add a recipe and retrieve it
    rid = db.add_recipe({'name': 'Pancake', 'ingredients': [], 'steps': []})
    assert isinstance(rid, str)
    doc = db.get_recipe_by_id(rid)
    assert doc['name'] == 'Pancake'
    assert doc['_id'] == rid

def test_get_recipes_filter_sort_limit():
    # Insert multiple recipes
    db.recipe_collection.insert_one({'name': 'B'})
    db.recipe_collection.insert_one({'name': 'A'})
    # No filter
    all_recipes = db.get_recipes()
    assert len(all_recipes) == 2
    # Sort by name ascending, limit to 1
    sorted_limited = db.get_recipes(sort_by='name', limit=1)
    assert len(sorted_limited) == 1
    assert sorted_limited[0]['name'] == 'A'

def test_get_recipe_by_id_invalid():
    # Invalid ObjectId format
    assert db.get_recipe_by_id('notanid') is None
    # Non-existent but valid id
    valid_but_missing = ObjectId()
    assert db.get_recipe_by_id(str(valid_but_missing)) is None

def test_get_ingredients():
    # Insert ingredients
    db.add_ingredient({'name': 'salt'})
    db.add_ingredient({'name': 'pepper'})
    ings = db.get_ingredients()
    names = {i['name'] for i in ings}
    assert names == {'salt', 'pepper'}

def test_get_ingredients_with_filter():
    # Insert ingredients
    db.add_ingredient({'name': 'apple', 'type': 'fruit'})
    db.add_ingredient({'name': 'beef',  'type': 'meat'})
    fruits = db.get_ingredients(filter_query={'type': 'fruit'})
    assert len(fruits) == 1 and fruits[0]['name'] == 'apple'

def test_user_ingredients_crud():
    # Initially none
    assert db.get_user_ingredients('u1') is None
    # Upsert new
    ok = db.update_user_ingredients('u1', ['egg','flour'])
    assert ok is True
    data = db.get_user_ingredients('u1')
    assert data['user_id'] == 'u1'
    assert data['ingredients'] == ['egg','flour']
    # Update existing
    ok2 = db.update_user_ingredients('u1', ['milk'])
    assert ok2 is True
    data2 = db.get_user_ingredients('u1')
    assert data2['ingredients'] == ['milk']

def test_add_and_retrieve_ingredient_id():
    iid = db.add_ingredient({'name': 'tomato'})
    assert isinstance(iid, str)
    # verify stored doc has that id
    found = list(db.ingredients_collection.find({'_id': ObjectId(iid)}))
    assert len(found) == 1