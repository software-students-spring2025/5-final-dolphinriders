# recommender_api/tests/test_app.py
import os, sys
# Ensure correct env and use mongomock before imports
os.environ.setdefault('MONGO_URI', 'mongodb://localhost:27017/recipes')
os.environ.setdefault('MONGO_DB', 'recipes')
import pymongo, mongomock
pymongo.MongoClient = mongomock.MongoClient
# Make 'app' package importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app.app import app as flask_app

@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    return flask_app.test_client()

# Root endpoint
def test_root(client):
    rv = client.get('/')
    assert rv.status_code == 200
    assert rv.get_json() == {'message': 'Welcome to the Recipe Recommender API'}

# GET /recipes without user_id
def test_get_all_recipes_no_user(monkeypatch, client):
    monkeypatch.setattr('app.app.filter', lambda p, ui: ['r1', 'r2'])
    rv = client.get(
        '/recipes?sortBy=alpha&timeCook=10&totalTime=20&prepTime=5'
        '&ready=true&ingredientsUsed=ing1&haveSome=false'
    )
    assert rv.status_code == 200
    assert rv.get_json() == ['r1', 'r2']

# GET /recipes with user_id
def test_get_all_recipes_with_user(monkeypatch, client):
    monkeypatch.setattr('app.db.get_user_ingredients', lambda uid: {'ingredients': ['salt']})
    monkeypatch.setattr('app.app.filter', lambda p, ui: ['r3'])
    rv = client.get('/recipes?user_id=123')
    assert rv.status_code == 200
    assert rv.get_json() == ['r3']

# GET /recipes/<id> success
def test_get_recipe_success(monkeypatch, client):
    monkeypatch.setattr('app.db.get_recipe_by_id', lambda rid: {'id': rid, 'name': 'Test'})
    rv = client.get('/recipes/abc')
    assert rv.status_code == 200
    assert rv.get_json() == {'id': 'abc', 'name': 'Test'}

# GET /recipes/<id> not found
def test_get_recipe_not_found(monkeypatch, client):
    monkeypatch.setattr('app.db.get_recipe_by_id', lambda rid: None)
    rv = client.get('/recipes/xxx')
    assert rv.status_code == 404

# GET /ingredients
def test_get_all_ingredients(monkeypatch, client):
    monkeypatch.setattr('app.db.get_ingredients', lambda: ['salt', 'pepper'])
    rv = client.get('/ingredients')
    assert rv.status_code == 200
    assert rv.get_json() == ['salt', 'pepper']

# GET /user/<id>/ingredients success
def test_get_user_ingredients_success(monkeypatch, client):
    monkeypatch.setattr('app.db.get_user_ingredients', lambda uid: {'ingredients': ['ing']})
    rv = client.get('/user/u1/ingredients')
    assert rv.status_code == 200
    assert rv.get_json() == {'ingredients': ['ing']}

# GET /user/<id>/ingredients not found
def test_get_user_ingredients_not_found(monkeypatch, client):
    monkeypatch.setattr('app.db.get_user_ingredients', lambda uid: None)
    rv = client.get('/user/u1/ingredients')
    assert rv.status_code == 404

# PUT /user/<id>/ingredients success
def test_update_user_ingredients_success(monkeypatch, client):
    monkeypatch.setattr('app.db.update_user_ingredients', lambda uid, ings: True)
    rv = client.put('/user/u1/ingredients', json=['a','b'])
    assert rv.status_code == 200
    assert rv.get_json() == {'user_id': 'u1', 'ingredients': ['a','b']}

# PUT /user/<id>/ingredients bad request
def test_update_user_ingredients_bad_request(client):
    rv = client.put('/user/u1/ingredients', data='notalist', content_type='application/json')
    assert rv.status_code == 400

# PUT /user/<id>/ingredients failure
def test_update_user_ingredients_failure(monkeypatch, client):
    monkeypatch.setattr('app.db.update_user_ingredients', lambda uid, ings: False)
    rv = client.put('/user/u1/ingredients', json=['x'])
    assert rv.status_code == 500

# GET /recipe/<id>/shopping-list success
def test_generate_shopping_list_success(monkeypatch, client):
    monkeypatch.setattr('app.db.get_recipe_by_id', lambda rid: {
        'name': 'R', 'ingredients': [{'name':'salt','quantity':1,'unit':'tsp'}]
    })
    monkeypatch.setattr('app.db.get_user_ingredients', lambda uid: {'ingredients':['salt']})
    rv = client.get('/recipe/123/shopping-list?user_id=u1')
    assert rv.status_code == 200
    data = rv.get_json()
    assert data['recipe_id'] == '123'
    assert data['recipe_name'] == 'R'
    assert data['missing_ingredients'] == []

# GET /recipe/<id>/shopping-list not found
def test_generate_shopping_list_not_found(monkeypatch, client):
    monkeypatch.setattr('app.db.get_recipe_by_id', lambda rid: None)
    rv = client.get('/recipe/999/shopping-list')
    assert rv.status_code == 404 