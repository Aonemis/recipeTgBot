from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from lexicon.lexicon import LEXICON, LEXICON_B
from database.database import users, recipes

#Стартовая клавиатура
def start_keyboard(width: int, *args, **kwargs) -> InlineKeyboardMarkup:
    buttons: list[InlineKeyboardButton] = []
    if args:
        for button in args:
            buttons.append(InlineKeyboardButton(
                text=LEXICON_B[button] if button in LEXICON_B else button,
                callback_data=button))
    if kwargs:
        for button, text in kwargs.items():
            buttons.append(InlineKeyboardButton(
                text=text,
                callback_data=button))
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(*buttons, width=width)
    return kb_builder.as_markup()
#Рандомный рецепт
def random_keyboard() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    button = InlineKeyboardButton(text='Следующий рецепт', callback_data='/next')
    button_save = InlineKeyboardButton(text='Сохранить', callback_data='save')
    button_cancel = InlineKeyboardButton(text=LEXICON['cancel'], callback_data='cancel')
    kb_builder.row(button, button_save)
    kb_builder.row(button_cancel)
    return kb_builder.as_markup()
#Поисковый запрос
def search_keyboard() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    #middle_button = InlineKeyboardButton(text='Рецепт', callback_data='see_recipe')
    button_forward = InlineKeyboardButton(text='⏩', callback_data='forward')
    button_backward = InlineKeyboardButton(text='⏪', callback_data='backward')
    kb_builder.row(button_backward, button_forward)
    kb_builder.row(InlineKeyboardButton(text=LEXICON['cancel'], callback_data='cancel'))
    return kb_builder.as_markup()
#Показ всех рецептов
def search_all_recipe(number: int, buttons: list[str]):
    kb_builder = InlineKeyboardBuilder()
    buttons_for_builder = []
    count = number
    while count<len(buttons) and len(buttons_for_builder)<5:
        buttons_for_builder.append(InlineKeyboardButton(text=buttons[count],
        callback_data=buttons[count]))
        count += 1
    if buttons_for_builder != []:
        kb_builder.row(*buttons_for_builder, width=1)
    button_forward = InlineKeyboardButton(text='⏩', callback_data='forward')
    button_backward = InlineKeyboardButton(text='⏪', callback_data='backward')
    kb_builder.row(button_backward, button_forward)
    kb_builder.row(InlineKeyboardButton(text=LEXICON['cancel'], callback_data='cancel'))
    return kb_builder.as_markup()
#Сохранение рецепта
def save_recipe() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    button_middle = InlineKeyboardButton(text='Сохраненные рецепты', callback_data='/see_save_recipe')
    button_save = InlineKeyboardButton(text='Сохранить', callback_data='save')
    button_cancel = InlineKeyboardButton(text=LEXICON['cancel'], callback_data='cancel')
    kb_builder.row(button_save, button_middle)
    kb_builder.row(button_cancel)
    return kb_builder.as_markup()
#Просмотр сохраненных рецептов
def print_save_recipe(id):
    buttons = []
    kb_builder = InlineKeyboardBuilder()
    if users[id]['save']:
        for button in users[id]['save']:
            buttons.append(InlineKeyboardButton(
                text=button,
                callback_data=button))
        kb_builder.row(*buttons, width=1)
        kb_builder.row(InlineKeyboardButton(text=LEXICON['edit'], callback_data='edit'))
    kb_builder.row(InlineKeyboardButton(text=LEXICON['cancel'], callback_data='cancel'))
    return kb_builder.as_markup()
#Редактирование
def edit_keyboard(id):
    buttons = []
    kb_builder = InlineKeyboardBuilder()
    if users[id]['save']:
        for button in users[id]['save']:
            buttons.append(InlineKeyboardButton(
                text='❌'+ button,
                callback_data='del' + button))
        kb_builder.row(*buttons, width=1)
    kb_builder.row(InlineKeyboardButton(text=LEXICON['cancel'], callback_data='cancel'))
    return kb_builder.as_markup()
