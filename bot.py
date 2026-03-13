#Код у Захара. На уроке будем смотреть и корректировать при необходимости
from telebot import TeleBot
from logic import *
from config import *
from telebot import types



BOT_TOKEN = 'YOUR_BOT_TOKEN_HERE'


bot = telebot.TeleBot(BOT_TOKEN)

# Месяцы-Праздники
holidays = {
    'январь': ['1 января — Новый год', '7 января — Рождество'],
    'февраль': ['23 февраля — День защитника Отечества'],
    'март': ['8 марта — Международный женский день'],
    'апрель': [],
    'май': ['1 мая — Праздник Весны и Труда', '9 мая — День Победы'],
    'июнь': ['12 июня — День России'],
    'июль': [],
    'август': [],
    'сентябрь': [],
    'октябрь': [],
    'ноябрь': ['4 ноября — День народного единства'],
    'декабрь': []
}

# Сезоны и их месяцы
seasons = {
    'Зима': ['январь', 'февраль', 'декабрь'],
    'Весна': ['март', 'апрель', 'май'],
    'Лето': ['июнь', 'июль', 'август'],
    'Осень': ['сентябрь', 'октябрь', 'ноябрь']
}


@bot.message_handler(commands=['start'])
def start(message):
    # Клавиатура(кнопки)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    season_buttons = [types.KeyboardButton(season) for season in seasons.keys()]
    markup.add(*season_buttons)

    text = "Привет! Я календарь праздников.\n"
    text += "Нажми на сезон, чтобы увидеть месяцы:\n"
    text += "Или напиши /all для всех праздников."
    bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.message_handler(commands=['all'])
def show_all(message):
    result = "Все праздники по месяцам:\n\n"
    for month in holidays:
        result += month.capitalize() + ":\n"
        if len(holidays[month]) == 0:
            result += "  Нет праздников\n"
        else:
            for day in holidays[month]:
                result += "  • " + day + "\n"
        result += "\n"
    bot.send_message(message.chat.id, result)

@bot.message_handler(func=lambda m: m.text in seasons.keys())
def show_months(message):
    season = message.text
    months_list = seasons[season]

    # Клавиатура(с месяцами)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    month_buttons = [types.KeyboardButton(month) for month in months_list]
    markup.add(*month_buttons)

    bot.send_message(
        message.chat.id,
        f"Выбран сезон: {season}. Теперь выбери месяц:",
        reply_markup=markup
    )

@bot.message_handler(func=lambda m: m.text.lower().strip() in holidays.keys())
def handle_month(message):
    user_input = message.text.lower().strip()

    if len(holidays[user_input]) == 0:
        answer = "В " + user_input + " нет праздников."
    else:
        answer = "Праздники в " + user_input + ":\n"
        for item in holidays[user_input]:
            answer += "• " + item + "\n"

    bot.send_message(message.chat.id, answer)

@bot.message_handler(func=lambda m: True)
def handle_other(message):
    answer = "Не понимаю. Нажми на сезон или месяц из кнопок!"
    bot.send_message(message.chat.id, answer)

print("Бот запущен!")
bot.infinity_polling()
