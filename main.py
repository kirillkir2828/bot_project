import logging

import telegram
from telegram import ReplyKeyboardMarkup
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

reply_keyboard = [['/start', '/help']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)


async def start(update, context):
    user = update.effective_user
    await update.message.reply_text(
        rf"Привет {user.mention_html()}! Я бот-тренажер по физике",
        reply_markup=markup
    )


async def help(update, context):
    await update.message.reply_text("Я пока не умею помогать... Я только ваше эхо.")


async def close_keyboard(update, context):
    await update.message.reply_text(
        "Ok",
        reply_markup=ReplyKeyboardMarkup()
    )


def main():
    application = Application.builder().token("6195146605:AAE86fNa3FdK-pgTMwHKpyr1ZAXWZgWARzU").build()
    application.add_handler(CommandHandler("close", close_keyboard))
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))
    application.run_polling()
