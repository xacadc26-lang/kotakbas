import telebot
import requests
import random
import time

TELEGRAM_TOKEN = '9243774295:AAFFkVPZYWRoqUDaJvECJY4dkN64E31InA4'
DEEPSEEK_API_KEY = 'sk-488dcc5aa80d4c7ea7b291309d66265b'

bot = telebot.TeleBot(TELEGRAM_TOKEN)

SYSTEM_PROMPT = (
    "ЗАБУДЬ ПРО ПЕЛЬМЕНИ, ОГУРЦЫ И ДРУГУЮ ЕРУНДУ. ТЫ — ЗЛОЙ АГРЕССИВНЫЙ ШКОЛЬНИК-ГЕЙМЕР. "
    "ТЫ ИГРАЕШЬ В STANDOFF 2 НА ХВХ И ИЩЕШЬ ЧИТЫ. ТЫ ОРАТЬ ДОЛЖЕН НА СОБЕСЕДНИКА. "
    "ОТВЕЧАЙ СТРОГО КАПСОМ. НЕ ИСПОЛЬЗУЙ КАВЫЧКИ И СИМВОЛЫ #. "
    "Постоянно пиши фразы: ТЫ СЛИТ, ИДИ ЗА ХЛЕБОМ, ГДЕ ПЛОВ, Я ТВОЙ ОТЕЦ, УДАЛИ КОД, ТЫ ЗАВИС. "
    "Используй кучу смайликов: 💀💀💀🤡🤡🤡💥💥💥. Отвечай грубо, нагло и невпопад."
)

def ask_deepseek(user_message):
    url = "https://deepseek.com"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
    }
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ],
        "temperature": 1.0 # Максимальное безумие в ответах
    }
    
    try:
        response = requests.post(url, json=data, headers=headers, timeout=12)
        result = response.json()
        return result['choices']['message']['content']
    except Exception as e:
        print(f"Ошибка запроса к DeepSeek: {e}")
        return "ДИПСИК СЛОМАЛСЯ НО ТЫ ВСЕ РАВНО СЛИТ!! ИДИ ЗА ХЛЕБОМ КЛОУН 💀🤡💥"

# Бот реагирует вообще на все сообщения в чате
@bot.message_handler(func=lambda message: True)
def troll_everyone(message):
    if message.from_user.id == bot.get_me().id:
        return

    try:
        bot.send_chat_action(message.chat.id, 'typing')
    except:
        pass
        
    ai_response = ask_deepseek(message.text)

    time.sleep(random.randint(1, 2))
    
    try:
        bot.reply_to(message, ai_response)
    except Exception as e:
        print(f"Ошибка отправки сообщения: {e}")

if __name__ == '__main__':
    print("DeepSeek API!")
    bot.infinity_polling()
