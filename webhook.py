from fastapi import FastAPI, Request
from pydantic import BaseModel
from handlers import *
import requests
from tg_message_data import Update
from config import load_config
import logging


app = FastAPI()

class TelegramWebhook(BaseModel):
    message: dict = {}
    callback_query: dict = {}
    message: dict = {}
    pre_checkout_query: dict = {}
    success_payment: dict = {}


# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler("webhook.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


@app.post("/webhook")
async def webhook_handler(update: Update):
    try:
        if update.message.text:
            await message_hendler(update.message)

        logger.info('Status: ok')
        return {"status": "ok"}

    except Exception as e:
        logger.exception(f"Error in webhook handler: {e}")
        return {"status": "error", "message": str(e)}

#  обработчик для корневого URL
@app.get("/")
async def read_root():
    logger.info('Root endpoint reached')
    return {"message": "Welcome to the Telegram Webhook Server"}

#  обработчик для favicon.ico
@app.get("/favicon.ico")
async def favicon():
    return {"status": "ok"}


if __name__ == '__main__':
    config = load_config('config')
    TOKEN = config.tg_bot.token
    # TOKEN = '6451700525:AAHrvFtmXWikJr643nkGYgkDbm8UcFm_9oQ'
    WEBHOOK_URL = config.webhook_url.url
    # WEBHOOK_URL='https://9daf-5-178-148-223.ngrok-free.app/webhook'


    # Настройка вебхука
    url = f'https://api.telegram.org/bot{TOKEN}/setWebhook'
    payload = {
        'url': WEBHOOK_URL,
        'allowed_updates': ["message", "callback_query", "pre_checkout_query", "successful_payment"]
    }
    response = requests.post(url, json=payload)

    if response.status_code == 200:
        print("Webhook set successfully")
    else:
        print(f"Failed to set webhook: {response.text}")

    # Запуск сервера FastAPI на порту 80
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=80)
