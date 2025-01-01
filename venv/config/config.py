from dataclasses import dataclass
from environs import Env

#Создаем класс бота
@dataclass
class TgBot:
    token: str
    admin_ids: list[int]

#Создаем класс конфига
@dataclass
class Config:
    tg_bot: TgBot

#Функция загрузки конфига и данных из виртуального окружения
def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    config = Config(
        tg_bot=TgBot(
            token=env('BOT_TOKEN'),
            admin_ids=list(map(int, env.list('ADMIN_IDS')))
        )
    )
    return config