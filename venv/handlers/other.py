from aiogram import Router
from aiogram.types import Message

router = Router()

#Иные сообщения боту
@router.message()
async def prin_noname_command(message: Message):
    await message.answer(text='Извините, но я не знаю такой команды,\n'
                              'если вы хотите повторно использовать поиск, введите /search\n'
                              'или просто перейдите в главное меню через команду /start')

