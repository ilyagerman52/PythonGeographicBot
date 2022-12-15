import time
import telebot
from telebot import types
from dataclasses import dataclass

from question_generation import generate_question
from MESSAGES import *
from create_good_name import good_name


@dataclass
class Chat:
    premessage = ''
    waiting_answer = None
    last_asked_message = None
    streak = 0
    category = None


class Bot:
    """
    c - country
    C - capital
    l - lake
    r - river
    t - town
    cd - country description
    rd - region (from Russia) description
    wthr - weather
    """

    def __init__(self, token):
        self.bot = telebot.TeleBot(token)
        self.bot_username = self.bot.user.username
        self.bot_id = self.bot.user.id
        self.question_types = ['cC', 'tc', 'wthr', 'cd', 'rd']
        self.chats = dict()

    def print_special_message(self, chat_id, t='unexpected'):
        if t == 'unexpected':
            self.bot.send_message(chat_id, UNEXPEXTED)
        elif t == 'hello':
            self.chats[chat_id] = Chat()
            markup = types.InlineKeyboardMarkup(row_width=1)
            but_y = types.InlineKeyboardButton(text="Да", callback_data='yes')
            but_n = types.InlineKeyboardButton(text="Посмотреть справку", callback_data='help')
            markup.add(but_y, but_n)
            self.bot.send_message(chat_id, HELLO_MESSAGE, reply_markup=markup)
        elif t == 'help':
            self.bot.send_message(chat_id, HELP_MESSAGE, )
        elif t == 'choose_category':
            message_text = 'Выбери тему.'
            markup = types.InlineKeyboardMarkup(row_width=1)
            but_cC = types.InlineKeyboardButton(text='Назвать столицу', callback_data='cC')
            but_tc = types.InlineKeyboardButton(text='Назвать страну по городу в ней', callback_data='tc')
            but_wthr = types.InlineKeyboardButton(text='Угадать город по погоде', callback_data='wthr')
            but_cd = types.InlineKeyboardButton(text='Угадать страну по описанию из ЕГЭ', callback_data='cd')
            but_rd = types.InlineKeyboardButton(text='Угадать регион России по описанию из ЕГЭ', callback_data='rd')
            markup.add(but_cC, but_tc, but_wthr, but_cd, but_rd)
            self.bot.send_message(chat_id, message_text, reply_markup=markup)

    def reply_inline_call(self, call):
        chat_id = call.message.chat.id
        if call.data == 'help':
            self.bot.edit_message_reply_markup(call.message.chat.id, call.message.id, reply_markup=None)
            self.print_special_message(chat_id, 'help')
        elif call.data == 'yes':
            self.bot.edit_message_reply_markup(call.message.chat.id, call.message.id, reply_markup=None)
            if chat_id not in self.chats: self.chats[chat_id] = Chat()
            self.chats[chat_id].premessage = 'Отлично!'
            self.print_special_message(chat_id, 'choose_category')
        elif call.data in self.question_types:
            self.bot.edit_message_reply_markup(call.message.chat.id, call.message.id, reply_markup=None)
            if chat_id not in self.chats: self.chats[chat_id] = Chat()
            self.chats[chat_id].category = call.data
            self.ask(chat_id, call.data)
        elif call.data == 'change_category':
            if chat_id not in self.chats: self.chats[chat_id] = Chat()
            self.chats[call.message.chat.id].premessage = ''
            self.chats[call.message.chat.id].waiting_answer = None
            self.chats[call.message.chat.id].category = None
            self.bot.edit_message_reply_markup(call.message.chat.id, call.message.id, reply_markup=None)
            self.print_special_message(chat_id, 'choose_category')
        elif call.data == 'exit':
            if chat_id not in self.chats: self.chats[chat_id] = Chat()
            self.chats[call.message.chat.id].premessage = ''
            self.chats[call.message.chat.id].waiting_answer = None
            self.chats[call.message.chat.id].category = None
            self.bot.edit_message_text('Ответы на вопросы закончились', call.message.chat.id, call.message.id)
            self.bot.edit_message_reply_markup(call.message.chat.id, call.message.id, reply_markup=None)
            pass

    def ask(self, chat_id, category='cC'):
        question, answer = generate_question(category)
        if chat_id not in self.chats: self.chats[chat_id] = Chat()
        question = self.chats[chat_id].premessage + '\n\n' + question
        try:
            markup = types.InlineKeyboardMarkup()
            but_change = types.InlineKeyboardButton(text='Хочу сменить категорию вопросов',
                                                    callback_data='change_category')
            but_exit = types.InlineKeyboardButton(text='Больше не хочу отвечать на вопросы', callback_data='exit')
            markup.add(but_change, but_exit)
            self.bot.send_message(chat_id, question, reply_markup=markup)
            self.chats[chat_id].waiting_answer = answer
        except Exception as e:
            print("{!s}\n{!s}".format(type(e), str(e)))

    def check_answer(self, message):
        chat_id = message.chat.id
        received_answer = good_name(message.text.strip())
        if chat_id not in self.chats: self.chats[chat_id] = Chat()
        if self.chats[chat_id].waiting_answer is None:
            self.print_special_message(message.chat.id, 'unexpected')
        elif (isinstance(self.chats[chat_id].waiting_answer, str)
              and received_answer == good_name(self.chats[chat_id].waiting_answer)) or \
                (received_answer in good_name(self.chats[chat_id].waiting_answer)):
            self.chats[chat_id].premessage = 'Верно!'
            self.chats[chat_id].waiting_answer = None
            self.chats[chat_id].streak += 1
            self.ask(message.chat.id, self.chats[chat_id].category)
        else:
            self.chats[chat_id].premessage = 'Неверно! Правильный ответ: ' + self.chats[chat_id].waiting_answer
            self.chats[chat_id].waiting_answer = None
            self.chats[chat_id].streak = 0
            self.ask(message.chat.id, self.chats[chat_id].category)


    def start(self):
        self.bot.polling(none_stop=True, interval=0)
