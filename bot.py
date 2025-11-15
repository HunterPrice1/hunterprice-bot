import os
import telebot
import requests
import logging
from flask import Flask

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Создаем Flask приложение для веб-сервера
app = Flask(__name__)

# Инициализируем бота
bot = telebot.TeleBot('8528605880:AAE9FTYavk_p0bBJctDtsiCPF7dSzJHkbjI')

# Заглушка парсера (позже заменим на реальный)
def parse_aliexpress(query):
    return [
        {
            'title': '🔥 Nike Air Max 2024 - ЛУЧШИЕ КРОССОВКИ',
            'price': '4,299 руб',
            'rating': '4.8/5 ⭐',
            'reviews': '1,234 отзыва',
            'link': 'https://aliexpress.ru/item/1005005123456.html',
            'image': 'https://via.placeholder.com/300x300/FF6B6B/white?text=Nike+Air+Max'
        },
        {
            'title': '💎 Adidas Ultraboost - СУПЕР УДОБНЫЕ',
            'price': '3,899 руб',
            'rating': '4.9/5 ⭐', 
            'reviews': '856 отзывов',
            'link': 'https://aliexpress.ru/item/1005005123457.html',
            'image': 'https://via.placeholder.com/300x300/4ECDC4/white?text=Adidas+Ultra'
        },
        {
            'title': '🚀 Puma RS-X - СТИЛЬ И КАЧЕСТВО',
            'price': '2,999 руб',
            'rating': '4.7/5 ⭐',
            'reviews': '2,101 отзыв',
            'link': 'https://aliexpress.ru/item/1005005123458.html',
            'image': 'https://via.placeholder.com/300x300/45B7D1/white?text=Puma+RS-X'
        }
    ]

@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = telebot.types.KeyboardButton('👟 Кроссовки')
    btn2 = telebot.types.KeyboardButton('🎒 Рюкзаки')
    btn3 = telebot.types.KeyboardButton('👕 Одежда')
    btn4 = telebot.types.KeyboardButton('📱 Гаджеты')
    btn5 = telebot.types.KeyboardButton('ℹ️ О боте')
    markup.add(btn1, btn2, btn3, btn4, btn5)
    
    welcome_text = f"""
🦊 *Добро пожаловать, {message.from_user.first_name}!*

Я *HunterPrice* - ваш личный помощник для поиска лучших товаров на AliExpress!

*🎯 Что я умею:*
• Искать товары по категориям  
• Показывать лучшие предложения
• Сортировать по цене и рейтингу
• Находить акции и скидки

*👇 Выберите категорию или напишите что искать:*
"""
    
    bot.send_message(
        message.chat.id,
        welcome_text,
        reply_markup=markup,
        parse_mode='Markdown'
    )

@bot.message_handler(func=lambda message: message.text == '👟 Кроссовки')
def send_sneakers(message):
    bot.send_message(message.chat.id, "🔍 *Ищу лучшие кроссовки...*", parse_mode='Markdown')
    
    products = parse_aliexpress('кроссовки')
    
    for product in products:
        caption = f"""
*{product['title']}*

💰 *Цена:* {product['price']}
⭐ *Рейтинг:* {product['rating']}
📝 *Отзывы:* {product['reviews']}

⚡ Бесплатная доставка
🛡️ Гарантия возврата
"""
        
        markup = telebot.types.InlineKeyboardMarkup()
        btn_buy = telebot.types.InlineKeyboardButton('🛒 Купить на AliExpress', url=product['link'])
        btn_more = telebot.types.InlineKeyboardButton('🔍 Еще варианты', callback_data='more_sneakers')
        markup.add(btn_buy, btn_more)
        
        # Отправляем изображение с описанием
        try:
            bot.send_photo(
                message.chat.id,
                product['image'],
                caption=caption,
                reply_markup=markup,
                parse_mode='Markdown'
            )
        except:
            # Если не удалось отправить фото, отправляем текстом
            bot.send_message(
                message.chat.id,
                caption,
                reply_markup=markup,
                parse_mode='Markdown'
            )

@bot.message_handler(func=lambda message: message.text == 'ℹ️ О боте')
def about_bot(message):
    about_text = """
*🦊 О боте HunterPrice*

*Версия:* 1.0
*Статус:* Активен ✅

*📈 Статистика:*
• Пользователей: растем!
• Найдено товаров: 1000+
• Экономим деньги: ДА!

*🛠 Разработчик:* Den Bejenari
*💡 Идея:* Помогать находить лучшие товары по выгодным ценам!

*🔮 В планах:*
- Реальный парсинг цен
- Уведомления о скидках  
- Сравнение цен
- История поисков
"""
    bot.send_message(message.chat.id, about_text, parse_mode='Markdown')

@bot.message_handler(func=lambda message: True)
def handle_other_messages(message):
    bot.send_message(
        message.chat.id,
        f"🔍 Хорошо! Ищу: *{message.text}*\n\nПока это демо-версия. Скоро здесь будут реальные товары!",
        parse_mode='Markdown'
    )

# Веб-сервер для Render
@app.route('/')
def home():
    return "🦊 HunterPrice Bot is running!"

@app.route('/health')
def health():
    return "OK"

# Запуск бота
def run_bot():
    logging.info("🦊 HunterPrice Bot запущен!")
    bot.infinity_polling()

if __name__ == "__main__":
    # Для Render нужно запускать через gunicorn
    if os.environ.get('RENDER'):
        # В Render запускаем только Flask
        app.run(host='0.0.0.0', port=5000)
    else:
        # Локально запускаем бота
        run_bot()
