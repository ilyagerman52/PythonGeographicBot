from Bot_Class import Bot


TOKEN = "5986823731:AAGCEnvbGZzYyKvG49PeRt5Caf5mhLTgaUs"
GeoBot = Bot(TOKEN)

@GeoBot.bot.message_handler(commands=['start'])
def func_name(message):
    GeoBot.print_special_message(message.chat.id, "hello")
# @GeoBot.bot.message_handler()
# def func_name1():
#     pass
# @GeoBot.bot.message_handler()
# def func_name2():
#     pass
# @GeoBot.bot.message_handler()
# def func_name3():
#     pass
# @GeoBot.bot.message_handler()
# def func_name4():
#     pass







GeoBot.start()