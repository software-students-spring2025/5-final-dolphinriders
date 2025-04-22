
ingredients_collection = db.ingredients

def filter(sortBy,timeCook,ready,ingredientsUsed,haveSome):
    ingredientsList = ingredients_collection.get()
    recipeList = recipe_collection.get()
    potentialRecipeIDs = []
    potRecIngredientRatio = {} # structure is _id:{"total":0,"present":0,"ratio":0}

    # TODO add filtering for specific ingredients, cook time, abd favorites

    # TOOO add price finding feature
    if (ingredientsUsed == []):



    # DONE mod filter to inclode 0% recipes
    for recipe in recipeList:
        ingredientNames = []
        for ingredient in recipe["ingredients"]:
            ingredientNames.append(recipe["ingredients"]["name"])
        if (haveSome == False):
                potentialRecipeIDs.append(recipe["_id"])
                potRecIngredientRatio.append(recipe["_id"]:{"total":ingredientNames.size,"present":0,"ratio":0})
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
    # TODO: sort by price, alphabetical, percent ingredients

    # this code was written by a human goddamn being with a soul and thoughts.

    return potentialRecipeIDs
