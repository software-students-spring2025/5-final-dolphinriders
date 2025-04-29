# recommender_api/tests/test_app.py

import os
# Ensure env vars so app.db can initialize without error
os.environ["MONGO_URI"] = "mongodb://localhost:27017"
os.environ["DB_NAME"] = "test_db"

import pytest
from app.app import create_app
import app.db as db_module
import app.recommend as recommend_module  # for patching the recommend.filter function

@pytest.fixture
def client():
    app = create_app()
    app.testing = True
    return app.test_client()

# ---- GET /recipes ----

def test_get_all_recipes_default_no_user(monkeypatch, client):
    dummy = [{"id": "1", "name": "Test Pancakes"}]
    # patch the filter function in app.recommend
    monkeypatch.setattr(recommend_module, 'filter', lambda params, user_ing: dummy)
    resp = client.get('/recipes')
    assert resp.status_code == 200
    assert resp.is_json
    assert resp.get_json() == dummy

# ---- GET /recipes/<id> ----

def test_get_recipe_found(monkeypatch, client):
    recipe = {"id": "42", "name": "Salad"}
    monkeypatch.setattr(db_module, 'get_recipe_by_id', lambda rid: recipe)
    resp = client.get('/recipes/42')
    assert resp.status_code == 200
    assert resp.get_json() == recipe


def test_get_recipe_not_found(monkeypatch, client):
    monkeypatch.setattr(db_module, 'get_recipe_by_id', lambda rid: None)
    resp = client.get('/recipes/999')
    assert resp.status_code == 404
    # since app returns HTML on abort, check raw body
    assert b"Recipe not found" in resp.data

# ---- GET /ingredients ----

def test_get_all_ingredients(monkeypatch, client):
    ingr = ["flour", "egg", "milk"]
    monkeypatch.setattr(db_module, 'get_ingredients', lambda: ingr)
    resp = client.get('/ingredients')
    assert resp.status_code == 200
    assert resp.get_json() == ingr

# ---- GET /user/<id>/ingredients ----

def test_get_user_ingredients_found(monkeypatch, client):
    user_data = {"user_id": "u1", "ingredients": ["egg"]}
    monkeypatch.setattr(db_module, 'get_user_ingredients', lambda uid: user_data)
    resp = client.get('/user/u1/ingredients')
    assert resp.status_code == 200
    assert resp.get_json() == user_data


def test_get_user_ingredients_not_found(monkeypatch, client):
    monkeypatch.setattr(db_module, 'get_user_ingredients', lambda uid: None)
    resp = client.get('/user/u2/ingredients')
    assert resp.status_code == 404
    assert b"User not found" in resp.data

# ---- PUT /user/<id>/ingredients ----

def test_update_user_ingredients_success(monkeypatch, client):
    monkeypatch.setattr(db_module, 'update_user_ingredients', lambda uid, lst: True)
    new_list = ["flour", "sugar"]
    resp = client.put('/user/u3/ingredients', json=new_list)
    assert resp.status_code == 200
    assert resp.get_json() == {"user_id": "u3", "ingredients": new_list}


def test_update_user_ingredients_bad_payload(client):
    resp = client.put('/user/u3/ingredients', json={"foo": "bar"})
    assert resp.status_code == 400
    assert b"Expected a list of ingredients" in resp.data


def test_update_user_ingredients_failure(monkeypatch, client):
    monkeypatch.setattr(db_module, 'update_user_ingredients', lambda uid, lst: False)
    resp = client.put('/user/u4/ingredients', json=["a"])
    assert resp.status_code == 500
    assert b"Failed to update ingredients" in resp.data

# ---- GET /recipe/<id>/shopping-list ----

def test_generate_shopping_list_success(monkeypatch, client):
    recipe = {
        "id": "r1", "name": "Pasta",
        "ingredients": [
            {"name": "egg", "quantity": 1, "unit": "each"},
            {"name": "flour", "quantity": 2, "unit": "cup"}
        ]
    }
    monkeypatch.setattr(db_module, 'get_recipe_by_id', lambda rid: recipe)
    monkeypatch.setattr(db_module, 'get_user_ingredients', lambda uid: {"ingredients": ["egg"]})
    resp = client.get('/recipe/r1/shopping-list?user_id=u5')
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['recipe_id'] == 'r1'
    assert any(item['ingredient'] == 'flour' for item in data['missing_ingredients'])


def test_generate_shopping_list_recipe_not_found(monkeypatch, client):
    monkeypatch.setattr(db_module, 'get_recipe_by_id', lambda rid: None)
    resp = client.get('/recipe/xxx/shopping-list')
    assert resp.status_code == 404
    # HTML error page includes “Recipe not found”
    assert b"Recipe not found" in resp.data