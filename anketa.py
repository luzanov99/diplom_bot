from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup
from telegram.ext import  ConversationHandler
from db import db, save_anketa ,get_or_create_user
from utils import main_keyboard
def anketa_start(update, context):
    update.message.reply_text(
        "Как вас зовут? Напишите имя и фамилию",
        reply_markup=ReplyKeyboardRemove()
    )
    return "name"
    
def anketa_name(update, context):
    user_name = update.message.text
    if len(user_name.split()) < 2:
        update.message.reply_text("Пожалуйста, напишите имя и фамилию")
        return "name"
    else:
        context.user_data["anketa"] = {"name": user_name}
        user = get_or_create_user(db, update.effective_user, update.message.chat.id)
        save_anketa(db, user['user_id'], context.user_data['anketa'])
        reply_keyboard = [
        ["Агент", "Кассир" ],
        ["Комендант"],
        ["Машинист", "Статистик"]
        ]
        update.message.reply_text(f"Приятно познакомится {user_name} \n Выберите вашу должность в комании ", reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return "profession"
       # return ConversationHandler.END

def anketa_profession(update, context):
    user_profession = update.message.text
    print("123")
    context.user_data["anketa"]["profession"] = user_profession
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    save_anketa(db, user['user_id'], context.user_data['anketa'])
    update.message.reply_text("Отлично давай приступим к работе ", reply_markup=main_keyboard())
    return ConversationHandler.END

def anketa_dontknow(update, context):
    update.message.reply_text("Не понимаю")