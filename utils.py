
from telegram import ReplyKeyboardMarkup

def main_keyboard():
    return ReplyKeyboardMarkup([
        ['Изменить анкету' ,'Взять задачу']
    ])

def first_meet_keyboard():
    return ReplyKeyboardMarkup([
        ['Заполнить анкету'],
    ])
