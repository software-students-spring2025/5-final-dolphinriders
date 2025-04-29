# grocery_optimizer/optimizer/utils.py

from typing import List, Dict, Any


def optimize_shopping_list(
    recipe_ingredients: List[Dict[str, Any]],
    inventory: List[str]
) -> List[Dict[str, Any]]:
    """
    Given a list of recipe ingredient dicts and a list of ingredient names
    already on hand, return only those ingredients still needed.

    Each recipe ingredient dict should have at least:
      - "name": str
      - optional "quantity": number
      - optional "unit": str
    """
    # Normalize inventory to lowercase set
    inv_set = {item.strip().lower() for item in inventory}
    missing: List[Dict[str, Any]] = []

    for ing in recipe_ingredients:
        name = ing.get("name", "").strip()
        if not name:
            continue
        # If user already has it, skip
        if name.lower() in inv_set:
            continue
        # Otherwise, include in missing list
        missing.append({
            "ingredient": name,
            "quantity": ing.get("quantity"),
            "unit": ing.get("unit"),
            "estimated_price": None
        })

    return missing