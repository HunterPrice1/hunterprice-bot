import os
import telebot
from flask import Flask
import threading

app = Flask(__name__)
bot = telebot.TeleBot('8528605880:AAE9FTYavk_p0bBJctDtsiCPF7dSzJHkbjI')

# Простой парсер
def parse_aliexpress(query):
    return [
        {
            'title': '🔥 Nike Air Max 2024',
            'price': '4,299 руб',
            'rating': '4.8/5 ⭐', 
            'link': 'https://aliexpress.ru'
        }
    ]

@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton('👟 Кроссовки')
    markup.add(btn1)
    
    bot.send_message(
        message.chat.id, 
        "🦊 Привет! Я HunterPrice!", 
        reply_markup=markup
    )

@bot.message_handler(func=lambda message: message.text == '👟 Кроссовки')
def sneakers(message):
    products = parse_aliexpress('кроссовки')
    for product in products:
        markup = telebot.types.InlineKeyboardMarkup()
        btn = telebot.types.InlineKeyboardButton('🛒 Купить', url=product['link'])
        markup.add(btn)
        
        bot.send_message(
            message.chat.id,
            f"{product['title']}\n💰 {product['price']}",
            reply_markup=markup
        )

@app.route('/')
def home():
    return "🦊 Bot is RUNNING!"

@app.route('/health')
def health():
    return "OK"

# Запуск бота в фоне
def run_bot():
    print("🦊 Starting Telegram Bot...")
    try:
        bot.infinity_polling()
    except Exception as e:
        print(f"Bot error: {e}")

# Запускаем при старте
bot_thread = threading.Thread(target=run_bot)
bot_thread.daemon = True
bot_thread.start()

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
