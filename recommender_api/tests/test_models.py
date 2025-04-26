# recommender_api/tests/test_models.py

import sys
import os
from datetime import datetime, timedelta
import pytest

# Ensure the app package is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.models import (
    Ingredient,
    RecipeIngredient,
    Recipe,
    UserIngredients,
    RecipeFilterParams,
    ShoppingListItem,
    ShoppingList
)


def test_ingredient_defaults():
    ingr = Ingredient(name='Tomato')
    assert ingr.name == 'Tomato'
    assert ingr.quantity is None
    assert ingr.unit is None
    assert ingr.price_per_unit is None
    assert ingr.category is None


def test_recipeingredient_defaults():
    ri = RecipeIngredient(name='Salt')
    assert ri.name == 'Salt'
    assert ri.quantity is None
    assert ri.unit is None


def test_recipe_fields():
    # Mandatory fields: name, ingredients, instructions, cookTime, prepTime
    ri = RecipeIngredient(name='Rice', quantity=1.0, unit='cup')
    recipe = Recipe(
        name='Boiled Rice',
        ingredients=[ri],
        instructions=['Boil water', 'Add rice'],
        cookTime=10,
        prepTime=5
    )
    assert recipe.name == 'Boiled Rice'
    assert isinstance(recipe.ingredients, list) and recipe.ingredients[0] is ri
    assert recipe.instructions == ['Boil water', 'Add rice']
    assert recipe.cookTime == 10
    assert recipe.prepTime == 5
    # Optional fields default to None
    assert recipe.totalTime is None
    assert recipe.servings is None
    assert recipe.cuisine is None
    assert recipe.tags is None
    assert recipe.image_url is None


def test_useringredients_last_updated():
    before = datetime.now() - timedelta(seconds=1)
    ui = UserIngredients(user_id='u1', ingredients=['egg'])
    after = datetime.now() + timedelta(seconds=1)
    # last_updated should be between before and after
    assert isinstance(ui.last_updated, datetime)
    assert before <= ui.last_updated <= after
    assert ui.user_id == 'u1'
    assert ui.ingredients == ['egg']


def test_recipefilterparams_defaults():
    params = RecipeFilterParams()
    assert params.sortBy == 'percent'
    assert params.timeCook == 0
    assert params.totalTime == 0
    assert params.prepTime == 0
    assert params.ready is False
    assert isinstance(params.ingredientsUsed, list) and params.ingredientsUsed == []
    assert params.haveSome is True


def test_shoppinglistitem_defaults():
    item = ShoppingListItem(ingredient='Milk')
    assert item.ingredient == 'Milk'
    assert item.quantity is None
    assert item.unit is None
    assert item.estimated_price is None


def test_shoppinglist_fields():
    item1 = ShoppingListItem(ingredient='Sugar', quantity=2, unit='tbsp', estimated_price=0.5)
    sl = ShoppingList(
        recipe_id='r1',
        recipe_name='Tea',
        missing_ingredients=[item1],
        total_estimated_price=0.5
    )
    assert sl.recipe_id == 'r1'
    assert sl.recipe_name == 'Tea'
    assert isinstance(sl.missing_ingredients, list) and sl.missing_ingredients[0] is item1
    assert sl.total_estimated_price == 0.5