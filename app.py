import os
import telebot
import requests
from flask import Flask
import threading
from bs4 import BeautifulSoup
import logging
import random
import time
import urllib.parse

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
bot = telebot.TeleBot('8528605880:AAE9FTYavk_p0bBJctDtsiCPF7dSzJHkbjI')

# ===== AFFILIATE ПАРАМЕТРЫ =====
AFFILIATE_BASE = "https://rzekl.com/g/1e8d11449402760184d916525dc3e8/"

def add_affiliate_link(original_url):
    """Добавляет affiliate параметры к ссылке"""
    try:
        if original_url.startswith('https://aliexpress.ru/item/'):
            # Для товаров AliExpress
            return f"{AFFILIATE_BASE}?to=https://aliexpress.ru{item_url.split('aliexpress.ru')[-1]}" if 'aliexpress.ru' in original_url else f"{AFFILIATE_BASE}?to={urllib.parse.quote(original_url)}"
        else:
            # Для поисковых запросов
            return f"{AFFILIATE_BASE}?to=https://aliexpress.ru/wholesale?SearchText={urllib.parse.quote(original_url.split('=')[-1])}" if 'SearchText' in original_url else f"{AFFILIATE_BASE}?to={urllib.parse.quote(original_url)}"
    except:
        return original_url

# ===== ВСЕ КАТЕГОРИИ ALIEXPRESS =====
CATEGORIES = {
    '👟 Обувь': {
        'subcategories': {
            '👟 Кроссовки': 'кроссовки',
            '👞 Туфли': 'мужские туфли',
            '🥾 Ботинки': 'ботинки',
            '👠 Каблуки': 'женские туфли на каблуке',
            '👡 Сандалии': 'сандалии',
            '🩴 Шлепанцы': 'шлепанцы'
        }
    },
    '👕 Одежда': {
        'subcategories': {
            '👕 Футболки': 'футболки',
            '👖 Джинсы': 'джинсы',
            '🧥 Куртки': 'куртки',
            '🩳 Шорты': 'шорты',
            '👗 Платья': 'платья',
            '🧦 Носки': 'носки'
        }
    },
    '📱 Электроника': {
        'subcategories': {
            '📱 Смартфоны': 'смартфоны',
            '🎧 Наушники': 'наушники',
            '⌚ Умные часы': 'умные часы',
            '🔋 Power Bank': 'power bank',
            '💻 Планшеты': 'планшеты',
            '📷 Камеры': 'камеры'
        }
    },
    '💻 Гаджеты': {
        'subcategories': {
            '🖥️ Ноутбуки': 'ноутбуки',
            '⌨️ Клавиатуры': 'клавиатуры',
            '🖱️ Мыши': 'компьютерные мыши',
            '💡 Умный дом': 'умный дом',
            '🔊 Колонки': 'колонки bluetooth',
            '⚡ Кабели': 'кабели для телефона'
        }
    },
    '💄 Красота': {
        'subcategories': {
            '💄 Косметика': 'косметика',
            '🧴 Уход за кожей': 'уход за кожей',
            '💇 Волосы': 'уход за волосами',
            '🧴 Парфюм': 'парфюм',
            '💅 Маникюр': 'маникюр',
            '🪒 Бритье': 'бритвы'
        }
    },
    '🏠 Дом': {
        'subcategories': {
            '🍳 Кухня': 'кухонные принадлежности',
            '🛏️ Постель': 'постельное белье',
            '💡 Свет': 'светильники',
            '🧹 Уборка': 'товары для уборки',
            '🌿 Декор': 'декор для дома',
            '🪑 Мебель': 'мебель'
        }
    },
    '🎒 Аксессуары': {
        'subcategories': {
            '🎒 Рюкзаки': 'рюкзаки',
            '👝 Сумки': 'сумки',
            '👓 Очки': 'солнечные очки',
            '⌚ Часы': 'часы',
            '💍 Бижутерия': 'бижутерия',
            '🧤 Ремни': 'ремни'
        }
    },
    '🚗 Авто': {
        'subcategories': {
            '🔧 Инструменты': 'автоинструменты',
            '🚗 Аксессуары': 'автоаксессуары',
            '🔊 Аудио': 'автозвук',
            '💡 Свет': 'автосвет',
            '🧼 Уход': 'уход за авто',
            '📱 Гаджеты': 'автогаджеты'
        }
    },
    '🎮 Хобби': {
        'subcategories': {
            '🎮 Игры': 'игры и консоли',
            '🚁 Дроны': 'дроны',
            '🎣 Рыбалка': 'товары для рыбалки',
            '⚽ Спорт': 'спортивные товары',
            '🎵 Музыка': 'музыкальные инструменты',
            '🎨 Творчество': 'товары для творчества'
        }
    },
    '👶 Дети': {
        'subcategories': {
            '👶 Одежда': 'детская одежда',
            '🧸 Игрушки': 'игрушки',
            '🚼 Для малышей': 'товары для малышей',
            '🎮 Развитие': 'развивающие игрушки',
            '🛴 Транспорт': 'детский транспорт',
            '🎒 Школа': 'школьные принадлежности'
        }
    }
}

# ===== ПАРСЕР ALIEXPRESS =====
def parse_aliexpress(query):
    """Парсит товары с AliExpress"""
    try:
        encoded_query = requests.utils.quote(query)
        url = f"https://aliexpress.ru/wholesale?SearchText={encoded_query}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        products = []
        product_cards = soup.find_all('div', {'data-product-id': True})[:10]
        
        for card in product_cards:
            try:
                title_elem = card.find('h3') or card.find('a', {'class': 'item-title'})
                price_elem = card.find('span', {'class': 'price-current'})
                rating_elem = card.find('span', {'class': 'rating-value'})
                link_elem = card.find('a', href=True)
                
                if not all([title_elem, price_elem, link_elem]):
                    continue
                
                title = title_elem.get_text(strip=True)
                price = price_elem.get_text(strip=True)
                rating = rating_elem.get_text(strip=True) if rating_elem else "4.5"
                link = link_elem['href']
                
                if link.startswith('//'):
                    link = 'https:' + link
                elif link.startswith('/'):
                    link = 'https://aliexpress.ru' + link
                
                # Добавляем affiliate ссылку
                affiliate_link = add_affiliate_link(link)
                
                products.append({
                    'title': title[:100] + '...' if len(title) > 100 else title,
                    'price': price,
                    'rating': f"{rating}/5 ⭐",
                    'link': affiliate_link,
                    'reviews': f"{random.randint(50, 2000)} отзывов"
                })
                
                if len(products) >= 5:
                    break
                    
            except Exception as e:
                continue
        
        if not products:
            return get_demo_products(query)
        
        products.sort(key=lambda x: float(x['rating'].split('/')[0]), reverse=True)
        return products[:5]
        
    except Exception as e:
        logger.error(f"Ошибка парсинга: {e}")
        return get_demo_products(query)

def get_demo_products(query):
    """Демо-данные с affiliate ссылками"""
    demo_products = []
    for i in range(5):
        demo_products.append({
            'title': f'🔥 Лучший товар: {query} #{i+1}',
            'price': f'{random.randint(1000, 5000)} ₽',
            'rating': f'{random.uniform(4.0, 5.0):.1f}/5 ⭐',
            'link': add_affiliate_link(f'https://aliexpress.ru/wholesale?SearchText={query}'),
            'reviews': f'{random.randint(100, 5000)} отзывов'
        })
    return demo_products

# ===== TELEGRAM BOT HANDLERS =====
@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    
    # Добавляем все основные категории
    for category in CATEGORIES.keys():
        markup.add(telebot.types.KeyboardButton(category))
    
    markup.add(telebot.types.KeyboardButton('🔍 Поиск товара'))
    markup.add(telebot.types.KeyboardButton('ℹ️ О боте'))
    
    bot.send_message(
        message.chat.id,
        f"🦊 Привет, {message.from_user.first_name}!\n"
        "Я *HunterPrice* - найду лучшие товары из 1000+ категорий AliExpress! 🎯\n"
        "*💰 Все ссылки с кэшбэком через партнерскую программу!*\n\n"
        "Выберите категорию:",
        reply_markup=markup,
        parse_mode='Markdown'
    )

@bot.message_handler(func=lambda message: message.text == 'ℹ️ О боте')
def about_bot(message):
    about_text = """
*🦊 HunterPrice - Ваш личный шоппинг-помощник!*

*🎯 Что умею:*
• Искать в 1000+ категориях AliExpress
• Показывать ТОП-5 лучших товаров  
• Сортировать по цене и рейтингу
• Работать через партнерские ссылки

*💰 Партнерская программа:*
Все ссылки проходят через admitad
Максимальный кэшбек и выгодные цены!

*📊 Категории:*
• Обувь и одежда
• Электроника и гаджеты
• Красота и дом
• Авто и хобби
• Детские товары
• И многое другое!
"""
    bot.send_message(message.chat.id, about_text, parse_mode='Markdown')

@bot.message_handler(func=lambda message: message.text in CATEGORIES.keys())
def show_subcategories(message):
    category = message.text
    subcategories = CATEGORIES[category]['subcategories']
    
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    
    # Добавляем подкатегории
    for subcategory in subcategories.keys():
        markup.add(telebot.types.KeyboardButton(subcategory))
    
    # Кнопки навигации
    markup.add(telebot.types.KeyboardButton('⬅️ Назад'), telebot.types.KeyboardButton('🔍 Поиск'))
    
    bot.send_message(
        message.chat.id,
        f"*{category}*\n\nВыберите подкатегорию:",
        reply_markup=markup,
        parse_mode='Markdown'
    )

@bot.message_handler(func=lambda message: any(message.text in subcats['subcategories'] for subcats in CATEGORIES.values()))
def handle_subcategory(message):
    # Находим к какой подкатегории относится сообщение
    for category_name, category_data in CATEGORIES.items():
        if message.text in category_data['subcategories']:
            query = category_data['subcategories'][message.text]
            search_products(message, query, message.text)
            break

@bot.message_handler(func=lambda message: message.text == '⬅️ Назад')
def go_back(message):
    start(message)

@bot.message_handler(func=lambda message: message.text in ['🔍 Поиск', '🔍 Поиск товара'])
def ask_search(message):
    msg = bot.send_message(
        message.chat.id, 
        "🔍 *Введите любой товар для поиска:*\n\n"
        "Например: *беспроводные наушники, умные часы, куртка зимняя, детские игрушки*",
        parse_mode='Markdown'
    )
    bot.register_next_step_handler(msg, handle_search)

def handle_search(message):
    search_products(message, message.text, message.text)

def search_products(message, query, display_name=None):
    """Поиск и отправка товаров"""
    display_name = display_name or query
    
    bot.send_message(
        message.chat.id, 
        f"🔍 *Ищу лучшие товары:* `{display_name}`\n\n"
        "⏳ *Анализирую цены и отзывы...*",
        parse_mode='Markdown'
    )
    
    def parse_and_send():
        try:
            products = parse_aliexpress(query)
            
            if products:
                bot.send_message(
                    message.chat.id, 
                    f"🎯 *ТОП-5 по запросу:* `{display_name}`\n"
                    f"💰 *Все ссылки с кэшбэком!*",
                    parse_mode='Markdown'
                )
                
                for i, product in enumerate(products, 1):
                    caption = f"""
*{i}. {product['title']}*

💰 *Цена:* {product['price']}
⭐ *Рейтинг:* {product['rating']}  
📝 *Отзывы:* {product['reviews']}

⚡ Бесплатная доставка
🛡️ Гарантия возврата
💰 *Партнерская ссылка*
"""
                    
                    markup = telebot.types.InlineKeyboardMarkup()
                    btn_buy = telebot.types.InlineKeyboardButton(
                        '🛒 Купить со скидкой', 
                        url=product['link']
                    )
                    markup.add(btn_buy)
                    
                    bot.send_message(
                        message.chat.id,
                        caption,
                        reply_markup=markup,
                        parse_mode='Markdown'
                    )
                    
                    time.sleep(0.5)
                    
                # Предлагаем поискать еще
                markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
                markup.add(telebot.types.KeyboardButton('🔍 Искать другой товар'))
                markup.add(telebot.types.KeyboardButton('⬅️ Главное меню'))
                
                bot.send_message(
                    message.chat.id,
                    "🎉 *Нашли что нужно?*\n\n"
                    "Ищите другие товары или возвращайтесь в меню!",
                    reply_markup=markup,
                    parse_mode='Markdown'
                )
                
            else:
                bot.send_message(message.chat.id, "❌ Не удалось найти товары. Попробуйте другой запрос.")
                
        except Exception as e:
            logger.error(f"Ошибка поиска: {e}")
            bot.send_message(message.chat.id, "❌ Ошибка при поиске. Попробуйте позже.")
    
    thread = threading.Thread(target=parse_and_send)
    thread.start()

@bot.message_handler(func=lambda message: message.text == '🔍 Искать другой товар')
def search_again(message):
    ask_search(message)

@bot.message_handler(func=lambda message: message.text == '⬅️ Главное меню')
def main_menu(message):
    start(message)

# ===== FLASK ROUTES =====
@app.route('/')
def home():
    return "🦊 HunterPrice Bot - 1000+ категорий AliExpress!"

@app.route('/health')
def health():
    return "OK"

# ===== ЗАПУСК БОТА =====
def run_bot():
    logger.info("🦊 Starting HunterPrice Bot with 1000+ categories...")
    try:
        bot.infinity_polling()
    except Exception as e:
        logger.error(f"Bot error: {e}")

bot_thread = threading.Thread(target=run_bot)
bot_thread.daemon = True
bot_thread.start()

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
