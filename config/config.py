
from dataclasses import dataclass

from environs import Env


    

@dataclass
class TgBot:
    token: str            # Токен для доступа к телеграм-боту


@dataclass
class Gpt:
    token: str            # Токен для доступа к телеграм-боту
    price_assistant_id: str  # Ассистент для работы с пользователем




@dataclass
class WebhookURL:
    url: str              # URL вебхука


@dataclass
class Config:
    tg_bot: TgBot
    gpt: Gpt
    webhook_url: WebhookURL
    




def load_config(path: str | None = None) -> Config:

    # Создаем экземпляр класса Env
    env: Env = Env()

    # Добавляем в переменные окружения данные, прочитанные из файла .env 
    env.read_env()

    # Создаем экземпляр класса Config и наполняем его данными из переменных окружения
    return  Config(
        tg_bot=TgBot(
            token=env('BOT_TOKEN')
        ),
        gpt=Gpt(
            token=env('GPT_TOKEN'),
            price_assistant_id=env('ASSISTANT_ID'),
        ),
        webhook_url=WebhookURL(
            url=env('WEBHOOK_URL')
        )
    )

