import os
import telebot
import requests
from flask import Flask
import threading
from bs4 import BeautifulSoup
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
bot = telebot.TeleBot('8528605880:AAE9FTYavk_p0bBJctDtsiCPF7dSzJHkbjI')

# ===== ПАРСЕР ALIEXPRESS =====
def parse_aliexpress(query):
    """Парсит товары с AliExpress и возвращает 5 лучших"""
    try:
        # Здесь будет реальный парсинг
        # Пока используем демо-данные
        return get_demo_products(query)
    except Exception as e:
        logger.error(f"Ошибка парсинга: {e}")
        return get_demo_products(query)

def get_demo_products(query):
    """Демо-данные товаров"""
    demo_data = {
        'кроссовки': [
            {'title': '🔥 Nike Air Max 2024', 'price': '4,299 ₽', 'rating': '4.8/5 ⭐', 'link': 'https://aliexpress.ru', 'reviews': '1,234 отзыва'},
            {'title': '💎 Adidas Ultraboost', 'price': '3,899 ₽', 'rating': '4.9/5 ⭐', 'link': 'https://aliexpress.ru', 'reviews': '856 отзывов'},
            {'title': '🚀 Puma RS-X', 'price': '2,999 ₽', 'rating': '4.7/5 ⭐', 'link': 'https://aliexpress.ru', 'reviews': '2,101 отзыв'},
        ],
        'одежда': [
            {'title': '👕 Футболка хлопковая', 'price': '899 ₽', 'rating': '4.6/5 ⭐', 'link': 'https://aliexpress.ru', 'reviews': '3,456 отзывов'},
            {'title': '👖 Джинсы классические', 'price': '1,599 ₽', 'rating': '4.7/5 ⭐', 'link': 'https://aliexpress.ru', 'reviews': '2,890 отзывов'},
        ],
        'техника': [
            {'title': '📱 Смартфон Xiaomi', 'price': '15,999 ₽', 'rating': '4.8/5 ⭐', 'link': 'https://aliexpress.ru', 'reviews': '5,678 отзывов'},
            {'title': '🎧 Беспроводные наушники', 'price': '2,499 ₽', 'rating': '4.5/5 ⭐', 'link': 'https://aliexpress.ru', 'reviews': '4,321 отзыв'},
        ],
        'косметика': [
            {'title': '💄 Помада матовая', 'price': '459 ₽', 'rating': '4.7/5 ⭐', 'link': 'https://aliexpress.ru', 'reviews': '1,234 отзыва'},
            {'title': '🧴 Крем для лица', 'price': '699 ₽', 'rating': '4.6/5 ⭐', 'link': 'https://aliexpress.ru', 'reviews': '2,345 отзывов'},
        ],
        'дом': [
            {'title': '🏠 Набор посуды', 'price': '2,899 ₽', 'rating': '4.8/5 ⭐', 'link': 'https://aliexpress.ru', 'reviews': '3,210 отзывов'},
            {'title': '🛏️ Постельное белье', 'price': '1,299 ₽', 'rating': '4.5/5 ⭐', 'link': 'https://aliexpress.ru', 'reviews': '4,567 отзывов'},
        ],
        'спорт': [
            {'title': '🏃‍♂️ Беговая дорожка', 'price': '12,999 ₽', 'rating': '4.7/5 ⭐', 'link': 'https://aliexpress.ru', 'reviews': '890 отзывов'},
            {'title': '⚽ Футбольный мяч', 'price': '1,299 ₽', 'rating': '4.6/5 ⭐', 'link': 'https://aliexpress.ru', 'reviews': '2,345 отзывов'},
        ]
    }
    
    return demo_data.get(query.lower(), [
        {'title': f'🔥 Лучший товар: {query}', 'price': '2,999 ₽', 'rating': '4.8/5 ⭐', 'link': 'https://aliexpress.ru', 'reviews': '1,000+ отзывов'},
        {'title': f'💎 Премиум: {query}', 'price': '4,599 ₽', 'rating': '4.9/5 ⭐', 'link': 'https://aliexpress.ru', 'reviews': '500+ отзывов'},
    ])

# ===== TELEGRAM BOT HANDLERS =====
@bot.message_handler(commands=['start'])
def start(message):
    show_main_menu(message)

def show_main_menu(message):
    """Показывает главное меню с кнопками как на скриншоте"""
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    
    # Первый ряд кнопок
    btn1 = telebot.types.KeyboardButton('👟 Обувь')
    btn2 = telebot.types.KeyboardButton('👕 Одежда')
    btn3 = telebot.types.KeyboardButton('📱 Техника')
    btn4 = telebot.types.KeyboardButton('💄 Косметика')
    
    # Второй ряд кнопок
    btn5 = telebot.types.KeyboardButton('🏠 Дом')
    btn6 = telebot.types.KeyboardButton('🏃‍♂️ Спорт')
    btn7 = telebot.types.KeyboardButton('🔍 Поиск товара')
    btn8 = telebot.types.KeyboardButton('ℹ️ О боте')
    
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8)
    
    welcome_text = f"""
🦊 *HunterPrice Bot*

*Добро пожаловать, {message.from_user.first_name}!*

Я помогу найти лучшие товары на AliExpress по выгодным ценам! 

👇 *Выберите категорию:*
"""
    
    bot.send_message(
        message.chat.id,
        welcome_text,
        reply_markup=markup,
        parse_mode='Markdown'
    )

@bot.message_handler(func=lambda message: message.text in ['👟 Обувь', '👕 Одежда', '📱 Техника', '💄 Косметика', '🏠 Дом', '🏃‍♂️ Спорт'])
def handle_category(message):
    """Обрабатывает выбор категории"""
    categories = {
        '👟 Обувь': 'кроссовки',
        '👕 Одежда': 'одежда',
        '📱 Техника': 'техника',
        '💄 Косметика': 'косметика',
        '🏠 Дом': 'дом',
        '🏃‍♂️ Спорт': 'спорт'
    }
    
    category = categories[message.text]
    search_products(message, category, message.text)

@bot.message_handler(func=lambda message: message.text == '🔍 Поиск товара')
def ask_search(message):
    """Запрашивает поисковый запрос"""
    msg = bot.send_message(
        message.chat.id, 
        "🔍 *Введите название товара для поиска:*\n\nНапример: *наушники, часы, куртка*",
        parse_mode='Markdown',
        reply_markup=telebot.types.ReplyKeyboardRemove()  # Убираем клавиатуру для ввода текста
    )
    bot.register_next_step_handler(msg, handle_search)

def handle_search(message):
    """Обрабатывает поисковый запрос"""
    if message.text == 'Вернуться в меню' or message.text == 'Меню':
        show_main_menu(message)
        return
        
    search_products(message, message.text, f"поиск: {message.text}")

@bot.message_handler(func=lambda message: message.text == 'ℹ️ О боте')
def about_bot(message):
    """Информация о боте"""
    about_text = """
*🦊 О боте HunterPrice*

*Наш сайт:* https://hunterprice-bot.onrender.com

*📞 Контакты:*
Поддержка: @hunterprice_support

*🎯 Что умеет бот:*
• Искать товары на AliExpress
• Показывать лучшие предложения
• Сравнивать цены и рейтинги

*💡 Используйте кнопки меню для навигации!*
"""
    bot.send_message(message.chat.id, about_text, parse_mode='Markdown')

@bot.message_handler(func=lambda message: message.text in ['Вернуться в меню', 'Меню'])
def back_to_menu(message):
    """Возврат в главное меню"""
    show_main_menu(message)

@bot.message_handler(func=lambda message: True)
def handle_other_messages(message):
    """Обработка других сообщений"""
    if message.text.lower() in ['начать', 'старт', 'start', 'меню']:
        show_main_menu(message)
    else:
        # Предлагаем вернуться в меню
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_menu = telebot.types.KeyboardButton('Вернуться в меню')
        markup.add(btn_menu)
        
        bot.send_message(
            message.chat.id,
            "❌ *Произошла ошибка. Возвращаемся в главное меню...*",
            reply_markup=markup,
            parse_mode='Markdown'
        )
        show_main_menu(message)

def search_products(message, query, display_name):
    """Поиск и отправка товаров"""
    bot.send_message(
        message.chat.id, 
        f"🔍 *Ищем товары:* {display_name}\n\n⏳ *Анализируем AliExpress...*", 
        parse_mode='Markdown'
    )
    
    # Запускаем парсинг в отдельном потоке
    def parse_and_send():
        try:
            products = parse_aliexpress(query)
            
            if products:
                # Кнопка возврата в меню
                markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn_menu = telebot.types.KeyboardButton('Вернуться в меню')
                markup.add(btn_menu)
                
                bot.send_message(
                    message.chat.id,
                    f"🎯 *Найдено товаров в категории '{display_name}':*",
                    reply_markup=markup,
                    parse_mode='Markdown'
                )
                
                for i, product in enumerate(products, 1):
                    caption = f"""
*{i}. {product['title']}*

💰 *Цена:* {product['price']}
⭐ *Рейтинг:* {product['rating']}
📝 *Отзывы:* {product['reviews']}

⚡ *Бесплатная доставка*
🛡️ *Гарантия возврата*
"""
                    
                    inline_markup = telebot.types.InlineKeyboardMarkup()
                    btn_buy = telebot.types.InlineKeyboardButton('🛒 Купить на AliExpress', url=product['link'])
                    inline_markup.add(btn_buy)
                    
                    bot.send_message(
                        message.chat.id,
                        caption,
                        reply_markup=inline_markup,
                        parse_mode='Markdown'
                    )
                    
            else:
                bot.send_message(message.chat.id, "❌ Не удалось найти товары. Попробуйте другой запрос.")
                
        except Exception as e:
            logger.error(f"Ошибка поиска: {e}")
            bot.send_message(message.chat.id, "❌ Произошла ошибка при поиске. Попробуйте позже.")
    
    thread = threading.Thread(target=parse_and_send)
    thread.start()

# ===== FLASK ROUTES =====
@app.route('/')
def home():
    return "🦊 HunterPrice Bot - Поиск товаров на AliExpress"

@app.route('/health')
def health():
    return "OK"

# ===== ЗАПУСК БОТА =====
def run_bot():
    logger.info("🦊 Starting HunterPrice Bot with beautiful menu...")
    try:
        bot.infinity_polling()
    except Exception as e:
        logger.error(f"Bot error: {e}")

# Запускаем бота
bot_thread = threading.Thread(target=run_bot)
bot_thread.daemon = True
bot_thread.start()

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
