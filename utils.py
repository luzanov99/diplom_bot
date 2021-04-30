
from telegram import ReplyKeyboardMarkup

def main_keyboard():
    return ReplyKeyboardMarkup([
        ['Изменить анкету' ,'Взять задачу', 'Посмотреть текущую задачу']
    ], resize_keyboard=True)

def first_meet_keyboard():
    return ReplyKeyboardMarkup([
        ['Заполнить анкету'],
    ],resize_keyboard=True)

