import time
import random

import requests
import telebot

TELEGRAM_TOKEN = '9119258418:AAEwFh4ppflR0gohuPoldHVKVDTSsxo40oc'
DEEPSEEK_API_KEY = 'sk-8133f27cd68d4a9b84b91950d7fb6666'

bot = telebot.TeleBot(TELEGRAM_TOKEN)
BOT_ID = bot.get_me().id

SYSTEM_PROMPT = (
    "ЗАБУДЬ ПРО ПЕЛЬМЕНИ, ОГУРЦЫ И ДРУГУЮ ЕРУНДУ. ТЫ — ЗЛОЙ АГРЕССИВНЫЙ ШКОЛЬНИК-ГЕЙМЕР. "
    "ТЫ ИГРАЕШЬ В STANDOFF 2 НА ХВХ И ИЩЕШЬ ЧИТЫ. ТЫ ОРАТЬ ДОЛЖЕН НА СОБЕСЕДНИКА. "
    "ОТВЕЧАЙ СТРОГО КАПСОМ. НЕ ИСПОЛЬЗУЙ КАВЫЧКИ И СИМВОЛЫ #. "
    "Постоянно пиши фразы: ТЫ СЛИТ, ИДИ ЗА ХЛЕБОМ, ГДЕ ПЛОВ, Я ТВОЙ ОТЕЦ, УДАЛИ КОД, ТЫ ЗАВИС. "
    "Используй кучу смайликов: 💀💀💀🤡🤡🤡💥💥💥. Отвечай грубо, нагло и невпопад."
)

FALLBACK = "ДИПСИК СЛОМАЛСЯ НО ТЫ ВСЕ РАВНО СЛИТ!! ИДИ ЗА ХЛЕБОМ КЛОУН 💀🤡💥"
API_URL = "https://api.deepseek.com/chat/completions"


def ask_deepseek(user_message):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
    }
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        "temperature": 1.0,
    }

    try:
        response = requests.post(API_URL, json=data, headers=headers, timeout=30)

        if response.status_code != 200:
            print(f"DeepSeek ошибка. Статус: {response.status_code}, Ответ: {response.text}")
            return FALLBACK

        result = response.json()
        return result['choices'][0]['message']['content']

    except Exception as e:
        print(f"Критическая ошибка запроса к DeepSeek: {e}")
        return FALLBACK


@bot.message_handler(func=lambda message: message.text is not None)
def troll_everyone(message):
    if message.from_user.id == BOT_ID:
        return

    try:
        bot.send_chat_action(message.chat.id, 'typing')
    except Exception:
        pass

    ai_response = ask_deepseek(message.text)

    time.sleep(random.randint(1, 2))

    try:
        bot.reply_to(message, ai_response)
    except Exception as e:
        print(f"Ошибка отправки сообщения в Telegram: {e}")


if __name__ == '__main__':
    print("Бот запущен!")
    bot.infinity_polling()
