import logging
from copy import deepcopy
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, StateFilter, Command
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.fsm.context import FSMContext
from lexicon.lexicon import LEXICON
from keyboard.keyboard import (start_keyboard, random_keyboard,
                               search_keyboard, save_recipe,
                               print_save_recipe, search_all_recipe,
                               edit_keyboard)
from services.recipes import get_recipe, get_random_recipes, get_see_recipe, del_recipe
from database.database import user_search, users, user_data, recipes


logger = logging.getLogger(__name__)
router = Router()
#Отслеживаем состояние бота поиск или обычное
class MyFSM(StatesGroup):
    fsearch = State()

#Обработка команды старт
@router.message(CommandStart(), StateFilter(default_state))
async def process_start(message: Message):
    logger.info('Запустили старт')
    if message.from_user.id not in users:
        users[message.from_user.id] = deepcopy(user_data)
    await message.answer(text=LEXICON['/start'],
                         reply_markup=start_keyboard(3, '/help', '/random', '/search', '/see_save_recipe'))

#Обработка команды помощь
@router.callback_query(F.data == '/help', StateFilter(default_state))
async def process_help(callback: CallbackQuery):
    logger.info('Запустили хелп')
    await callback.message.edit_text(text=LEXICON['/help'],
                                     reply_markup=start_keyboard(2, '/random', '/search', '/see_save_recipe'))
@router.message(Command(commands='help'), StateFilter(default_state))
async def process_help(message: Message):
    logger.info('Запустили хелп')
    await message.answer(text=LEXICON['/help'],
                         reply_markup=start_keyboard(2, '/random', '/search', '/see_save_recipe'))

#Обработка показа случайного рецепта
@router.callback_query(F.data == '/random', StateFilter(default_state))
async def process_random(callback: CallbackQuery):
    logger.info('Запросили рандомный рецепт')
    text = get_random_recipes()
    while text == callback.message.text:
        text = get_random_recipes()
    await callback.message.edit_text(text=text,
                                     reply_markup=random_keyboard())

@router.message(Command(commands='random'), StateFilter(default_state))
async def process_random(message: Message):
    logger.info('Запросили рандомный рецепт')
    text = get_random_recipes()
    while text == message.text:
        text = get_random_recipes()
    await message.answer(text=text, reply_markup=random_keyboard())

#Обработка нажатия на показ следующего случайного рецепта
@router.callback_query(F.data == '/next', StateFilter(default_state))
async def process_next_recipe(callback: CallbackQuery):
    logger.info("Отправили запрос на следующий рецепт")
    text = get_random_recipes()
    while text == callback.message.text:
        text = get_random_recipes()
    await callback.message.edit_text(text=text,
                                     reply_markup=random_keyboard())

#Инициализируем поиск рецепта
@router.callback_query(F.data == '/search', StateFilter(default_state))
async def process_start_search(callback: CallbackQuery, state: FSMContext):
    user_search.clear()
    await state.set_state(MyFSM.fsearch)
    await callback.message.edit_text(text=LEXICON['search'])
@router.message(Command(commands='search'), StateFilter(default_state))
async def process_start_search(message: Message, state: FSMContext):
    user_search.clear()
    await state.set_state(MyFSM.fsearch)
    await message.answer(text=LEXICON['search'])

#Ищем рецепт в базе и отправляем пользователю
@router.message(StateFilter(MyFSM.fsearch))
async def process_search(message: Message, state: FSMContext):
    answer = get_recipe(message.text)
    if answer:
        for ans in answer:
            user_search.append(ans)
    else:
        user_search.append(LEXICON['no_recipe'])
    if len(user_search) > 1:
        users[message.from_user.id]['recipe'] = 0
        text = search_all_recipe(0, user_search)
        await message.answer(text=f"Результаты запроса #{users[message.from_user.id]['recipe']+1}", reply_markup=text)
    else:
        await message.answer(text=get_see_recipe(user_search[0]))
    await state.clear()

#Проходим по списку найденных результатов поиска
@router.callback_query(F.data.in_(['forward', 'backward']), StateFilter(default_state))
async def process_find_recipes(callback: CallbackQuery):
    if callback.data == 'forward' and users[callback.from_user.id]['recipe'] <= len(user_search):
        users[callback.from_user.id]['recipe']+=5
        text = search_all_recipe(users[callback.from_user.id]['recipe'], user_search)
        await callback.message.edit_text(text=f'Результаты запроса #{users[callback.from_user.id]['recipe']}',
                                         reply_markup=text)
        print(text)
        print(users[callback.from_user.id]['recipe'])
        print(user_search)
        print(len(user_search))
    elif callback.data == 'backward' and users[callback.from_user.id]['recipe']-5 >= -1:
        users[callback.from_user.id]['recipe']-=5
        text = search_all_recipe(users[callback.from_user.id]['recipe'], user_search)
        #if callback.message.text != user_search[users[callback.from_user.id]['recipe']]:
        await callback.message.edit_text(text=f'Результаты запроса #{users[callback.from_user.id]['recipe']}', reply_markup=text)
        #await callback.message.edit_text(text=user_search[users[callback.from_user.id]['recipe']], reply_markup=search_keyboard())
    else:
        await callback.answer(text=LEXICON['end_result'])
#Просмотр рецепта
@router.callback_query(F.data == 'see_recipe', StateFilter(default_state))
async def process_see_recipe(callback: CallbackQuery):
    await callback.message.edit_text(
        text=get_see_recipe(user_search[users[callback.from_user.id]['recipe']]),
        reply_markup=save_recipe()
    )
#Сохранение рецепта
@router.callback_query(F.data == 'save', StateFilter(default_state))
async def process_save_recipe(callback: CallbackQuery):
    if user_search:
        users[callback.from_user.id]['save'].add(user_search[users[callback.from_user.id]['recipe']])
    else:
        users[callback.from_user.id]['save'].add(callback.message.text[:callback.message.text.find('\n')])
    await callback.answer(text='Рецепт сохранен')
#Просмотр сохраненных рецептов
@router.callback_query(F.data == '/see_save_recipe', StateFilter(default_state))
async def process_see_save_recipe(callback: CallbackQuery):
    await callback.message.edit_text(text='Сохраненные рецепты🍽', reply_markup=print_save_recipe(callback.from_user.id))

@router.message(Command(commands='see_save_recipe'), StateFilter(default_state))
async def see_save_recipe_mes(message: Message):
    await message.answer(
        text='Сохраненные рецепты🍽',
        reply_markup=print_save_recipe(message.from_user.id))

@router.callback_query(F.data.in_(recipes.keys()), StateFilter(default_state))
async def process_see_recipe_from_save(callback: CallbackQuery):
    await callback.message.edit_text(text=get_see_recipe(callback.data), reply_markup=save_recipe())
#Отмена
@router.callback_query(F.data == 'cancel', StateFilter(default_state))
async def process_cancel(callback: CallbackQuery, state: FSMContext):
    user_search.clear()
    users[callback.from_user.id]['recipe'] = 0
    await state.clear()
    await callback.message.edit_text(text=LEXICON['/start'],
                                     reply_markup=start_keyboard(3, '/help', '/random', '/search', '/see_save_recipe'))
#Редактирование рецептов
@router.callback_query(F.data == 'edit', StateFilter(default_state))
async def process_edit(callback: CallbackQuery):
    await callback.message.edit_text(
        text='Редактирование сохраненных рецептов',
        reply_markup=edit_keyboard(callback.from_user.id))
#Удаление рецепта
@router.callback_query(F.data.startswith('del') and F.data[3:].in_(recipes.keys()), StateFilter(default_state))
async def process_del(callback: CallbackQuery):
    del_recipe(callback.data[3:], callback.from_user.id)
    print(users[callback.from_user.id]['save'])
    await callback.answer(text='Рецепт удален')
    await callback.message.edit_text(
        text=f'Редактирование сохраненных рецептов. Всего рецептов сохранено {len(users[callback.from_user.id]['save'])}',
        reply_markup=edit_keyboard(callback.from_user.id))