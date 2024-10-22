from utils import get_ai_text
from tg_message_data import Message
from main import dp, bot



async def message_hendler(message: Message):
    print(message)
    user_nickname = message.chat.username
    response = get_ai_text(user_nickname, message.text)
    await bot.send_chat_action(chat_id=message.chat.id, action='typing')
    await bot.send_message(chat_id=message.chat.id, text=response)


