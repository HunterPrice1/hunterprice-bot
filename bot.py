import os
import telebot
from flask import Flask
import threading
import time

app = Flask(__name__)
bot = telebot.TeleBot('8528605880:AAE9FTYavk_p0bBJctDtsiCPF7dSzJHkbjI')

# Простой парсер (заглушка)
def parse_aliexpress(query):
    return [
        {
            'title': '🔥 Nike Air Max 2024 - ЛУЧШИЕ КРОССОВКИ',
            'price': '4,299 руб',
            'rating': '4.8/5 ⭐',
            'link': 'https://aliexpress.ru'
        },
        {
            'title': '💎 Adidas Ultraboost - СУПЕР УДОБНЫЕ',
            'price': '3,899 руб', 
            'rating': '4.9/5 ⭐',
            'link': 'https://aliexpress.ru'
        }
    ]

@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton('👟 Кроссовки')
    btn2 = telebot.types.KeyboardButton('ℹ️ О боте')
    markup.add(btn1, btn2)
    
    bot.send_message(
        message.chat.id,
        f"🦊 Привет, {message.from_user.first_name}! Я HunterPrice!",
        reply_markup=markup
    )

@bot.message_handler(func=lambda message: message.text == '👟 Кроссовки')
def send_sneakers(message):
    bot.send_message(message.chat.id, "🔍 Ищу кроссовки...")
    
    products = parse_aliexpress('кроссовки')
    for product in products:
        markup = telebot.types.InlineKeyboardMarkup()
        btn = telebot.types.InlineKeyboardButton('🛒 Купить', url=product['link'])
        markup.add(btn)
        
        bot.send_message(
            message.chat.id,
            f"{product['title']}\n💰 {product['price']}\n⭐ {product['rating']}",
            reply_markup=markup
        )

@bot.message_handler(func=lambda message: message.text == 'ℹ️ О боте')
def about(message):
    bot.send_message(message.chat.id, "🦊 HunterPrice - ищет лучшие товары!")

# Важные маршруты для Render health checks
@app.route('/')
def home():
    return "🦊 HunterPrice Bot is ALIVE!"

@app.route('/health')
def health():
    return "OK", 200

@app.route('/ping')
def ping():
    return "pong", 200

# Запускаем бота в отдельном потоке
def run_bot():
    print("🦊 Starting HunterPrice Bot...")
    while True:
        try:
            bot.infinity_polling(timeout=60, long_polling_timeout=30)
        except Exception as e:
            print(f"Bot error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    # Запускаем бота в фоне
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    
    # Запускаем Flask на порту из переменной окружения Render
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
