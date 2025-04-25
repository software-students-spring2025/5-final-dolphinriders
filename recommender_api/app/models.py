from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Ingredient:
    name: str
    quantity: Optional[float] = None
    unit: Optional[str] = None
    price_per_unit: Optional[float] = None
    category: Optional[str] = None

@dataclass
class RecipeIngredient:
    name: str
    quantity: Optional[float] = None
    unit: Optional[str] = None
    
@dataclass
class Recipe:
    name: str
    ingredients: List[RecipeIngredient]
    instructions: List[str]
    cookTime: int
    prepTime: int 
    totalTime: Optional[int] = None
    servings: Optional[int] = None
    cuisine: Optional[str] = None
    tags: Optional[List[str]] = None
    image_url: Optional[str] = None
    
@dataclass
class UserIngredients:
    user_id: str
    ingredients: List[str]
    last_updated: datetime = field(default_factory=datetime.now)

@dataclass
class RecipeFilterParams:
    sortBy: str = "percent"
    timeCook: int = 0  
    totalTime: int = 0 
    prepTime: int = 0  
    ready: bool = False  
    ingredientsUsed: List[str] = field(default_factory=list) 
    haveSome: bool = True  

@dataclass
class ShoppingListItem:
    ingredient: str
    quantity: Optional[float] = None
    unit: Optional[str] = None
    estimated_price: Optional[float] = None

@dataclass
class ShoppingList:
    recipe_id: str
    recipe_name: str
    missing_ingredients: List[ShoppingListItem]
    total_estimated_price: Optional[float] = None 