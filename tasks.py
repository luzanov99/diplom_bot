from db import db, get_or_create_user
from utils import main_keyboard
from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup

def take_task(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    profession = user["anketa"]["profession"]
    task = db.tasks.find_one({"specialty": profession})
    reply_keyboard = [
        ["Взять задачу", "Вернуться назад"]
        ]
    if  not task:
        update.message.reply_text(f"К сожалению пока задач никаких нет", reply_markup=main_keyboard())
    else:
        task_name=task["task"]
        update.message.reply_text(f"Новая задача \nВот ее описание:{task_name}", reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return "choose" 
        

def choose_activity(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
