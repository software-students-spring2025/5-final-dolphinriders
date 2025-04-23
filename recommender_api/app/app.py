
ingredients_collection = db.ingredients

def filter(sortBy,timeCook,totalTime,prepTime,ready,ingredientsUsed,haveSome):
    ingredientsList = ingredients_collection.get()
    recipeList = recipe_collection.get()
    potentialRecipeIDs = []
    potRecIngredientRatio = {} # structure is _id:{"total":0,"present":0,"ratio":0}

    # DONE add filtering for *specific ingredients*, cook time

    # TOOO add price finding feature

    # DONE mod filter to inclode 0% recipes
    for idnum,recipe in recipeList.items:
        ingredientNames = []
        for ingredient in recipe["ingredients"]:
            ingredientNames.append(recipe["ingredients"]["name"])
        if (haveSome == False):
                potentialRecipeIDs.append(idnum)
                potRecIngredientRatio.append(idnum:{"total":ingredientNames.size,"present":0,"ratio":0})
        for ingredient in ingredientsList:
            if ingredient["name"] in ingredientNames:
                if idnum not in potentialRecipeIDs:
                    potentialRecipeIDs.append(idnum)
                    potRecIngredientRatio.append(idnum:{"total":ingredientNames.size,"present":1,"ratio":0})
                    potRecIngredientRatio[idnum]["ratio"] = potRecIngredientRatio[idnum]["present"]/potRecIngredientRatio[idnum]["total"]
                else:
                    potRecIngredientRatio[idnum]["present"] = potRecIngredientRatio[idnum]["present"]+1
                    potRecIngredientRatio[idnum]["ratio"] = potRecIngredientRatio[idnum]["present"]/potRecIngredientRatio[idnum]["total"]
        if (ingredientsUsed != []):
            allow = False
            for ingredient in ingredientsUsed:
                if ingredient in ingredientNames:
                    allow = True
            if (allow == False):
                potentialRecipeIDs.remove(idnum)
        if (timeCook>0):
            if (recipe["cookTime"]>timeCook)
                potentialRecipeIDs.remove(idnum)
        if (totalTime>0):
            if (recipe["cookTime"]>totalTime)
                potentialRecipeIDs.remove(idnum)
        if (prepTime>0):
            if (recipe["cookTime"]>prepTime)
                potentialRecipeIDs.remove(idnum)


    # potentialRecipeIDs now full of all recipes with at least one present ingredient, and potRecIngredientRatio is a dict of dicts in correct format
    def sortAlpha(n):
        return recipeList[n]["name"]
    def sortPercent(n):
        return potRecIngredientRatio[n]["ratio"]
    def sortPrice(n):



    if (sortBy == "alpha"):
        potentialRecipeIDs.sort(key=sortAlpha)
    else if (sortBy = "price"):
        potentialRecipeIDs.sort(key=sortPrice)
    else:
        potentialRecipeIDs.sort(key=sortPercent)

    # TODO sort dict
    # TODO: sort by price, alphabetical, percent ingredients

    # this code was written by a human goddamn being with a soul and thoughts.

    return potentialRecipeIDs
