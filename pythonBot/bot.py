import asyncio

from Bot_Class import Bot
import profiles

TOKEN = "5986823731:AAHVMdWsWb_sUjBIbQz4j_1ja_mm41tNkHw"
GeoBot = Bot(TOKEN)


@GeoBot.dp.message_handler(commands=['start'])
async def say_hello(message):
    await GeoBot.print_special_message(message.chat.id, "hello", name=message.from_user.first_name)


@GeoBot.dp.callback_query_handler()
async def reply_callback_query(call):
    await GeoBot.reply_inline_call(call)


@GeoBot.dp.message_handler(commands=['help'])
async def help(message):
    await GeoBot.print_special_message(message.chat.id, 'help')


@GeoBot.dp.message_handler(commands=['profile'])
async def profile_getter(message):
    await GeoBot.print_special_message(message.chat.id, 'profile')


@GeoBot.dp.message_handler(commands=['top'])
async def top(message):
    await GeoBot.print_special_message(message.chat.id, 'top')


@GeoBot.dp.message_handler(commands=['change_username'])
async def change_username(message):
    await GeoBot.bot.send_message(message.chat.id, 'Введите новый Username')
    GeoBot.username_reqeust = True


async def UU(message):
    profiles.update_username(message.chat.id, str(message.text))


@GeoBot.dp.message_handler(content_types=['text'])
async def answer(message):
    if GeoBot.username_reqeust:
        await UU(message)
        GeoBot.username_reqeust = False
    else:
        await GeoBot.check_answer(message)


async def main():
    await GeoBot.start()


if __name__ == "__main__":
    asyncio.run(main())
