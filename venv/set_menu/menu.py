from aiogram import Bot
from aiogram.types import BotCommand
from lexicon.lexicon import LEXICON_COMMAND

async def main_menu(bot: Bot):
    my_command = [BotCommand(
        command=command,
        description=description) for command, description in LEXICON_COMMAND.items()]
    await bot.set_my_commands(my_command)