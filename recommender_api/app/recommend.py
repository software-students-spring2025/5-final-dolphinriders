# recommender_api/app/recommend.py

from flask import current_app
from typing import List, Dict, Any


def recommend_recipes(
    inventory: List[str],
    preferences: Dict[str, bool],
    top_n: int = 5
) -> List[Dict[str, Any]]:
    """
    1. Load all recipes from MongoDB
    2. Filter by dietary preferences (True = must include, False = must exclude)
    3. Compute match ratio = (# matched ingredients) / (total recipe ingredients)
    4. Sort by match ratio (desc) then name (asc)
    5. Return top_n recipe dicts with match_ratio
    """
    db = current_app.db
    raw_docs = list(db.recipes.find({}))
    inv_set = set(item.strip().lower() for item in inventory)

    candidates: List[Dict[str, Any]] = []
    for doc in raw_docs:
        # Normalize tags
        tags = [t.strip().lower() for t in doc.get('tags', [])]
        # Preferences filtering
        skip = False
        for pref, want in preferences.items():
            key = pref.strip().lower()
            if want and key not in tags:
                skip = True
                break
            if not want and key in tags:
                skip = True
                break
        if skip:
            continue

        # Normalize ingredients
        req_ing = [ing.strip().lower() for ing in doc.get('ingredients', [])]
        req_set = set(req_ing)
        # Compute match ratio
        matched = inv_set & req_set
        ratio = len(matched) / len(req_set) if req_set else 0.0

        # Build plain dict for output
        candidates.append({
            'name': doc.get('name', ''),
            'ingredients': req_ing,
            'steps': doc.get('steps', []),
            'tags': tags,
            'match_ratio': round(ratio, 2)
        })

    # Sort by match_ratio desc, then name asc
    candidates.sort(key=lambda x: (-x['match_ratio'], x['name'].lower()))
    return candidates[:top_n] 

