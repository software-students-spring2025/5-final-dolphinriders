# recommender_api/tests/test_recommend.py

import os
# Ensure environment variables so app.db can initialize without error
os.environ["MONGO_URI"] = "mongodb://localhost:27017"
os.environ["DB_NAME"] = "test_db"

import pytest
from app.recommend import filter as filter_recipes
from app.models import RecipeFilterParams

@pytest.fixture(autouse=True)
def stub_db(monkeypatch):
    # stub out external DB calls so filter logic is tested in isolation
    monkeypatch.setattr("app.recommend.get_recipes", lambda: [])
    monkeypatch.setattr("app.recommend.get_ingredients", lambda: [])

def make_params(**overrides):
    defaults = dict(
        sortBy='percent', timeCook=0, totalTime=0, prepTime=0,
        ingredientsUsed=[], haveSome=True
    )
    defaults.update(overrides)
    return RecipeFilterParams(**defaults)

def test_filter_empty():
    result = filter_recipes(make_params(), user_ingredients=[])
    assert result == []

def test_filter_by_ingredients_used(monkeypatch):
    recipes = [
        {"_id": "r1", "name": "One", "ingredients": [{"name": "egg"}]},
        {"_id": "r2", "name": "Two", "ingredients": [{"name": "flour"}]},
    ]
    monkeypatch.setattr("app.recommend.get_recipes", lambda: recipes)
    result = filter_recipes(make_params(ingredientsUsed=["egg"]), user_ingredients=["egg"])
    assert result == ["r1"]

def test_sort_and_filters(monkeypatch):
    # cookTime filter
    recipes1 = [
        {"_id": "r1", "name": "A", "ingredients": [], "cookTime": 5, "totalTime": 7, "prepTime": 2},
        {"_id": "r2", "name": "B", "ingredients": [], "cookTime": 15, "totalTime": 20, "prepTime": 5},
    ]
    monkeypatch.setattr("app.recommend.get_recipes", lambda: recipes1)
    assert filter_recipes(make_params(timeCook=10), []) == ["r1"]

    # alpha sort
    monkeypatch.setattr("app.recommend.get_recipes", lambda: recipes1)
    assert filter_recipes(make_params(sortBy='alpha'), []) == ["r1", "r2"]

    # price sort with haveSome
    recipes2 = [
        {"_id": "r1", "name": "One", "ingredients": [{"name": "x"}, {"name": "y"}]},
        {"_id": "r2", "name": "Two", "ingredients": [{"name": "x"}]},
    ]
    monkeypatch.setattr("app.recommend.get_recipes", lambda: recipes2)
    res = filter_recipes(make_params(sortBy='price', haveSome=True), ['x'])
    # fallback price sort is by ratio, so r1 (1/2) < r2 (1/1) yields ['r1','r2']
    assert res == ['r1', 'r2']
