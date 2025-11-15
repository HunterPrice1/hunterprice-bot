import telebot
import time

bot = telebot.TeleBot('8528605880:AAE9FTYavk_p0bBJctDtsiCPF7dSzJHkbjI')

@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton('👟 Кроссовки')
    markup.add(btn1)
    
    bot.send_message(message.chat.id, "🦊 Привет! Я работаю!", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == '👟 Кроссовки')
def sneakers(message):
    bot.send_message(message.chat.id, "🔍 Ищу кроссовки...")

print("🦊 Bot STARTED!")
bot.infinity_polling()
