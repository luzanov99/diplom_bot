
from telegram import ReplyKeyboardMarkup

def main_keyboard():
    return ReplyKeyboardMarkup([
        ['Отметиться в журнале посещаемости'],
        ['Изменить анкету' ,'Взять задачу', 'Посмотреть текущую задачу'],
        ['Начать перерыв']
    ], resize_keyboard=True)

def first_meet_keyboard():
    return ReplyKeyboardMarkup([
        ['Заполнить анкету'],
    ],resize_keyboard=True)

def admin_keyboard():
    return ReplyKeyboardMarkup([
        ['Добавить задачу', 'Активные сотрудники'],
    ],resize_keyboard=True)


active_users=list()