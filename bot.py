from Bot_Class import Bot


TOKEN = "5986823731:AAHVMdWsWb_sUjBIbQz4j_1ja_mm41tNkHw"
GeoBot = Bot(TOKEN)

@GeoBot.bot.message_handler(commands=['start'])
def say_hello(message):
    GeoBot.print_special_message(message.chat.id, "hello")

@GeoBot.bot.callback_query_handler(func=lambda call: True)
def reply_callback_query(call):
    GeoBot.reply_inline_call(call)

@GeoBot.bot.message_handler(commands=['help'])
def help(message):
    GeoBot.print_special_message(message.chat.id, 'help')

@GeoBot.bot.message_handler(content_types=['text'])
def answer(message):
    GeoBot.check_answer(message)

GeoBot.start()
