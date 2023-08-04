from subprocess import call
from aiogram.types import CallbackQuery, Message,ReplyKeyboardMarkup,ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
import random
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from datetime import datetime
from aiogram.utils import executor

from aiogram.utils.markdown import text


def main_menu():
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='🕸️ Получение временной почты', callback_data='get_mail'),
            ],
            [
                InlineKeyboardButton(
                    text='🕷️ Избранное', callback_data='cfavorites'),
                 InlineKeyboardButton(
                    text='🎓 Создать пароль', callback_data='password'),
            ],
        ]
    )

    return markup

def deleted():
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='🕳️ Очистить', callback_data='del')
            ]
        ]
    )

    return markup

def admin_panel():
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='🐦‍⬛ Статистика', callback_data='stats'),
                InlineKeyboardButton(
                    text='🕸️ Почта', callback_data='rass'),
            ],
            [
                InlineKeyboardButton(
                    text='🎩 Перезагрузить', callback_data='reboot'),
            ],
        ]
    )

    return markup

def email_menu():
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='save', callback_data='favorite'),
                InlineKeyboardButton(
                    text='', callback_data=''),
            ],
        ]
    )

    return markup


def btnCheck():
	btnCheck = types.InlineKeyboardMarkup(
		inline_keyboard=[
			[
				InlineKeyboardButton(
					text='🕷️ Подписаться, url='https://t.me/+Dn6ZLbZA9wY5YWQy'),
				InlineKeyboardButton(
					text='🌑 Я подписался', callback_data='subchanneldone')
			],
		]
	)

	return btnCheck


def email():
    markup = types.InlineKeyboardMarkup(
    	inline_keyboard=[
    		[
    			InlineKeyboardButton(
    				text='🕷️ Добавить в избранное', callback_data="favorite"),
    			InlineKeyboardButton(
    				text='✖️ Спрятать', callback_data='del'),
    		],
    		]
    	)

    return markup


def loading():
	markup = types.InlineKeyboardMarkup(
		inline_keyboard=[
			[
				InlineKeyboardButton(
					text='🪮 Загрузка...', callback_data=''),
			],
			]
		)

	return markup