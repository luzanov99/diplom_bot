import logging
import settings
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from glob import glob
from random import randint, choice
from telegram import ReplyKeyboardMarkup
logging.basicConfig(filename='bot.log', level=logging.INFO)

def greet_user(update, context):
    print(update)
    update.message.reply_text('Привет, пользователь! Ты вызвал команду /start', reply_markup=main_keyboard)

def main_keyboard():
    return ReplyKeyboardMarkup([
        ['Кнопка', 'Кнопка1'],
        ['Кнопка2'],
        ['Кнопка3']
    ])

def send_picture(update, context):
    cat_photos_list = glob('images/*.jp*g')
    cat_pic_filename = choice(cat_photos_list)
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, photo=open(cat_pic_filename, 'rb'))
def main():
    # Создаем бота и передаем ему ключ для авторизации на серверах Telegram
    mybot = Updater(settings.API_KEY, use_context=True)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("photo", send_picture))
    dp.add_handler(MessageHandler(Filters.regex('^(Кнопка)$'), send_picture))
    dp.add_handler(MessageHandler(Filters.regex('^(Кнопка1)$'), send_picture))
    dp.add_handler(MessageHandler(Filters.regex('^(Кнопка2)$'), send_picture))
    dp.add_handler(MessageHandler(Filters.regex('^(Кнопка3)$'), greet_user))
    logging.info("Бот стартовал")
    mybot.start_polling()
    # Запускаем бота, он будет работать, пока мы его не остановим принудительно
    mybot.idle()


if __name__ == "__main__":
    main()