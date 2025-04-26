from app.db import recipe_collection, ingredients_collection, get_recipes, get_ingredients
from app.models import RecipeFilterParams

def filter(params,user_ingredients):
    sortBy = params.sortBy
    timeCook=params.timeCook
    totalTime=params.totalTime
    prepTime=params.prepTime
    ready=params.ready
    ingredientsUsed=params.ingredientsUsed
    haveSome=params.haveSome # unpack params

    ingredientsCursor = ingredients_collection.find() # .find returns a cursor of all items
    ingredientsList = [x for x in ingredients_collection.find()] # iterate through cursor to get all ingredients
    ingredientsIHave = user_ingredients # same but for ingredients we have some of
    ingredientsCursor = ingredients_collection.find()
    recipeCursor = recipe_collection.get()
    recipeList = {x._id:{name:x.name,ingredients:x.ingredients,instructions:x.instructions,cookTime:x.cooktime,prepTime:x.prepTime,totalTime:x.totalTime} for x in recipeCursor}
    recipeCursor = recipe_collection.get()
    potentialRecipeIDs = []
    potRecIngredientRatio = {} # structure is _id:{"total":0,"present":0,"ratio":0}

    # DONE add filtering for *specific ingredients*, cook time

    # TODO add price finding feature

    # DONE mod filter to inclode 0% recipes
    for idnum,recipe in recipeList.items:
        ingredientNames = []
        for ingredient in recipe["ingredients"]:
            ingredientNames.append(recipe["ingredients"]["name"])
            
        if (haveSome == False):
                potentialRecipeIDs.append(idnum)
                potRecIngredientRatio[idnum]={"total":ingredientNames.size,"present":0,"ratio":0}
        for ingredient in ingredientsCursor:
            if ingredient["name"] in ingredientNames:
                if idnum not in potentialRecipeIDs:
                    potentialRecipeIDs.append(idnum)
                    potRecIngredientRatio[idnum]={"total":ingredientNames.size,"present":1,"ratio":0}
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
            if (recipe["cookTime"]>timeCook):
                potentialRecipeIDs.remove(idnum)
        if (totalTime>0):
            if (recipe["cookTime"]>totalTime):
                potentialRecipeIDs.remove(idnum)
        if (prepTime>0):
            if (recipe["cookTime"]>prepTime):
                potentialRecipeIDs.remove(idnum)


    # potentialRecipeIDs now full of all recipes with at least one present ingredient, and potRecIngredientRatio is a dict of dicts in correct format
    def sortAlpha(n):
        return recipeList[n]["name"]
    def sortPercent(n):
        return potRecIngredientRatio[n]["ratio"]
    def sortPrice(n):
        totalPrice = 0.0
        for ingredient in recipeList[n]["ingredients"]:
            if ingredient["name"] not in ingredientsIHave.keys():
                totalprice += ingredientsList[ingredient["name"]]["price"]*(ingredient["quantity"]-ingredientsList[ingredient["name"]]["quantity"])
        return totalPrice




    if (sortBy == "alpha"):
        potentialRecipeIDs.sort(key=sortAlpha)
    elif (sortBy == "price"):
        potentialRecipeIDs.sort(key=sortPrice)
    else:
        potentialRecipeIDs.sort(key=sortPercent)

    # DONE sort dict
    # DONE: sort by price, alphabetical, percent ingredients

    # this code was written by a human goddamn being with a soul and thoughts.

    return potentialRecipeIDs