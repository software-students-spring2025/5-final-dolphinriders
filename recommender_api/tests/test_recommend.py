import pytest
from app.recommend import filter
from app.models import RecipeFilterParams

def test_filter_no_inventory():
    params = RecipeFilterParams()
    result = filter(params, [])
    assert isinstance(result, list)
