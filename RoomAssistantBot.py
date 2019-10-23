#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is to control a object recognizer.

import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def start(update, context):
    keyboard = [[InlineKeyboardButton("Estado de Móviles", callback_data='1'),
                 InlineKeyboardButton("Estado de E-210", callback_data='2')],

                [InlineKeyboardButton("Estadp de MiniAuditorio", callback_data='3')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose:', reply_markup=reply_markup)


def button(update, context):
    query = update.callback_querylasedf
    if(query.data == '1'):
        status = 1232
        query.edit_message_text(text= "Hay aproximandamente: {}".format(status))
    elif(query.data == '2'):
        status = 11
        query.edit_message_text(text= "Hay aproximandamente: {}".format(status))
    elif(query.data == '3'):
        status = 1232
        query.edit_message_text(text= "Hay aproximandamente: {}".format(status))


def help(update, context):
    update.message.reply_text("Use /start to test this bot.")


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("987076381:AAEK8oT-VhNvnTKvx3pWTgNnte9EWC__Vf0", use_context=True)

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(CommandHandler('help', help))
    updater.dispatcher.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()