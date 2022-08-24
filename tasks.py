from db import db, get_or_create_user
from utils import main_keyboard, admin_keyboard, active_users
from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup
from datetime import datetime
from telegram.ext import  ConversationHandler
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from datetime import datetime
import os
def take_task(update, context):
    reply_keyboard = [
        ["Начать задачу", "Вернуться назад"]
    ]
    task_count=0
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    profession = user["anketa"]["profession"]
    now=datetime.today()
    date_now=str(now.date())
    time_now=str(now.time())
    tasks = db.tasks.find({"specialty": profession})
    
    #user_name=user["anketa"]["name"]
    user_find=db.visit_log.find_one({
        "user_name":user["anketa"]["name"],
        "date": { '$exists' : True } ,
        "time": { '$exists' : True }
    })
    if not user_find:
        update.message.reply_text(f"Для получения задачи необходимо отметиться в журнале посещаемости", reply_markup=main_keyboard())
        return ConversationHandler.END
    elif "endtime" in user_find:
        update.message.reply_text(f"Рабочий день закончен", reply_markup=main_keyboard())
        return ConversationHandler.END
    else:
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
                reply_keyboard=[['Закончить выполнение','Прикрепить файл-отчет']]
                update.message.reply_text(f"Начало выполнения задачи {task_name} в : {datetime.now()}", reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True))
                return "finish"
        
    else:
        update.message.reply_text('Вы вренулись в главное меню', reply_markup=main_keyboard())
        return ConversationHandler.END
      


def add_photo(update, context):
    reply_keyboard=[['Закончить выполнение','Прикрепить файл-отчет']]
    update.message.reply_text("Загружаю файл")
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    user_name=user["username"]
    os.makedirs(f'downloads/users/{user_name}', exist_ok=True)
    photo_file = context.bot.getFile(update.message.photo[-1].file_id)
    filename = os.path.join(f'downloads/users/{user_name}', f'{photo_file.file_id}.jpg')
    photo_file.download(filename)
    update.message.reply_text("Файл сохранен", reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True))
    return "finish"

    
def finish_activity(update, context):
    text=update.message.text
    if text=="Прикрепить файл-отчет":
        update.message.reply_text("Прикрепите фото-отчет",reply_markup=ReplyKeyboardRemove())
        return "photo"
    else:
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


def add_task(update, context):
    user=get_or_create_user(db, update.effective_user, update.message.chat.id)
    if user["anketa"]["profession"]=="Админ":
        update.message.reply_text("Введите название задачи", reply_markup=ReplyKeyboardRemove())
        
        return "profession_for_task"
    else:
        update.message.reply_text("Эта команда предназначена для администратора")
        return ConversationHandler.END

def choose_profession_for_task(update, context):
    text= update.message.text
    reply_keyboard = [
        ["Агент", "Кассир" ],
        ["Комендант"],
        ["Машинист", "Статистик","Выбрать сотрудника"]
        ]
    task={
        "task":text,
        "status": "directed"
    }
    db.tasks.insert_one(task)
    update.message.reply_text(f"Выберите проффесию для задачи", reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True))
    return "formation_task"

def adding_task(update, context):
    text= update.message.text
    active_users.clear()
    if text=="Выбрать сотрудника":
        
        users=db.users.find()
        count=0
        update.message.reply_text("Список активных сотрудников")
        for user in users:
            if not "task" in user:
                count+=1
                user_name=user["anketa"]["name"]
                update.message.reply_text(f"{count} {user_name}")
                t={count:user_name}
                active_users.append(t)
        update.message.reply_text("Введите номер сотрудника из спика выше")
        return "user_for_task"
        
    else:
        task=db.tasks.find_one({"status": "directed"})
        db.tasks.update_one(
                                {'_id': task['_id']},
                                {'$set': {'specialty': text}})
        db.tasks.update_one(
                                {'_id': task['_id']},
                                {'$unset': {'status': 1}}
                            )
        update.message.reply_text("Задача добавлена в список",reply_markup=admin_keyboard())
        return ConversationHandler.END


def set_user_for_task(update, context):
    text= update.message.text
    try:
        number=abs(int(text))
    except (TypeError, IndexError, ValueError):
        update.message.reply_text("Введите номер сотрудника коректоно")
        return "user_for_task"
    for items in active_users:
        if items.get(number) !=None:
            user_name=items.get(number)
    
    user = db.users.find_one({"anketa.name": user_name})
    task=db.tasks.find_one({"status": "directed"})
    task_name=task["task"]
    db.tasks.update_one(
                        {'_id': task['_id']},
                        {'$unset': {'status': 1}}
                    )
    db.tasks.update_one(
                        {'_id': task['_id']},
                        {'$set': {'executor': user_name}}
                    )                
    db.users.update_one(
                        {'_id': user['_id']},
                        {'$set': {'task': task_name}})
    update.message.reply_text("Задача добавлена в список",reply_markup=admin_keyboard())
    return ConversationHandler.END

    






     
    


   
