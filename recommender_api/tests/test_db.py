# tests/test_db.py
import os
import pytest
import mongomock
import importlib
from bson.objectid import ObjectId

@pytest.fixture(autouse=True)
def fake_db_module(monkeypatch):
    # Set dummy env vars
    monkeypatch.setenv("MONGO_URI", "mongodb://localhost/test")
    monkeypatch.setenv("DB_NAME", "test_db")
    # Patch pymongo.MongoClient to use mongomock
    import pymongo
    monkeypatch.setattr(pymongo, 'MongoClient', lambda uri=None, *args, **kwargs: mongomock.MongoClient())
    # Reload the db module to pick up patched MongoClient
    import app.db as db_module
    importlib.reload(db_module)
    return db_module


def test_get_recipes_and_ingredients(fake_db_module):
    db = fake_db_module
    # Seed recipes and ingredients
    db.recipe_collection.insert_many([
        {"name": "R1", "ingredients": [{"name": "a"}]},
        {"name": "R2", "ingredients": [{"name": "b"}]},
    ])
    db.ingredients_collection.insert_many([
        {"name": "a", "price_per_unit": 1.0},
        {"name": "b", "price_per_unit": 2.0},
    ])

    recs = db.get_recipes()
    assert isinstance(recs, list)
    assert len(recs) == 2
    assert all(isinstance(r["_id"], str) for r in recs)

    ings = db.get_ingredients()
    assert isinstance(ings, list)
    assert any(i["name"] == "a" for i in ings)
    assert all(isinstance(i["_id"], str) for i in ings)


def test_get_recipe_by_id(fake_db_module):
    db = fake_db_module
    oid = db.recipe_collection.insert_one({"name": "Solo"}).inserted_id
    rec = db.get_recipe_by_id(str(oid))
    assert rec["_id"] == str(oid)
    assert rec["name"] == "Solo"
    # Invalid ID returns None
    assert db.get_recipe_by_id("invalid") is None


def test_user_ingredients_and_update(fake_db_module):
    db = fake_db_module
    db.user_ingredients_collection.insert_one({"user_id": "u1", "ingredients": ["a"]})
    u = db.get_user_ingredients("u1")
    assert u["ingredients"] == ["a"]

    ok = db.update_user_ingredients("u1", ["b"])
    assert ok
    u2 = db.get_user_ingredients("u1")
    assert u2["ingredients"] == ["b"]

    # Upsert new user
    ok2 = db.update_user_ingredients("new_user", ["x"])
    assert ok2
    u3 = db.get_user_ingredients("new_user")
    assert u3["ingredients"] == ["x"]


def test_add_recipe_and_ingredient(fake_db_module):
    db = fake_db_module
    new_id = db.add_recipe({"name": "Added"})
    assert isinstance(new_id, str)
    found = db.recipe_collection.find_one({"_id": ObjectId(new_id)})
    assert found and found["name"] == "Added"

    ing_id = db.add_ingredient({"name": "NewIng"})
    assert isinstance(ing_id, str)
    found_ing = db.ingredients_collection.find_one({"_id": ObjectId(ing_id)})
    assert found_ing and found_ing["name"] == "NewIng"
