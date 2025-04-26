# recommender_api/tests/test_app.py

import os, sys
import pytest

# Ensure project root is on PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.app import app

@pytest.fixture
def client(monkeypatch):
    # Stub database layer methods
    monkeypatch.setattr('app.app.db.get_user_ingredients', lambda uid: {'ingredients': ['salt']})
    monkeypatch.setattr('app.app.db.get_recipe_by_id', lambda rid: {
        'name': 'R', 'ingredients': [{'name': 'salt', 'quantity': 1, 'unit': 'tsp'}]
    })
    monkeypatch.setattr('app.app.db.get_ingredients', lambda: ['salt', 'pepper'])
    monkeypatch.setattr('app.app.db.update_user_ingredients', lambda uid, ings: True)
    # Stub recommendation logic
    monkeypatch.setattr('app.app.recommend_recipes', lambda inv, prefs, params: ['r1', 'r2'])

    app.config['TESTING'] = True
    return app.test_client()

# 1. Root endpoint
def test_root(client):
    rv = client.get('/')
    assert rv.status_code == 200
    assert rv.get_json() == {"message": "Welcome to the Recipe Recommender API"}

# 2. GET /recipes without user_id
def test_get_all_recipes_no_user(client):
    rv = client.get(
        '/recipes?sortBy=alpha&timeCook=10&totalTime=20&prepTime=5'
        '&ready=true&ingredientsUsed=ing1&haveSome=false'
    )
    assert rv.status_code == 200
    assert rv.get_json() == ['r1', 'r2']

# 3. GET /recipes with user_id
def test_get_all_recipes_with_user(client):
    rv = client.get('/recipes?user_id=123')
    assert rv.status_code == 200
    assert rv.get_json() == ['r1', 'r2']

# 4. GET /recipes/<id>
def test_get_recipe_success(monkeypatch, client):
    monkeypatch.setattr('app.app.db.get_recipe_by_id', lambda rid: {'id': rid, 'name': 'Test'})
    rv = client.get('/recipes/abc')
    assert rv.status_code == 200
    assert rv.get_json() == {'id': 'abc', 'name': 'Test'}


def test_get_recipe_not_found(monkeypatch, client):
    monkeypatch.setattr('app.app.db.get_recipe_by_id', lambda rid: None)
    rv = client.get('/recipes/notfound')
    assert rv.status_code == 404

# 5. GET /ingredients
def test_get_all_ingredients(client):
    rv = client.get('/ingredients')
    assert rv.status_code == 200
    assert rv.get_json() == ['salt', 'pepper']

# 6. GET /user/<id>/ingredients
def test_get_user_ingredients_success(client):
    rv = client.get('/user/u1/ingredients')
    assert rv.status_code == 200
    assert rv.get_json() == {'ingredients': ['salt']}


def test_get_user_ingredients_not_found(monkeypatch, client):
    monkeypatch.setattr('app.app.db.get_user_ingredients', lambda uid: None)
    rv = client.get('/user/u1/ingredients')
    assert rv.status_code == 404

# 7. PUT /user/<id>/ingredients
def test_update_user_ingredients_success(client):
    rv = client.put('/user/u1/ingredients', json=['a', 'b'])
    assert rv.status_code == 200
    assert rv.get_json() == {'user_id': 'u1', 'ingredients': ['a', 'b']}


def test_update_user_ingredients_bad_request(client):
    rv = client.put('/user/u1/ingredients', data='notalist', content_type='application/json')
    assert rv.status_code == 400


def test_update_user_ingredients_failure(monkeypatch, client):
    monkeypatch.setattr('app.app.db.update_user_ingredients', lambda uid, ings: False)
    rv = client.put('/user/u1/ingredients', json=['x'])
    assert rv.status_code == 500

# 8. GET /recipe/<id>/shopping-list
def test_generate_shopping_list_success(client):
    rv = client.get('/recipe/123/shopping-list?user_id=u1')
    assert rv.status_code == 200
    data = rv.get_json()
    assert data['recipe_id'] == '123'
    assert data['recipe_name'] == 'R'
    assert data['missing_ingredients'] == []


def test_generate_shopping_list_not_found(monkeypatch, client):
    monkeypatch.setattr('app.app.db.get_recipe_by_id', lambda rid: None)
    rv = client.get('/recipe/999/shopping-list')
    assert rv.status_code == 404