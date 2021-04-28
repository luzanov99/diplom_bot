import logging
import settings
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from handlers import greet_user, send_picture
from anketa import anketa_start, anketa_name, anketa_dontknow, anketa_profession
from db import db, save_anketa ,get_or_create_user
from tasks import take_task, choose_activity
logging.basicConfig(filename='bot.log', level=logging.INFO)

    
def main():
    # Создаем бота и передаем ему ключ для авторизации на серверах Telegram
    mybot = Updater(settings.API_KEY, use_context=True)
    anketa = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex('^(Заполнить анкету)$'), anketa_start)
            ],
        states={
            "name": [MessageHandler(Filters.text, anketa_name)],
            "profession":[MessageHandler(Filters.regex('^(Агент|Кассир|Комендант|Машинист|Статистик)$'), anketa_profession)]
            },
        fallbacks=[MessageHandler(Filters.text | Filters.video | Filters.photo | Filters.document | Filters.location, anketa_dontknow)]
    )
    task=ConversationHandler(
    entry_points=[dp.add_handler(MessageHandler(Filters.regex('^(Взять задачу)$'), take_task))],
    states={
        "choose":[MessageHandler(Filters.text, choose_activity)],
    },
    fallbacks=[MessageHandler(Filters.text | Filters.video | Filters.photo | Filters.document | Filters.location, anketa_dontknow)] 
    )
    
    dp = mybot.dispatcher
    dp.add_handler(anketa)
    
    

    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("photo", send_picture))
    
    logging.info("Бот стартовал")
    mybot.start_polling()
    # Запускаем бота, он будет работать, пока мы его не остановим принудительно
    mybot.idle()


if __name__ == "__main__":
    main()