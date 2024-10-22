import datetime
import json
from openai import OpenAI
from config import load_config
config = load_config('config')
   
OPENAI_API_KEY = config.gpt.token
assistant_id = config.gpt.price_assistant_id
import re



def get_ai_text(user_nickname, user_message):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Загружаем историю диалогов
    try:
        with open('history.json', 'r', encoding='utf-8') as f:
            history = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        history = {}

    # Формируем промпт с учетом истории
    prompt = f"prompt: [{user_message} user_nickname: {user_nickname}], history: ["

    # Добавляем данные по каждому никнейму из истории
    if user_nickname in history:
        for dialog in history[user_nickname]:
            prompt += f"user_nickname: {user_nickname} user: {dialog['user']} bot: {dialog['bot']} current_time: {dialog['current_time']}, "

    # Убираем последнюю лишнюю запятую и закрываем скобку
    prompt = prompt.rstrip(", ") + "]"

    # Выводим итоговый промпт для проверки
    print('prompt:', prompt)

    client = OpenAI(api_key=OPENAI_API_KEY)
    thread = client.beta.threads.create()

    message = client.beta.threads.messages.create(
                thread_id=thread.id,
                role="assistant",
                content=f"{prompt}"
                )
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=assistant_id,
    )

    if run.status == 'completed': 
        messages = client.beta.threads.messages.list(
            thread_id=thread.id
        )
        result_text = messages.data[0].content[0].text.value
        clean_text = re.sub(r'【[^】]*】', '', result_text)
        print('result_text: ', clean_text)
        
        # Сохраняем ответ в истории
        if user_nickname not in history:
            history[user_nickname] = []
        history[user_nickname].append({
            "user": user_message, 
            "bot": clean_text, 
            "current_time": current_time
        })
        
        with open('history.json', 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=4)

        return clean_text
    else:
        print(run.status)


