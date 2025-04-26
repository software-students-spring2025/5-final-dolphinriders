# recommender_api/tests/test_recommend.py

import os, sys
import pytest
from flask import Flask

# Ensure project root is on PYTHONPATH for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.recommend import recommend_recipes

class DummyCollection:
    def __init__(self, docs):
        self._docs = docs
    def find(self, _filter=None):
        return self._docs

@pytest.fixture
def app():
    return Flask(__name__)

@pytest.fixture
def set_db(app):
    def _set(docs):
        # Attach dummy DB with recipes collection
        app.db = type('DB', (), {'recipes': DummyCollection(docs)})()
    return _set

@ pytest.mark.parametrize("inventory, preferences, docs, expected_names", [
    # True preference (must include)
    (
        ['egg', 'flour'], {'vegan': True},
        [
            {'name': 'VeganRecipe', 'ingredients': ['egg'],   'steps': [], 'tags': ['vegan']},
            {'name': 'NonVegan',    'ingredients': ['flour'], 'steps': [], 'tags': []}
        ],
        ['VeganRecipe']
    ),
    # False preference (must exclude)
    (
        ['milk'], {'gluten_free': False},
        [
            {'name': 'GFRecipe', 'ingredients': ['milk'], 'steps': [], 'tags': ['gluten_free']},
            {'name': 'Regular',  'ingredients': ['milk'], 'steps': [], 'tags': []}
        ],
        ['Regular']
    ),
])
def test_preference_filtering(app, set_db, inventory, preferences, docs, expected_names):
    set_db(docs)
    with app.app_context():
        results = recommend_recipes(inventory, preferences, top_n=5)
        names = [r['name'] for r in results]
        assert names == expected_names


def test_match_ratio_and_sorting(app, set_db):
    docs = [
        {'name': 'Z', 'ingredients': ['a', 'b'], 'steps': [], 'tags': []},
        {'name': 'A', 'ingredients': ['a'],      'steps': [], 'tags': []},
        {'name': 'B', 'ingredients': ['a'],      'steps': [], 'tags': []}
    ]
    set_db(docs)
    with app.app_context():
        results = recommend_recipes(['a'], {}, top_n=3)
        # Expected order: A, B (ratio=1.0, name asc), then Z (ratio=0.5)
        assert [r['name'] for r in results] == ['A', 'B', 'Z']
        assert [r['match_ratio'] for r in results] == [1.0, 1.0, 0.5]


def test_top_n_limit(app, set_db):
    docs = [
        {'name': 'One',   'ingredients': ['x'], 'steps': [], 'tags': []},
        {'name': 'Two',   'ingredients': ['x'], 'steps': [], 'tags': []},
        {'name': 'Three', 'ingredients': ['x'], 'steps': [], 'tags': []}
    ]
    set_db(docs)
    with app.app_context():
        results = recommend_recipes(['x'], {}, top_n=2)
        assert len(results) == 2


def test_empty_ingredients(app, set_db):
    docs = [
        {'name': 'EmptyRecipe', 'ingredients': [], 'steps': [], 'tags': []}
    ]
    set_db(docs)
    with app.app_context():
        results = recommend_recipes([], {}, top_n=1)
        # No ingredients => ratio is 0.0
        assert results[0]['match_ratio'] == 0.0
