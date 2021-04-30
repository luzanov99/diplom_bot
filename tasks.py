from db import db, get_or_create_user
from utils import main_keyboard
from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup
from datetime import datetime
from telegram.ext import  ConversationHandler
def take_task(update, context):
    reply_keyboard = [
        ["Начать задачу", "Вернуться назад"]
    ]
    task_count=0
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    profession = user["anketa"]["profession"]

    tasks = db.tasks.find({"specialty": profession})
    
    
    if  not tasks:
        update.message.reply_text(f"К сожалению пока задач никаких нет", reply_markup=main_keyboard())
    else:
        if not "task" in user:
               
            for task in tasks:
                
                    if not 'executor' in task:
                        task_name=task["task"]
                        db.tasks.update_one(
                            {'_id': task['_id']},
                            {'$set': {'executor': user["anketa"]["name"]}}
                        )
                        db.users.update_one(
                            {'_id': user['_id']},
                            {'$set': {'task': task_name}}
                        )
                    
                        update.message.reply_text(f"Новая задача \nВот ее описание:{task_name}", reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True))
                        return "choose" 
                    else:
                        task_count+=1
            if task_count==tasks.count():
                update.message.reply_text(f"К сожалению пока задач никаких нет", reply_markup=main_keyboard())
                return ConversationHandler.END
        else:
            update.message.reply_text(f"У вас уже есть задача на выполнении")
            return ConversationHandler.END

            

    

def choose_activity(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    task= update.message.text

    if task=="Начать задачу":
      
        tasks = db.tasks.find({"executor": user["anketa"]["name"]})
        for task in tasks:
            if not "start_datetime" in task:
                db.tasks.update_one(
                            {'_id': task['_id']},
                            {'$set': {'start_datetime': datetime.now()}}
                        
                        )
                task_name=task['task']
                reply_keyboard=[['Закончить выполнение']]
                update.message.reply_text(f"Начало выполнения задачи {task_name} в : {datetime.now()}", reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True))
                return "finish"
        
    else:
        update.message.reply_text('Вы вренулись в главное меню', reply_markup=main_keyboard())
        return ConversationHandler.END
      

def finish_activity(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    tasks = db.tasks.find({"executor": user["anketa"]["name"]})
    for task in tasks:
        if not "end_datetime" in task:
            db.tasks.update_one(
                            {'_id': task['_id']},
                            {'$set': {'end_datetime': datetime.now()}}
                        
                        )
            db.users.update(
                      { '_id' : user['_id'] },
                      { '$unset': { "task":1 }})
            task_name=task["task"]
            update.message.reply_text(f" Задача   {task_name} выполнена : {datetime.now()}", reply_markup=main_keyboard())
            return ConversationHandler.END


def current_task(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    try:
        task_name=user["task"]
    except KeyError:
        update.message.reply_text(f"У вас нет активной задачи на данный момент", reply_markup=main_keyboard())
        return ConversationHandler.END

    reply_keyboard1 = [
        ["Начать задачу", "Вернуться назад"]
    ]
    reply_keyboard2=[['Закончить выполнение']]
   

    if not "task" in user:
        update.message.reply_text(f"У вас нет активной задачи на данный момент", reply_markup=main_keyboard())
        return ConversationHandler.END
    else:
        tasks = db.tasks.find({"executor": user["anketa"]["name"]})
        for task in tasks:
            if not "end_datetime"  in task:
                update.message.reply_text(f"У вас есть активная задача \nВот ее описание:{task_name}", reply_markup=ReplyKeyboardMarkup(reply_keyboard1, one_time_keyboard=True, resize_keyboard=True))
                return "choose"
    

def task_dontknow(update, context):
    update.message.reply_text("Не понимаю")


    






     
    


   
