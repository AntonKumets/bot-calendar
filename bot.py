from telebot import TeleBot
from logic import *
from confic import *
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import sqlite3

bot = TeleBot(token)

db = Calendar("holidays.db")
db.create_tables()
db.fill_holidays()
db.fill_seasons()

months_names = {
    1: "Январь", 2: "Февраль", 3: "Март", 4: "Апрель",
    5: "Май", 6: "Июнь", 7: "Июль", 8: "Август",
    9: "Сентябрь", 10: "Октябрь", 11: "Ноябрь", 12: "Декабрь"
}

def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 4
    markup.add(
        InlineKeyboardButton("Зима", callback_data="winter"),
        InlineKeyboardButton("Весна", callback_data="spring"),
        InlineKeyboardButton("Лето", callback_data="summer"),
        InlineKeyboardButton("Осень", callback_data="autumn")
    )
    return markup

@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(
        message.chat.id,
        "Привет! Это бот-календарь, нажимай кнопку нужного времени года, затем нужного месяца, и тебе покажутся все праздники этого месяца.\nДля перезапуска или выбора нового месяца жми /start",
        reply_markup=gen_markup()
    )

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    bot.answer_callback_query(call.id)
    
    if call.data in ["winter", "spring", "summer", "autumn"]:
        season_map = {
            "winter": "Зима",
            "spring": "Весна",
            "summer": "Лето",
            "autumn": "Осень"
        }
        season_ru = season_map[call.data]
        
        conn = sqlite3.connect(db.db_name)
        cur = conn.cursor()
        cur.execute("SELECT month_id FROM season WHERE season = ?", (season_ru,))
        month_ids = cur.fetchall()
        conn.close()
        
        markup = InlineKeyboardMarkup()
        for (month_id,) in month_ids:
            markup.add(InlineKeyboardButton(
                months_names[month_id],
                callback_data=f"month_{month_id}"
            ))
        
        bot.edit_message_text(
            "Выберите месяц:",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=markup
        )
    
    elif call.data.startswith("month_"):
        month_id = int(call.data.split("_")[1])
        
        conn = sqlite3.connect(db.db_name)
        cur = conn.cursor()
        cur.execute("SELECT holidays FROM holidays WHERE month_id = ?", (month_id,))
        row = cur.fetchone()
        conn.close()
        
        if row:
            holidays_text = row[0]
            bot.send_message(call.message.chat.id, f"{months_names[month_id]}:\n{holidays_text}")
        else:
            bot.send_message(call.message.chat.id, "Праздники не найдены.")

bot.infinity_polling(none_stop=True)
        row = cur.fetchone()
        conn.close()

bot.infinity_polling(none_stop=True)
