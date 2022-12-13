import time
import telebot
from telebot import types

from question_generation import generate_question


class Bot:
    """
    c - country
    C - capital
    l - lake
    r - river
    """
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)
        self.bot_username = self.bot.user.username
        self.bot_id = self.bot.user.id
        self.is_waiting = False
        self.waiting_answer = None
        self.premessage = ''

    def print_special_message(self, chat_id, t='unexpected'):
        if t == 'unexpected':
            self.bot.send_message(chat_id, 'Я тебя не понял. Справку можно вызвать командой /help')
        elif t == 'hello':
            markup = types.InlineKeyboardMarkup(row_width=1)
            but_y = types.InlineKeyboardButton(text="Да", callback_data='yes')
            but_n = types.InlineKeyboardButton(text="Посмотреть справку", callback_data='no')
            markup.add(but_y, but_n)
            self.bot.send_message(chat_id, 'Привет! Готов отвечать на вопросы?', reply_markup=markup)

    def reply_inline_call(self, call):
        if call.data == 'no':
            pass
        elif call.data == 'yes':
            message_text = 'Отлично! \n\n Теперь выбери тему.'
            markup = types.InlineKeyboardMarkup(row_width=2)
            but_cC = types.InlineKeyboardButton(text='Назвать столицу', callback_data='cC')
            but_tc = types.InlineKeyboardButton(text='Назвать страну по городу в ней', callback_data='tc')
            markup.add(but_cC, but_tc)
            self.bot.send_message()
    def ask_cC(self, chat_id):
        question, answer = generate_question('cC')
        question = self.premessage + question
        try:
            self.bot.send_message(chat_id, question, parse_mode='HTML')
            self.is_waiting = True
            self.waiting_answer = answer
        except Exception as e:
            print("{!s}\n{!s}".format(type(e), str(e)))

    def check_answer(self, message):
        received_answer = message.text.strip()
        if received_answer == self.waiting_answer:
            self.premessage = 'Верно!'
            self.waiting_answer = None
            self.is_waiting = False

    def reply_inline_call(self, call):
        pass

    def start(self):
        self.bot.polling(none_stop=True, interval=0)

