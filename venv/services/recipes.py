from random import choice
from database.database import recipes, users
from lexicon.lexicon import LEXICON

#Получение рандомного рецепта
def get_random_recipes() -> str:
    name_recipe = choice(list(recipes))
    return name_recipe+"\n"+recipes[name_recipe]
#Получение рецептов (названия)
def get_recipe(message: str) -> list[str]:
    answer = []
    for recipe in recipes.keys():
        if message.lower() in recipe.lower().split():
            answer.append(recipe)
    if len(answer)==0:
        answer.append(LEXICON['no_recipe'])
        return answer
    return answer
#Посмотреть сам рецепт
def get_see_recipe(message: str) -> str:
    return recipes[message]
#Удаление рецепта
def del_recipe(rec, id):
    if rec in users[id]['save']:
       users[id]['save'].remove(rec)