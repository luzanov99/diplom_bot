from glob import glob
from utils import main_keyboard, first_meet_keyboard
from random import randint, choice
from db import db, get_or_create_user
from telegram.ext import  ConversationHandler
def greet_user(update, context):
    user = db.users.find_one({"user_id": update.effective_user.id})
    if not user:
        update.message.reply_text('Привет, новый пользователь давай лучше узнаем друг друга!', reply_markup=first_meet_keyboard())    
    else:
        user = get_or_create_user(db, update.effective_user, update.message.chat.id)
        update.message.reply_text('Привет, пользователь! Ты вызвал команду /start', reply_markup=main_keyboard())
    return ConversationHandler.END



def send_picture(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    cat_photos_list = glob('images/*.jp*g')
    cat_pic_filename = choice(cat_photos_list)
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, photo=open(cat_pic_filename, 'rb'))
    update.message.reply_text("Привет, пользователь! Ты вызвал команду /start", reply_markup=main_keyboard())

