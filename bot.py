import sqlite3
import BD
from Bot_Class import Bot


TOKEN = "5986823731:AAGCEnvbGZzYyKvG49PeRt5Caf5mhLTgaUs"
GeoBot = Bot(TOKEN)

@GeoBot.bot.message_handler(commands=['start'])
def say_hello(message):
    BD.ADD_USER(message)
    GeoBot.print_special_message(message.chat.id, "hello")

@GeoBot.bot.callback_query_handler(func=lambda call: True)
def reply_callback_query(call):
    GeoBot.reply_inline_call(call)


@GeoBot.bot.message_handler(commands=['profile'])
def profile_getter(message):
    GeoBot.bot.send_message(message.chat.id, 'Username: ' + BD.Get_Username(message.chat.id))
    GeoBot.bot.send_message(message.chat.id, 'streak: ' + str(BD.Get_Streak(message.chat.id)))

@GeoBot.bot.message_handler(commands=['help'])
def help(message):
    GeoBot.print_special_message(message.chat.id, 'help')

@GeoBot.bot.message_handler(content_types=['text'])
def answer(message):
    if message.text == '/change_username':
        GeoBot.bot.send_message(message.chat.id, 'Введите новый Username')
        GeoBot.bot.register_next_step_handler(message, UU)
    else:
        GeoBot.check_answer(message)
def UU(message):
    BD.Update_Username(message.chat.id, str(message.text))




GeoBot.start()
