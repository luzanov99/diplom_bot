from glob import glob
from utils import main_keyboard, first_meet_keyboard, admin_keyboard
from random import randint, choice
from db import db, get_or_create_user
from telegram.ext import  ConversationHandler
from datetime import datetime
import os

def greet_user(update, context):
    user = db.users.find_one({"user_id": update.effective_user.id})
    if not user:
        update.message.reply_text('Добрый день! Для начала работы необходимо заполнить анкету', reply_markup=first_meet_keyboard())
    elif user["anketa"]["profession"]=="Админ":
        user_name=user["anketa"]["name"]
        update.message.reply_text(f'Добрый день, {user_name}!', reply_markup=admin_keyboard())
    else:
        user = get_or_create_user(db, update.effective_user, update.message.chat.id)
        user_name=user["anketa"]["name"]
        update.message.reply_text(f'Добрый день, {user_name}!', reply_markup=main_keyboard())
    return ConversationHandler.END

'''
def send_picture(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    cat_photos_list = glob('images/*.jp*g')
    cat_pic_filename = choice(cat_photos_list)
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, photo=open(cat_pic_filename, 'rb'))
    update.message.reply_text("Привет, пользователь! Ты вызвал команду /start", reply_markup=main_keyboard())
'''

def start_work(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    user_name=user["anketa"]["name"]
    now=datetime.today()
    date_now=str(now.date())
    time_now=str(now.time())
    user_come = db.visit_log.find_one({
        "user_name":user["anketa"]["name"],
        "date": date_now  
    })
    if not user_come:
       
        user_go = {
                "user_name": user["anketa"]["name"],
                "date": date_now,
                "time":time_now

            }
        db.visit_log.insert_one(user_go)
        update.message.reply_text(f"Здравствуйте, {user_name}! Время начала смены: {time_now}", reply_markup=main_keyboard())
    else:
        if not "endtime" in user_come:
           
            db.visit_log.update(
                        { '_id' : user_come['_id'] },
                        { '$set': { "endtime":time_now }})
            update.message.reply_text(f"Приятного отдыха!", reply_markup=main_keyboard())
        else:
        
            update.message.reply_text(f"Приятного отдыха!", reply_markup=main_keyboard())
            


def active_workers(update, context):
    user = db.users.find_one({"user_id": update.effective_user.id})
    now=datetime.today()
    date_now=str(now.date())
    if user["anketa"]["profession"]=="Админ":
        update.message.reply_text("Список активных сегодня пользователей",reply_markup=admin_keyboard())
        active_users=db.visit_log.find({"date": date_now})
        for active_user in active_users:
            update.message.reply_text(active_user["user_name"])
    else:
        update.message.reply_text("Эта команда предназначена для администратора")

    


def send_file(update, context):
    user = db.users.find_one({"user_id": update.effective_user.id})
    user_name=user["username"]
    update.message.reply_text("Обрабатываю фото")
    os.makedirs(f'downloads/users/{user_name}', exist_ok=True)
    photo_file = context.bot.getFile(update.message.photo[-1].file_id)
    filename = os.path.join(f'downloads/users/{user_name}', f'{photo_file.file_id}.jpg')
    photo_file.download(filename)
    update.message.reply_text("Файл сохранен")