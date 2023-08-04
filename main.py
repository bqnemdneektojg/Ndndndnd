import logging
import asyncio
import random
import sqlite3
import json
import os
import time
import requests
from aiogram import Bot, Dispatcher, executor, types
from config import bot_token, admin, CHANNEL_ID, logs
import keyboards as kb
from faker import Faker
from onesec_api import Mailbox
import defaut as key
from states import CellarImport, dialog, linkTamer, IsPrivate
from os.path import exists
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from urllib import response

storage = MemoryStorage()
logging.basicConfig(level=logging.INFO)
bot = Bot(token=bot_token)
dp = Dispatcher(bot, storage=storage)
connection = sqlite3.connect('db.db')
q = connection.cursor()
q.execute("""CREATE TABLE IF NOT EXISTS "users" (
    "user_id"   INTEGER,
    "block" TEXT
);""")
q.execute("""CREATE TABLE IF NOT EXISTS "favorites" (
    "user_id"   INTEGER,
    "message"   TEXT
);""")
connection.commit()
    

async def anti_flood(*args, **kwargs): # сообщение антифлуда
    m = args[0]
    await m.answer(f"<b>💭 Looks like you already pressed start\nPlease try again in a few seconds 🕐</b>", #
    parse_mode="html"
    ) 

def check_sub_channel(chat_member): # проверка подписки на канал
    if chat_member['status'] != 'left':
        return True
    else:
        return False


NOTSUB_MESSAGE="🕷️ Что бы продолжить, необходимо подписаться на канал\n🕸️ Там будут публиковаться новости\n" #


@dp.callback_query_handler(text='del') # удаление сообщений
async def _update_(query: types.CallbackQuery):
    await bot.delete_message(query.from_user.id, query.message.message_id)

@dp.callback_query_handler(lambda c: c.data == 'get_mail') # создание временной почты
async def get_mail(callback_query: types.CallbackQuery):
    ma = Mailbox('')
    email = f'{ma._mailbox_}@dcctb.com'
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    new_msg = await bot.send_message(callback_query.from_user.id, 
        '<b>💣 Ваша почта:</b> {}\n'
        '🐦‍⬛<i>Почта проверяется все время, вам придет сообщение сразу же, после получение письма</i>\n\n'
        🪰 <b>Время действия почты - 12 минут</b>'.format(email), 
        parse_mode='HTML', 
        reply_markup=kb.deleted()
        )
    timeout = 720
    timer = {}
    timeout_start = time.time()
    while time.time() < timeout_start + timeout:
        test = 0
        if test == 5:
            break
        test -= 1
        mb = ma.filtred_mail()
        if mb != 'not found':
            for i in mb:
                if i not in timer:
                    timer[i] = i
                    if isinstance(mb, list):
                        mf = ma.mailjobs('read', mb[0])
                        js = mf.json()
                        fromm = js['from']
                        theme = js['subject']
                        mes = js['textBody']
                        data_time = js['date']
                        id_message = js['id']           
                        global messagetofavorite
                        messagetofavorite = f'<b>Message id: #{id_message}\nFrom</b>: <code>{fromm}</code>\n<b>Subject</b>: <code>{theme}</code>\n<b>Date: <code>{data_time}</code>\nMessage</b>: <code>{mes}</code> '
                        await bot.send_message(callback_query.from_user.id, f'<b>🕷️ Новое сообщение: </b>\n<b>Айди: <code> {id_message}</code>\Отправитель </b>: <code>{fromm}</code>\n<b>Обьект</b>: <code>{theme}</code>\n<b>D: <code>{data_time}</code>\nСообщение</b>: <code>{mes}</code>', 
                        parse_mode='HTML', 
                         
                        reply_markup=kb.deleted()
                        )
                        continue
        await asyncio.sleep(0.0)

@dp.callback_query_handler(lambda c: c.data == 'favorite') # сохранение письма в избранное
async def favorite_cb(callback_query: types.CallbackQuery):
    global messagetofavorite
    q.execute(f"""INSERT INTO "main"."favorites"("user_id","message") VALUES ("{callback_query.from_user.id}","{messagetofavorite}");""")
    connection.commit()
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    await bot.send_message(callback_query.from_user.id, '🕸️ Сообщение добавлено в избранное', 
    reply_markup=kb.deleted()
    )


@dp.callback_query_handler(lambda c: c.data == 'cfavorites') # избранное
async def checkfavorites(callback_query: types.CallbackQuery):
    messages = q.execute(f"""SELECT "message" FROM "main"."favorites" WHERE "user_id"={callback_query.from_user.id}""").fetchall()
    messages = [item for t in messages for item in t]
    messages = '\n\n'.join(messages)
    await bot.send_message(callback_query.from_user.id, text=f"🕷️ Избранное: \n {messages}",
    parse_mode='html', 
    reply_markup=kb.deleted()
    )


@dp.callback_query_handler(lambda c: c.data == 'password') # генератор паролей
async def process_callback_button1(callback_query: types.CallbackQuery):
    ma = Mailbox('')
    passw = ma.rand_pass_for()
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    await bot.send_message(callback_query.from_user.id, f'*🎓 Готовый пароль *`{passw}`\n\n', 
    parse_mode='MarkdownV2', 
    reply_markup=kb.deleted()
    )


@dp.message_handler(IsPrivate(), commands=['admin', "adm", "a"]) # админка
async def adminstration_menu(msg: types.Message):
    if msg.chat.id == admin:
        await msg.answer('<b>welcome</b>', 
        parse_mode='html',
        reply_markup=kb.admin_panel()
        )


@dp.callback_query_handler(text="subchanneldone") # есои человек подписан
async def subchanneldone(message: types.Message):
        await bot.delete_message(message.from_user.id, message.message.message_id)
        if check_sub_channel(await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=message.from_user.id)):
                await bot.send_message(message.from_user.id, f"🕷️ Приветствую, {message.from_user.mention}\n", 
                reply_markup=kb.main_menu()
                )
        else:
                await bot.send_message(message.from_user.id, NOTSUB_MESSAGE, 
                reply_markup=kb.btnCheck()
                )


@dp.message_handler(IsPrivate(), commands=['start']) # стартовый хэндрер
async def texthandler(msg: types.Message):
    q.execute(f"SELECT * FROM users WHERE user_id = {msg.chat.id}")
    result = q.fetchall()
    if len(result) == 0:
        uid = 'user_id'
        sql = 'INSERT INTO users ({}) VALUES ({})'.format(uid, msg.chat.id)
        q.execute(sql)
        connection.commit()
    if check_sub_channel(await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=msg.from_user.id)):
            await bot.send_message(msg.from_user.id, f'<b>🕷️ Приветствую, {msg.from_user.mention}</>\n', 
            parse_mode='html', 
            reply_markup=kb.main_menu()
            )
    else:
            await bot.send_message(msg.from_user.id, NOTSUB_MESSAGE, 
            reply_markup=kb.btnCheck()
            )


@dp.callback_query_handler(lambda call: call.data.startswith('stats')) # статистика
async def statistics(call):
    re = q.execute(f'SELECT * FROM users').fetchall()
    kol = len(re)
    connection.commit()
    await call.message.answer(f'<b>🐦‍⬛ Количество юзеров: {kol}</b>', 
    parse_mode='html', 
    reply_markup=kb.deleted()
    )

@dp.callback_query_handler(lambda call: call.data.startswith('rass')) # сообщение для начала рассылки
async def usender(call):
    await call.message.answer('<b>💣 Напиши сюда текст для рассылки</b>', 
    parse_mode='html',
    reply_markup=kb.deleted()
    )
    await CellarImport.rasst.set()

@dp.callback_query_handler(lambda call: call.data.startswith('reboot')) # Перезагрузка
async def usender(call):
    os.system("python main.py")
    await call.message.answer('successfully!')

@dp.message_handler(state=CellarImport.rasst) # Рассылка
async def process_name(message: types.Message, state: FSMContext):
    q.execute(f'SELECT user_id FROM users')
    row = q.fetchall()
    connection.commit()
    if message.text == 'cancellation':
        await message.answer('cancellation!', 
        reply_markup=kb.ReplyKeyboardRemove()
        )
        await state.finish()
    else:
        info = row
        await message.answer('I start mailing...')
        for i in range(len(info)):
            try:
                await bot.send_message(info[i][0], str(message.html_text), 
                reply_markup=kb.deleted()
                )
            except:
                pass
        await message.answer('Newsletter completed.')
        await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True) 