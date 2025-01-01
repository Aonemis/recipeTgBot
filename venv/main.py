import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from handlers import user, other
from config.config import load_config
from set_menu.menu import main_menu

#Инициируем логер
logger = logging.getLogger(__name__)

async def main():
    #Настройка логера
    logging.basicConfig(
        level=logging.DEBUG,
        format=f'[%(asctime)s] %(filename)s: %(name)s'
               f'%(lineno)d %(levelname)s %(message)s '
    )
    logger.info('Start bot')
    #Добавляем конфиг с инициализацией данных в виртуальное окружение
    config = load_config()
    #Создаем бота, передаем токен с виртуального окружения
    bot = Bot(
        token=config.tg_bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    #Создаем диспатчер
    dp = Dispatcher()
    #Регистрируем в нем роутеры с хендлеров
    dp.include_router(user.router)
    dp.include_router(other.router)
    #Создаем меню бота
    await main_menu(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

asyncio.run(main())