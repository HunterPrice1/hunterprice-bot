import os
import telebot
import requests
import logging
import threading
from flask import Flask

# Настройка логирования
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
bot = telebot.TeleBot('8528605880:AAE9FTYavk_p0bBJctDtsiCPF7dSzJHkbjI')

# Заглушка парсера
def parse_aliexpress(query):
    return [
        {
            'title': '🔥 Nike Air Max 2024',
            'price': '4,299 руб',
            'rating': '4.8/5 ⭐',
            'link': 'https://aliexpress.ru/item/1005005123456.html'
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
        f"🦊 Привет! Я HunterPrice - найду лучшие товары!",
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
            f"{product['title']}\n💰 Цена: {product['price']}\n⭐ Рейтинг: {product['rating']}",
            reply_markup=markup
        )

# Запуск бота в отдельном потоке
def run_bot():
    logging.info("🦊 HunterPrice Bot запущен!")
    bot.infinity_polling()

# Flask маршруты для Render
@app.route('/')
def home():
    return "🦊 HunterPrice Bot is Running!"

@app.route('/health')
def health():
    return "OK"

# Запускаем бот при старте приложения
if __name__ == "__main__":
    # Запускаем бота в отдельном потоке
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()
    
    # Запускаем Flask сервер
    app.run(host='0.0.0.0', port=5000, debug=False)
