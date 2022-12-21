from Bot_Class import Bot
import BD

TOKEN = "5986823731:AAHVMdWsWb_sUjBIbQz4j_1ja_mm41tNkHw"
GeoBot = Bot(TOKEN)


@GeoBot.bot.message_handler(commands=['start'])
def say_hello(message):
    GeoBot.print_special_message(message.chat.id, "hello", name=message.from_user.first_name)


@GeoBot.bot.callback_query_handler(func=lambda call: True)
def reply_callback_query(call):
    GeoBot.reply_inline_call(call)


@GeoBot.bot.message_handler(commands=['help'])
def help(message):
    GeoBot.print_special_message(message.chat.id, 'help')


@GeoBot.bot.message_handler(commands=['profile'])
def profile_getter(message):
    GeoBot.print_special_message(message.chat.id, 'profile')


@GeoBot.bot.message_handler(commands=['top'])
def top(message):
    GeoBot.print_special_message(message.chat.id, 'top')


@GeoBot.bot.message_handler(commands=['change_username'])
def change_username(message):
    if message.text == '/change_username':
        GeoBot.bot.send_message(message.chat.id, 'Введите новый Username')
        GeoBot.bot.register_next_step_handler(message, UU)
def UU(message):
    BD.update_username(message.chat.id, str(message.text))

@GeoBot.bot.message_handler(content_types=['text'])
def answer(message):
    GeoBot.check_answer(message)


GeoBot.start()
