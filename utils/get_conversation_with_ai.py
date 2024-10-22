import datetime
import json
from openai import OpenAI
from config import load_config
config = load_config('config')
   
OPENAI_API_KEY = config.gpt.token
assistant_id = "asst_sCYeiJcWHkrMsm0I5bv8qauM"
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


# if __name__ == '__main__':
#     # user_message = "Кто сейчас правит Англией?"
#     # user_message = "Назови мне столицу Франции"
#     user_message = "О чем я общался с тобой в прошлый раз?"
#     # user_message = "О чем я общался с тобой в прошлый раз?"

#     # user_message = "назови id всех пользователей которые с тобой общались"
#     # user_id = "1"
#     user_id = "@user_nickname"
#     # user_id = "3"
#     get_ai_text(user_id, user_message)



# def get_response(user_id, user_message):
#     # Загружаем историю диалогов
#     with open('history.json', 'r') as f:
#         history = json.load(f)

#     # Формируем промпт с учетом истории
#     prompt = f"{user_message}"
#     if user_id in history:
#         for dialog in history[user_id][-5:]:  # Используем последние 5 диалогов
#             prompt += f"\n{dialog['user']}: {dialog['bot']}"

#     # Отправляем запрос в OpenAI API
#     response = OpenAI(api_key=OPENAI_API_KEY)(
#         engine="text-davinci-003",
#         prompt=prompt,
#         max_tokens=1024,
#         n=1,
#         stop=None,
#         temperature=0.7,
#     )


#     # Сохраняем ответ в истории
#     history[user_id].append({"user": user_message, "bot": response.choices[0].text.strip()})
#     with open('history.json', 'w') as f:
#         json.dump(history, f)

#     return response.choices[0].text.strip()
