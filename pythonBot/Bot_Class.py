import random
from dataclasses import dataclass
import aiogram
from aiogram import Dispatcher, types

from question_generation import generate_question
from utils import good_name, HELP_MESSAGE, UNEXPEXTED
import profiles


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
        self.bot = aiogram.Bot(token)
        self.dp = Dispatcher(self.bot)
        self.username_reqeust = False
        # self.bot_username = self.bot.user.username
        # self.bot_id = self.bot.user.id
        self.question_types = ['cC', 'tc', 'wthr', 'cd', 'rd', 'flg', 'brd', 'rnd']
        self.chats = dict()

    async def print_special_message(self, chat_id, t='unexpected', name='неудачник'):
        if t == 'unexpected':
            await self.bot.send_message(chat_id, UNEXPEXTED)
        elif t == 'hello':
            profiles.add_user(chat_id)
            self.chats[chat_id] = Chat()
            markup = types.InlineKeyboardMarkup(row_width=1)
            but_y = types.InlineKeyboardButton(text="Да", callback_data='start_q')
            but_n = types.InlineKeyboardButton(text="Посмотреть справку", callback_data='help')
            markup.add(but_y, but_n)
            await self.bot.send_message(chat_id, f'Привет, {name}! Готов отвечать на вопросы?', reply_markup=markup)
        elif t == 'help':
            markup = types.InlineKeyboardMarkup()
            but_start = types.InlineKeyboardButton(text='Начать', callback_data='change_category')
            markup.add(but_start)
            await self.bot.send_message(chat_id, HELP_MESSAGE, parse_mode='html')
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
            await self.bot.send_message(chat_id, message_text, reply_markup=markup)
        elif t == 'profile':
            name, streak, max_streak, total_answers, correct_answers, accuracy, rating = profiles.get_stats(chat_id)
            await self.bot.send_message(chat_id, f'Имя пользователя: {name}'
                                                 f'\nРейтинг: {rating}'
                                                 f'\nВсего ответов: {total_answers}'
                                                 f'\nВерных ответов: {correct_answers}'
                                                 f'\nПроцент верных ответов: {accuracy}%'
                                                 f'\nМаксимальный стрик: {max_streak}'
                                                 f'\nСтрик сейчас: {streak}')
        elif t == 'top':
            leader = profiles.leader()
            s = str('TOP:' + '\n')
            i = 1
            for user in leader:
                s += str(i) + '. ' + user[0] + '\n        Рейтинг: ' + str(user[6]) + \
                                '\n        Всего ответов: ' + str(user[3]) + \
                                '\n        Процент верных ответов: ' + str(user[5]) + \
                                '%\n        Максимальный стрик: ' + str(user[2]) + '\n'
                i += 1
            await self.bot.send_message(chat_id, s)

    async def reply_inline_call(self, call):
        chat_id = call.message.chat.id
        if chat_id not in self.chats:
            self.chats[chat_id] = Chat()
        if call.data == 'help':
            await self.bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
            await self.print_special_message(chat_id, 'help')
        elif call.data == 'start_q':
            await self.bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
            self.chats[chat_id].premessage = 'Отлично!'
            await self.print_special_message(chat_id, 'choose_category')
        elif call.data == 'change_vars':
            self.chats[chat_id].ans_hidden = not self.chats[chat_id].ans_hidden
            await self.bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
            if self.chats[chat_id].ans_hidden:
                await self.bot.edit_message_text('Варианты ответа выключены', call.message.chat.id,
                                                 call.message.message_id)
            else:
                await self.bot.edit_message_text('Варианты ответа включены', call.message.chat.id,
                                                 call.message.message_id)
            await self.print_special_message(chat_id, 'choose_category')
        elif call.data == 'correct_ans':
            profiles.update_stats(chat_id, 1)
            self.chats[chat_id].premessage = 'Верно!'
            await self.ask(call.message.chat.id, self.chats[chat_id].category, self.chats[chat_id].ans_hidden)
        elif call.data == 'wrong_ans':
            profiles.update_stats(chat_id, 0)
            self.chats[chat_id].premessage = 'Неверно! Правильный ответ: ' + self.chats[chat_id].waiting_answer
            await self.ask(call.message.chat.id, self.chats[chat_id].category, self.chats[chat_id].ans_hidden)
        elif call.data in self.question_types:
            await self.bot.edit_message_reply_markup(chat_id, call.message.message_id, reply_markup=None)
            self.chats[chat_id].category = call.data
            await self.ask(chat_id, call.data, self.chats[chat_id].ans_hidden)
        elif call.data == 'change_category':
            self.chats[chat_id].premessage = ''
            self.chats[chat_id].waiting_answer = None
            self.chats[chat_id].category = None
            await self.bot.edit_message_reply_markup(chat_id, call.message.message_id, reply_markup=None)
            await self.print_special_message(chat_id, 'choose_category')
        elif call.data == 'exit':
            await self.bot.send_message(chat_id, 'А придётся!')
            self.chats[chat_id].premessage = ''
            self.chats[chat_id].waiting_answer = None
            self.chats[chat_id].category = None
            await self.ask(chat_id, self.chats[chat_id].category, self.chats[chat_id].ans_hidden)

    async def ask(self, chat_id, category='cC', ans_hidden=False):
        if category is None:
            category = 'cC'
        if chat_id not in self.chats:
            self.chats[chat_id] = Chat()
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
            if self.chats[chat_id].premessage != '':
                await self.bot.send_message(chat_id, self.chats[chat_id].premessage)
            await self.bot.send_photo(chat_id, photo=question_image, caption='Угадайте страну:', reply_markup=markup)
        else:
            await self.bot.send_message(chat_id, question, reply_markup=markup)

    async def check_answer(self, message):
        chat_id = message.chat.id
        received_answer = good_name(message.text.strip())
        if chat_id not in self.chats:
            self.chats[chat_id] = Chat()
        if self.chats[chat_id].waiting_answer is None:
            await self.print_special_message(message.chat.id, 'unexpected')
        elif (isinstance(self.chats[chat_id].waiting_answer, str)
              and received_answer == good_name(self.chats[chat_id].waiting_answer)) or \
                (received_answer in good_name(self.chats[chat_id].waiting_answer).split('|')):
            profiles.update_stats(chat_id, 1)
            self.chats[chat_id].premessage = 'Верно!'
            self.chats[chat_id].waiting_answer = None
            self.chats[chat_id].streak += 1
            await self.ask(message.chat.id, self.chats[chat_id].category, self.chats[chat_id].ans_hidden)
        else:
            profiles.update_stats(chat_id, 0)
            self.chats[chat_id].premessage = 'Неверно! Правильный ответ: ' + self.chats[chat_id].waiting_answer
            self.chats[chat_id].waiting_answer = None
            self.chats[chat_id].streak = 0
            await self.ask(message.chat.id, self.chats[chat_id].category, self.chats[chat_id].ans_hidden)

    async def start(self):
        await self.dp.start_polling(self.bot)
