import logging
import time
from telegram import ReplyKeyboardMarkup
from telegram import ForceReply, Update
from telegram import ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import requests

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

URL = 't.me/physics_training_bot'
TOKEN = '6915498321:AAEG09W9StyUxgOqV7-wNw73RocE7I46msQ'


async def start(update, context):
    reply_keyboard = [['/start', '/help'],
                      ['/data', '/time']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    await update.message.reply_text(
        "Привет! 👋 \nЯ бот-тренажер по физике, давай вместе порешаем задачи?",
        reply_markup=markup
    )


async def close_keyboard(update, context):
    await update.message.reply_text(
        "Ok",
        reply_markup=ReplyKeyboardRemove()
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Как я могу помочь?")


async def topic(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Для того, чтобы выбрать раздел напиши его номер:\n1.Кинематика \n2.Динамика\n3.Статика")
    """
    if a == '1':
        await update.message.reply_text(
            f'Для того, чтобы выбрать подраздел напиши его номер:\nAзбука кинематики\nПрямолинейное равномерное движение')
    """


async def time_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(time.asctime().split()[3])


async def data_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(' '.join(time.asctime().split()[1:3]))


async def echo(update, context):
    #global a
    # У объекта класса Updater есть поле message,
    # являющееся объектом сообщения.
    # У message есть поле text, содержащее текст полученного сообщения,
    # а также метод reply_text(str),
    # отсылающий ответ пользователю, от которого получено сообщение.
    a = update.message.reply_text(f'{update.message.text}')
    await a
    #await update.message.reply_text(f'{update.message.text}')


def main() -> None:
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("6915498321:AAEG09W9StyUxgOqV7-wNw73RocE7I46msQ").build()
    application.add_handler(CommandHandler("close", close_keyboard))
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("topic", topic))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("time", time_command))
    application.add_handler(CommandHandler("data", data_command))

    # Run the bot until the user presses Ctrl-C
    text_handler = MessageHandler(filters.TEXT, echo)
    application.add_handler(text_handler)
    application.run_polling()
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
