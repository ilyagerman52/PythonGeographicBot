import random
import time
import telebot
from telebot import types
from dataclasses import dataclass

from question_generation import generate_question
from utils import good_name

@dataclass
class Chat:
    premessage = ''
    waiting_answer = None
    streak = 0
    category = None
    ans_hidden = True


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
    flg - flag
    brd - shape (borders)
    """

    def __init__(self, token):
        self.bot = telebot.TeleBot(token)
        self.bot_username = self.bot.user.username
        self.bot_id = self.bot.user.id
        self.question_types = ['cC', 'tc', 'wthr', 'cd', 'rd', 'flg', 'brd', 'rnd']
        self.chats = dict()

    def print_special_message(self, chat_id, t='unexpected'):
        if t == 'unexpected':
            self.bot.send_message(chat_id, 'Я тебя не понял. Справку можно вызвать командой /help .')
        elif t == 'hello':
            self.chats[chat_id] = Chat()
            markup = types.InlineKeyboardMarkup(row_width=1)
            but_y = types.InlineKeyboardButton(text="Да", callback_data='yes')
            but_n = types.InlineKeyboardButton(text="Посмотреть справку", callback_data='help')
            markup.add(but_y, but_n)
            self.bot.send_message(chat_id, 'Привет, неудачник! Готов отвечать на вопросы?', reply_markup=markup)
        elif t == 'help':
            markup = types.InlineKeyboardMarkup()
            but_start = types.InlineKeyboardButton(text='Начать', callback_data='change_category')
            markup.add(but_start)
            self.bot.send_photo(chat_id, photo='https://raw.githubusercontent.com/ilyagerman52/PythonGeographicBot/main/img.png', reply_markup=markup)
        elif t == 'choose_category':
            message_text = 'Выбери тему.'
            markup = types.InlineKeyboardMarkup(row_width=1)
            but_cC = types.InlineKeyboardButton(text='Назвать столицу', callback_data='cC')
            but_tc = types.InlineKeyboardButton(text='Назвать страну по городу в ней', callback_data='tc')
            but_wthr = types.InlineKeyboardButton(text='Угадать город по погоде', callback_data='wthr')
            but_cd = types.InlineKeyboardButton(text='Угадать страну по описанию из ЕГЭ', callback_data='cd')
            but_rd = types.InlineKeyboardButton(text='Угадать регион России по описанию из ЕГЭ', callback_data='rd')
            but_flg = types.InlineKeyboardButton(text='Угадать страну по флагу', callback_data='flg')
            but_brd = types.InlineKeyboardButton(text='Угадать страну по очертаниям', callback_data='brd')
            but_rnd = types.InlineKeyboardButton(text='Случайные вопросы', callback_data='rnd')
            but_vars = types.InlineKeyboardButton(text='Добавить/убрать варианты ответа', callback_data='change_vars')
            markup.add(but_cC, but_tc, but_wthr, but_cd, but_rd, but_flg, but_brd, but_rnd, but_vars)
            self.bot.send_message(chat_id, message_text, reply_markup=markup)

    def reply_inline_call(self, call):
        chat_id = call.message.chat.id
        if chat_id not in self.chats: self.chats[chat_id] = Chat()
        if call.data == 'help':
            self.bot.edit_message_reply_markup(call.message.chat.id, call.message.id, reply_markup=None)
            self.print_special_message(chat_id, 'help')
        elif call.data == 'yes':
            self.bot.edit_message_reply_markup(call.message.chat.id, call.message.id, reply_markup=None)
            self.chats[chat_id].premessage = 'Отлично!'
            self.print_special_message(chat_id, 'choose_category')
        elif call.data == 'change_vars':
            self.chats[chat_id].ans_hidden = not self.chats[chat_id].ans_hidden
            self.bot.edit_message_reply_markup(call.message.chat.id, call.message.id, reply_markup=None)
            if self.chats[chat_id].ans_hidden:
                self.bot.edit_message_text('Варианты ответа выключены')
            else:
                self.bot.edit_message_text('Варианты ответа включены')
            self.print_special_message(chat_id, 'choose_category')
        elif call.data == 'correct_ans':
            self.chats[chat_id].premessage = 'Верно!'
            self.ask(call.message.chat.id, self.chats[chat_id].category, self.chats[chat_id].ans_hidden)
        elif call.data == 'wrong_ans':
            self.chats[chat_id].premessage = 'Неверно! Правильный ответ: ' + self.chats[chat_id].waiting_answer
            self.ask(call.message.chat.id, self.chats[chat_id].category, self.chats[chat_id].ans_hidden)
        elif call.data in self.question_types:
            self.bot.edit_message_reply_markup(chat_id, call.message.id, reply_markup=None)
            self.chats[chat_id].category = call.data
            self.ask(chat_id, call.data, self.chats[chat_id].ans_hidden)
        elif call.data == 'change_category':
            self.chats[chat_id].premessage = ''
            self.chats[chat_id].waiting_answer = None
            self.chats[chat_id].category = None
            self.bot.edit_message_reply_markup(chat_id, call.message.id, reply_markup=None)
            self.print_special_message(chat_id, 'choose_category')
        elif call.data == 'exit':
            self.bot.send_message(chat_id, 'А придётся!')
            self.chats[chat_id].premessage = ''
            self.chats[chat_id].waiting_answer = None
            self.chats[chat_id].category = None
            time.sleep(1)
            self.ask(chat_id, self.chats[chat_id].category, self.chats[chat_id].ans_hidden)

    def ask(self, chat_id, category='cC', ans_hidden=False):
        if category is None: category = 'cC'
        if chat_id not in self.chats: self.chats[chat_id] = Chat()
        question, answer, vars = generate_question(category)
        question_image = question
        question = self.chats[chat_id].premessage + '\n\n' + question
        markup = types.InlineKeyboardMarkup(row_width=2)
        but_change = types.InlineKeyboardButton(text='Хочу сменить категорию вопросов',
                                                callback_data='change_category')
        but_exit = types.InlineKeyboardButton(text='Больше не хочу отвечать на вопросы', callback_data='exit')
        if not ans_hidden and category not in ['cd', 'rd']:
            but_correct = types.InlineKeyboardButton(text=answer, callback_data='correct_ans')
            but_vars = [but_correct]
            for var in vars:
                new_but = types.InlineKeyboardButton(text=var, callback_data='wrong_ans')
                but_vars.append(new_but)
            random.shuffle(but_vars)
            markup.add(*but_vars)
        self.chats[chat_id].waiting_answer = answer
        markup.add(but_change)
        markup.add(but_exit)
        if category in ['flg', 'brd']:
            self.bot.send_photo(chat_id, photo=question_image, caption=self.chats[chat_id].premessage + '\nУгадайте страну:', reply_markup=markup)
        else:
            self.bot.send_message(chat_id, question, reply_markup=markup)


    def check_answer(self, message):
        chat_id = message.chat.id
        received_answer = good_name(message.text.strip())
        if chat_id not in self.chats: self.chats[chat_id] = Chat()
        if self.chats[chat_id].waiting_answer is None:
            self.print_special_message(message.chat.id, 'unexpected')
        elif (isinstance(self.chats[chat_id].waiting_answer, str)
              and received_answer == good_name(self.chats[chat_id].waiting_answer)) or \
                (received_answer in good_name(self.chats[chat_id].waiting_answer).split('|')):
            self.chats[chat_id].premessage = 'Верно!'
            self.chats[chat_id].waiting_answer = None
            self.chats[chat_id].streak += 1
            self.ask(message.chat.id, self.chats[chat_id].category, self.chats[chat_id].ans_hidden)
        else:
            self.chats[chat_id].premessage = 'Неверно! Правильный ответ: ' + self.chats[chat_id].waiting_answer
            self.chats[chat_id].waiting_answer = None
            self.chats[chat_id].streak = 0
            self.ask(message.chat.id, self.chats[chat_id].category, self.chats[chat_id].ans_hidden)

    def start(self):
        self.bot.polling(none_stop=True, interval=0)
