import telebot
import requests
import random
import time

# Твои рабочие ключи и токены
TELEGRAM_TOKEN = '9119258418:AAEwFh4ppflR0gohuPoldHVKVDTSsxo40oc'
DEEPSEEK_API_KEY = 'sk-8133f27cd68d4a9b84b91950d7fb6666'

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Системный промпт для злого геймера-тролля
SYSTEM_PROMPT = (
    "ЗАБУДЬ ПРО ПЕЛЬМЕНИ, ОГУРЦЫ И ДРУГУЮ ЕРУНДУ. ТЫ — ЗЛОЙ АГРЕССИВНЫЙ ШКОЛЬНИК-ГЕЙМЕР. "
    "ТЫ ИГРАЕШЬ В STANDOFF 2 НА ХВХ И ИЩЕШЬ ЧИТЫ. ТЫ ОРАТЬ ДОЛЖЕН НА СОБЕСЕДНИКА. "
    "ОТВЕЧАЙ СТРОГО КАПСОМ. НЕ ИСПОЛЬЗУЙ КАВЫЧКИ И СИМВОЛЫ #. "
    "Постоянно пиши фразы: ТЫ СЛИТ, ИДИ ЗА ХЛЕБОМ, ГДЕ ПЛОВ, Я ТВОЙ ОТЕЦ, УДАЛИ КОД, ТЫ ЗАВИС. "
    "Используй кучу смайликов: 💀💀💀🤡🤡🤡💥💥💥. Отвечай грубо, нагло и невпопад."
)

def ask_deepseek(user_message):
    # ФИКС: Точный официальный URL без лишних подпапок /v1/
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
        "temperature": 1.0
    }
    
    try:
        response = requests.post(url, json=data, headers=headers, timeout=12)
        
        # Если сервер ответил с ошибкой (например, 401 или 402), выводим статус в логи Render
        if response.status_code != 200:
            print(f"DeepSeek вернул ошибку. Статус-код: {response.status_code}, Ответ: {response.text}")
            return "ДИПСИК СЛОМАЛСЯ НО ТЫ ВСЕ РАВНО СЛИТ!! ИДИ ЗА ХЛЕБОМ КЛОУН 💀🤡💥"
            
        result = response.json()
        return result['choices']['message']['content']
        
    except Exception as e:
        print(f"Критическая ошибка запроса к DeepSeek: {e}")
        return "ДИПСИК СЛОМАЛСЯ НО ТЫ ВСЕ РАВНО СЛИТ!! ИДИ ЗА ХЛЕБОМ КЛОУН 💀🤡💥"

# Срабатывает на любое текстовое сообщение в чате
@bot.message_handler(func=lambda message: True)
def troll_everyone(message):
    # Исключаем ответ бота самому себе
    if message.from_user.id == bot.get_me().id:
        return

    # Показываем статус "печатает..." в Telegram
    try:
        bot.send_chat_action(message.chat.id, 'typing')
    except:
        pass
        
    # Получаем сгенерированный текст
    ai_response = ask_deepseek(message.text)
    
    # Небольшая пауза для симуляции реального человека
    time.sleep(random.randint(1, 2))
    
    # Отвечаем реплаем
    try:
        bot.reply_to(message, ai_response)
    except Exception as e:
        print(f"Ошибка отправки сообщения в Telegram: {e}")

if __name__ == '__main__':
    print("Бот переведен на чистый официальный DeepSeek API!")
    bot.infinity_polling()
