import os
import telebot
import requests
from flask import Flask
import threading
from bs4 import BeautifulSoup
import logging
import random

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
bot = telebot.TeleBot('8528605880:AAE9FTYavk_p0bBJctDtsiCPF7dSzJHkbjI')

# ===== БАЗА ДАННЫХ ТОВАРОВ С ФОТОГРАФИЯМИ =====
PRODUCTS_DATA = {
    'кроссовки': [
        {
            'title': '🔥 Nike Air Max 2024',
            'price': '4,299 ₽',
            'rating': '4.8/5 ⭐', 
            'reviews': '1,234 отзыва',
            'link': 'https://aliexpress.ru/item/1005005123456.html',
            'image': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&h=400&fit=crop',
            'description': 'Беговые кроссовки премиум-класса'
        },
        {
            'title': '💎 Adidas Ultraboost',
            'price': '3,899 ₽',
            'rating': '4.9/5 ⭐',
            'reviews': '856 отзывов', 
            'link': 'https://aliexpress.ru/item/1005005123457.html',
            'image': 'https://images.unsplash.com/photo-1606107557195-0e29a4b5b4aa?w=400&h=400&fit=crop',
            'description': 'Ультра удобные для повседневной носки'
        },
        {
            'title': '🚀 Puma RS-X',
            'price': '2,999 ₽',
            'rating': '4.7/5 ⭐',
            'reviews': '2,101 отзыв',
            'link': 'https://aliexpress.ru/item/1005005123458.html',
            'image': 'https://images.unsplash.com/photo-1605348532760-6753d2c43329?w=400&h=400&fit=crop',
            'description': 'Стильные кроссовки для города'
        },
        {
            'title': '👟 New Balance 574',
            'price': '3,499 ₽', 
            'rating': '4.6/5 ⭐',
            'reviews': '1,567 отзывов',
            'link': 'https://aliexpress.ru/item/1005005123459.html',
            'image': 'https://images.unsplash.com/photo-1549289524-06cf8837ace5?w=400&h=400&fit=crop',
            'description': 'Классические кроссовки для любого стиля'
        },
        {
            'title': '⚡ Reebok Nano',
            'price': '3,199 ₽',
            'rating': '4.5/5 ⭐',
            'reviews': '892 отзыва',
            'link': 'https://aliexpress.ru/item/1005005123460.html', 
            'image': 'https://images.unsplash.com/photo-1600185365483-26d7a4cc7519?w=400&h=400&fit=crop',
            'description': 'Идеальны для тренировок и фитнеса'
        }
    ],
    'одежда': [
        {
            'title': '👕 Футболка хлопковая',
            'price': '899 ₽',
            'rating': '4.6/5 ⭐',
            'reviews': '3,456 отзывов',
            'link': 'https://aliexpress.ru/item/4001234567890.html',
            'image': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=400&fit=crop',
            'description': '100% хлопок, комфорт в носке'
        },
        {
            'title': '👖 Джинсы классические',
            'price': '1,599 ₽',
            'rating': '4.7/5 ⭐', 
            'reviews': '2,890 отзывов',
            'link': 'https://aliexpress.ru/item/4001234567891.html',
            'image': 'https://images.unsplash.com/photo-1542272604-787c3835535d?w=400&h=400&fit=crop',
            'description': 'Классический крой, премиум качество'
        },
        {
            'title': '🧥 Куртка ветровка',
            'price': '2,299 ₽',
            'rating': '4.5/5 ⭐',
            'reviews': '1,234 отзыва',
            'link': 'https://aliexpress.ru/item/4001234567892.html',
            'image': 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400&h=400&fit=crop', 
            'description': 'Защита от ветра и дождя'
        }
    ],
    'техника': [
        {
            'title': '📱 Смартфон Xiaomi',
            'price': '15,999 ₽', 
            'rating': '4.8/5 ⭐',
            'reviews': '5,678 отзывов',
            'link': 'https://aliexpress.ru/item/5001234567890.html',
            'image': 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400&h=400&fit=crop',
            'description': 'Высокая производительность, отличная камера'
        },
        {
            'title': '🎧 Беспроводные наушники',
            'price': '2,499 ₽',
            'rating': '4.5/5 ⭐',
            'reviews': '4,321 отзыв',
            'link': 'https://aliexpress.ru/item/5001234567891.html',
            'image': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=400&fit=crop',
            'description': 'Качественный звук, шумоподавление'
        },
        {
            'title': '⌚ Умные часы',
            'price': '3,799 ₽',
            'rating': '4.7/5 ⭐',
            'reviews': '2,987 отзывов', 
            'link': 'https://aliexpress.ru/item/5001234567892.html',
            'image': 'https://images.unsplash.com/photo-1544117519-31a4b719223d?w=400&h=400&fit=crop',
            'description': 'Фитнес-трекер, уведомления, стильный дизайн'
        }
    ],
    'косметика': [
        {
            'title': '💄 Помада матовая',
            'price': '459 ₽',
            'rating': '4.7/5 ⭐',
            'reviews': '1,234 отзыва', 
            'link': 'https://aliexpress.ru/item/6001234567890.html',
            'image': 'https://images.unsplash.com/photo-1586495777744-4413f21062fa?w=400&h=400&fit=crop',
            'description': 'Стойкая матовая помада, 12 часов'
        },
        {
            'title': '🧴 Крем для лица',
            'price': '699 ₽',
            'rating': '4.6/5 ⭐',
            'reviews': '2,345 отзывов',
            'link': 'https://aliexpress.ru/item/6001234567891.html',
            'image': 'https://images.unsplash.com/photo-1556228578-8c89e6adf883?w=400&h=400&fit=crop',
            'description': 'Увлажняющий крем с SPF защитой'
        }
    ],
    'дом': [
        {
            'title': '🏠 Набор посуды',
            'price': '2,899 ₽', 
            'rating': '4.8/5 ⭐',
            'reviews': '3,210 отзывов',
            'link': 'https://aliexpress.ru/item/7001234567890.html',
            'image': 'https://images.unsplash.com/photo-1583778176476-4a8b7d6f6b80?w=400&h=400&fit=crop',
            'description': 'Керамический набор 12 предметов'
        },
        {
            'title': '🛏️ Постельное белье',
            'price': '1,299 ₽',
            'rating': '4.5/5 ⭐',
            'reviews': '4,567 отзывов',
            'link': 'https://aliexpress.ru/item/7001234567891.html',
            'image': 'https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?w=400&h=400&fit=crop', 
            'description': '100% хлопок, размер 2.0x2.2'
        }
    ],
    'спорт': [
        {
            'title': '🏃‍♂️ Беговая дорожка',
            'price': '12,999 ₽',
            'rating': '4.7/5 ⭐',
            'reviews': '890 отзывов',
            'link': 'https://aliexpress.ru/item/8001234567890.html',
            'image': 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=400&h=400&fit=crop',
            'description': 'Электрическая, складываемая'
        },
        {
            'title': '⚽ Футбольный мяч',
            'price': '1,299 ₽', 
            'rating': '4.6/5 ⭐',
            'reviews': '2,345 отзывов',
            'link': 'https://aliexpress.ru/item/8001234567891.html',
            'image': 'https://images.unsplash.com/photo-1614632231381-1e717133b3dd?w=400&h=400&fit=crop',
            'description': 'Официальный размер, прочный'
        }
    ]
}

# ===== ПАРСЕР ALIEXPRESS =====
def parse_aliexpress(query):
    """Парсит товары с AliExpress или возвращает демо-данные"""
    try:
        # Здесь будет реальный парсинг
        # Пока используем демо-данные из базы
        return PRODUCTS_DATA.get(query.lower(), get_fallback_products(query))
    except Exception as e:
        logger.error(f"Ошибка парсинга: {e}")
        return get_fallback_products(query)

def get_fallback_products(query):
    """Резервные товары если категория не найдена"""
    return [
        {
            'title': f'🔥 Лучший товар: {query}',
            'price': '2,999 ₽',
            'rating': '4.8/5 ⭐',
            'reviews': '1,000+ отзывов',
            'link': 'https://aliexpress.ru',
            'image': 'https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=400&h=400&fit=crop',
            'description': 'Высокое качество, гарантия'
        }
    ]

# ===== TELEGRAM BOT HANDLERS =====
@bot.message_handler(commands=['start'])
def start(message):
    show_main_menu(message)

def show_main_menu(message):
    """Показывает главное меню с кнопками"""
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    
    # Кнопки меню
    btn1 = telebot.types.KeyboardButton('👟 Обувь')
    btn2 = telebot.types.KeyboardButton('👕 Одежда')
    btn3 = telebot.types.KeyboardButton('📱 Техника')
    btn4 = telebot.types.KeyboardButton('💄 Косметика')
    btn5 = telebot.types.KeyboardButton('🏠 Дом')
    btn6 = telebot.types.KeyboardButton('🏃‍♂️ Спорт')
    btn7 = telebot.types.KeyboardButton('🔍 Поиск товара')
    btn8 = telebot.types.KeyboardButton('ℹ️ О боте')
    
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8)
    
    welcome_text = f"""
🦊 *HunterPrice Bot*

*Добро пожаловать, {message.from_user.first_name}!*

Я помогу найти лучшие товары на AliExpress с фотографиями и описаниями! 

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
        reply_markup=telebot.types.ReplyKeyboardRemove()
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
• Показывать фото и описания
• Сравнивать цены и рейтинги

*💡 Используйте кнопки меню для навигации!*
"""
    bot.send_message(message.chat.id, about_text, parse_mode='Markdown')

@bot.message_handler(func=lambda message: message.text in ['Вернуться в меню', 'Меню'])
def back_to_menu(message):
    """Возврат в главное меню"""
    show_main_menu(message)

def search_products(message, query, display_name):
    """Поиск и отправка товаров с фотографиями"""
    bot.send_message(
        message.chat.id, 
        f"🔍 *Ищем товары:* {display_name}\n\n⏳ *Загружаем фотографии...*", 
        parse_mode='Markdown'
    )
    
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
📦 *{product['description']}*

⚡ *Бесплатная доставка*
🛡️ *Гарантия возврата*
"""
                    
                    inline_markup = telebot.types.InlineKeyboardMarkup()
                    btn_buy = telebot.types.InlineKeyboardButton('🛒 Купить на AliExpress', url=product['link'])
                    inline_markup.add(btn_buy)
                    
                    # Отправляем фото с описанием
                    try:
                        bot.send_photo(
                            message.chat.id,
                            product['image'],
                            caption=caption,
                            reply_markup=inline_markup,
                            parse_mode='Markdown'
                        )
                    except Exception as e:
                        # Если не удалось отправить фото, отправляем текстом
                        logger.error(f"Ошибка отправки фото: {e}")
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
    return "🦊 HunterPrice Bot - Поиск товаров с фото"

@app.route('/health')
def health():
    return "OK"

# ===== ЗАПУСК БОТА =====
def run_bot():
    logger.info("🦊 Starting HunterPrice Bot with photos...")
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
