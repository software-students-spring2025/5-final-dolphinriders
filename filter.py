
ingredients_collection = db.ingredients

def search_api():
    ingredientsList = ingredients_collection.get()
    recipeList = recipe_collection.get()
    potentialRecipeIDs = []
    potRecIngredientRatio = {} # structure is _id:{"total":0,"present":0,"ratio":0}

    for recipe in recipeList:
        ingredientNames = []
        for ingredient in recipe["ingredients"]:
            ingredientNames.append(recipe["ingredients"]["name"])
        for ingredient in ingredientsList:
            if ingredient["name"] in ingredientNames:
                if recipe["_id"] not in potentialRecipeIDs:
                    potentialRecipeIDs.append(recipe["_id"])
                    potRecIngredientRatio.append(recipe["_id"]:{"total":ingredientNames.size,"present":1,"ratio":0})
                    potRecIngredientRatio[recipe["_id"]]["ratio"] = potRecIngredientRatio[recipe["_id"]]["present"]/potRecIngredientRatio[recipe["_id"]]["total"]
                else:
                    potRecIngredientRatio[recipe["_id"]]["present"] = potRecIngredientRatio[recipe["_id"]]["present"]+1
                    potRecIngredientRatio[recipe["_id"]]["ratio"] = potRecIngredientRatio[recipe["_id"]]["present"]/potRecIngredientRatio[recipe["_id"]]["total"]

    # potentialRecipeIDs now full of all recipes with at least one present ingredient, and potRecIngredientsRatio is a dict of dicts in correct format

    # TODO sort dict

    return potRecIngredientRatio