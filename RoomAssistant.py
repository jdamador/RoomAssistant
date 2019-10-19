from telegram.ext import Updater, CommandHandler
import re 

def get_status():
    return "Hay aproximadamente 10 personas"

# This function in in charge of manage how will send the response message.
def handler(bot, update):
    # * Get room status.
    status = get_status()
    chat_id = update.message.chat_id
    bot.send_message(chat_id=chat_id, )
    

