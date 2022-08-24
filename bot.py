import logging
import settings

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from handlers import greet_user,  start_work, active_workers, send_file
from anketa import anketa_start, anketa_name, anketa_dontknow, anketa_profession
from db import db, save_anketa ,get_or_create_user
from tasks import take_task, choose_activity, finish_activity, current_task, task_dontknow, choose_profession_for_task, add_task, adding_task, add_photo, set_user_for_task
from break_bot import break_start, end_break
logging.basicConfig(filename='bot.log', level=logging.INFO)



    
def main():
    # Создаем бота и передаем ему ключ для авторизации на серверах Telegram
    mybot = Updater(settings.API_KEY, use_context=True)
    anketa = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex('^(Заполнить анкету|Изменить анкету)$'), anketa_start)
            ],
        states={
            "name": [MessageHandler(Filters.text, anketa_name)],
            "profession":[MessageHandler(Filters.regex('^(Агент|Кассир|Комендант|Машинист|Статистик)$'), anketa_profession)]
            },
        fallbacks=[MessageHandler(Filters.text | Filters.video | Filters.photo | Filters.document | Filters.location, anketa_dontknow)]
    )
    task=ConversationHandler(
    entry_points=[
        MessageHandler(Filters.regex('^(Взять задачу)$'), take_task),
        MessageHandler(Filters.regex('^(Посмотреть текущую задачу)$'), current_task),
        ],
    states={
        "choose":[MessageHandler(Filters.regex('^(Начать задачу|Вернуться назад)$'), choose_activity)],
        "finish":[MessageHandler(Filters.regex('^(Закончить выполнение|Прикрепить файл-отчет)$'), finish_activity)],

        "photo": [MessageHandler(Filters.photo,add_photo)]

    },
    fallbacks=[MessageHandler(Filters.text | Filters.video | Filters.photo | Filters.document | Filters.location, task_dontknow)] 
    )
    break_user = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex('^(Начать перерыв)$'), break_start)
        ],
        states={"finish_break":[MessageHandler(Filters.regex('^(Закончить перерыв)$'), end_break)]
            },
        fallbacks=[MessageHandler(Filters.text | Filters.video | Filters.photo | Filters.document | Filters.location, task_dontknow)]
    )

    new_task=ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('^(Добавить задачу)$'), add_task)],
        states={
            "profession_for_task": [MessageHandler(Filters.text, choose_profession_for_task)],
            "formation_task": [MessageHandler(Filters.text, adding_task)],
            "user_for_task": [MessageHandler(Filters.text, set_user_for_task)]
        },
        fallbacks=[MessageHandler(Filters.text | Filters.video | Filters.document | Filters.location, task_dontknow)]
    )

    dp = mybot.dispatcher
    dp.add_handler(anketa)
    dp.add_handler(task)
    dp.add_handler(break_user)
    dp.add_handler(new_task)
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(MessageHandler(Filters.regex('^(Отметиться в журнале посещаемости)$'), start_work))
    dp.add_handler(MessageHandler(Filters.regex('^(Активные сотрудники)$'), active_workers))
    #dp.add_handler(CommandHandler("photo", send_picture))
    dp.add_handler(MessageHandler(Filters.photo, send_file))
    
    logging.info("Бот стартовал")
    mybot.start_polling()
  
    mybot.idle()


if __name__ == "__main__":
    main()
