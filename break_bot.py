from db import db, get_or_create_user
from utils import main_keyboard
from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup
from datetime import datetime, timedelta
from telegram.ext import  ConversationHandler

def break_continue(context):
    context.bot.send_message(chat_id=context.job.context, text="Осталось 5 минут перерыва")
    

def break_start(update, context):
    try:
        reply_keyboard=[['Закончить выполнение']]
        user = get_or_create_user(db, update.effective_user, update.message.chat.id)
        context.job_queue.run_once(break_continue, 600, context=update.message.chat_id)
        update.message.reply_text(f"Перерыв начался в {datetime.now()}",reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True))
        db.users.update_one(
                            {'_id': user['_id']},
                            {'$set': {'break_start': datetime.now()}}
                        )
        db.users.update_one(
                            {'_id': user['_id']},
                            {'$inc': {'number_of_breaks': 1}}
                        )
        
        return "finish_break"
    except (IndexError, ValueError):
        update.message.reply_text("В")

def end_break(update, context):
    update.message.reply_text(f"Перерыв закончился в {datetime.now()}",reply_markup=main_keyboard())
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    time_start=user["break_start"]
    time_end=datetime.now()
    time=time_end-time_start
    db.users.update_one(
                            {'_id': user['_id']},
                            {'$unset': {'break_start': 1}}
                        )
    if time.seconds>900:
        update.message.reply_text("Ты слишком долго был на перерыве")
        db.users.update_one(
                            {'_id': user['_id']},
                            {'$inc': {'forfeit': 1}}
                        )
    else:
        update.message.reply_text("Пора снова поработать")
    
    return ConversationHandler.END



