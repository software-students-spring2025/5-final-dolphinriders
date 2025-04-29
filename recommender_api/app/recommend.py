# recommender_api/app/recommend.py

from typing import List
from app.db import get_recipes, get_ingredients
from app.models import RecipeFilterParams

def filter(params: RecipeFilterParams, user_ingredients: List[str]) -> List[str]:
    """
    Return a list of recipe IDs matching the filter params and
    sorted according to params.sortBy (
      'percent' (default), 'alpha', or 'price' ).
    """
    # 1) Unpack filter params
    sortBy        = params.sortBy
    timeCook      = params.timeCook
    totalTime     = params.totalTime
    prepTime      = params.prepTime
    ingredientsUsed = params.ingredientsUsed
    haveSome      = params.haveSome

    # 2) Fetch all data
    recipes    = get_recipes()     # list of dicts, each with '_id', 'name', 'ingredients', etc.
    ingredients = get_ingredients()  # list of dicts, each with 'name', maybe 'price_per_unit', etc.

    # Build lookups
    recipe_map = { r["_id"]: r for r in recipes }
    user_set   = set(user_ingredients or [])

    # 3) Filter & score
    pot_ratio = {}   # recipe_id -> match ratio
    candidates = []

    for rid, recipe in recipe_map.items():
        names = [ing["name"] for ing in recipe.get("ingredients", [])]

        # a) ingredientsUsed filter: require at least one
        if ingredientsUsed:
            if not any(i in names for i in ingredientsUsed):
                continue

        # b) time filters
        if timeCook and recipe.get("cookTime", 0) > timeCook:
            continue
        if totalTime and recipe.get("totalTime", 0) > totalTime:
            continue
        if prepTime and recipe.get("prepTime", 0) > prepTime:
            continue

        # c) compute ingredient‐match ratio
        if haveSome:
            present = sum(1 for n in names if n in user_set)
        else:
            present = 0
        total = len(names)
        ratio = (present / total) if total > 0 else 0.0

        candidates.append(rid)
        pot_ratio[rid] = ratio

    # 4) Sort candidates
    if sortBy == "alpha":
        candidates.sort(key=lambda rid: recipe_map[rid]["name"])
    elif sortBy == "price":
        # Placeholder: price logic not implemented yet → fallback to ratio
        candidates.sort(key=lambda rid: pot_ratio[rid])
    else:
        # 'percent' or anything else → highest match first
        candidates.sort(key=lambda rid: pot_ratio[rid], reverse=True)

    return candidates
