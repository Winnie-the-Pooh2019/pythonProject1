import telebot
import requests as r
from telebot import types

if __name__ == '__main__':
    print("hi")

token = "5244855984:AAFpKobreUhyb8IG5OVq30uGgAarKyj3Mw4"
bot = telebot.TeleBot(token)

language = 'en'

items = [
    ("Что почитать?", ["https://habr.com/ru/all", "https://medium.com/tag/software-engineering"]),
    ("Форумы", ["https://stackoverflow.com/", "https://ru.stackoverflow.com/"]),
    ("Новости индустрии", ["https://4pda.to/", "https://www.ixbt.com/"])
]


@bot.message_handler(commands=['start'])
def start_messaging(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for item in items:
        button = types.KeyboardButton(item[0])
        markup.add(button)

    bot.send_message(message.chat.id, 'Выберите что вам надо', reply_markup=markup)


@bot.message_handler(content_types='text')
def message_reply(message):
    for item in items:
        if message.text == item[0]:
            for text in item[1]:
                bot.send_message(message.chat.id, text)
            return

    bot.send_message(message.chat.id, "Не понимаю")


@bot.message_handler(commands=['weather'])
def weather(message):
    bot.send_message(message.chat.id, 'Введите город')
    bot.register_next_step_handler(message, get_weather)


def get_weather(message):
    city = message.text
    url = f"https://api.openweathermap.org/data/2.5/forecast?appid=b7eedb84f15757c5da8941a00663136d&units=metric&lang=ru&q={city}"

    response = r.get(url).json()
    weathers = response['list']
    count = int(response['cnt'])
    bot.send_message(message.chat.id, f"""Погода в городе {city}
на момент {weathers[count - 1]["dt_txt"]}
температура: {weathers[count - 1]["main"]["temp"]}
влажность: {weathers[count - 1]["main"]["temp"]}
ощущения: {weathers[count - 1]["main"]["humidity"]}
скорость ветра: {weathers[count - 1]["wind"]["speed"]}""")


bot.polling()
