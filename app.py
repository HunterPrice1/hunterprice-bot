import os
import telebot
from flask import Flask
import threading

app = Flask(__name__)
bot = telebot.TeleBot('8528605880:AAE9FTYavk_p0bBJctDtsiCPF7dSzJHkbjI')

# ===== TELEGRAM BOT HANDLERS =====
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
    products = [
        {'title': '🔥 Nike Air Max', 'price': '4,299 руб', 'link': 'https://aliexpress.ru'},
        {'title': '💎 Adidas Ultraboost', 'price': '3,899 руб', 'link': 'https://aliexpress.ru'}
    ]
    
    for product in products:
        markup = telebot.types.InlineKeyboardMarkup()
        btn = telebot.types.InlineKeyboardButton('🛒 Купить', url=product['link'])
        markup.add(btn)
        
        bot.send_message(
            message.chat.id,
            f"{product['title']}\n💰 {product['price']}",
            reply_markup=markup
        )

@bot.message_handler(func=lambda message: message.text == 'ℹ️ О боте')
def about(message):
    bot.send_message(message.chat.id, "🦊 HunterPrice - ищет лучшие товары на AliExpress!")

# ===== FLASK ROUTES (для Render) =====
@app.route('/')
def home():
    return "🦊 HunterPrice Bot is RUNNING!"

@app.route('/health')
def health():
    return "OK"

@app.route('/ping')
def ping():
    return "pong"

# ===== ЗАПУСК БОТА В ФОНЕ =====
def run_bot():
    print("🦊 Starting Telegram Bot...")
    try:
        bot.infinity_polling()
    except Exception as e:
        print(f"Bot error: {e}")

# Запускаем бота при импорте
print("🦊 Initializing HunterPrice Bot...")
bot_thread = threading.Thread(target=run_bot)
bot_thread.daemon = True
bot_thread.start()

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
