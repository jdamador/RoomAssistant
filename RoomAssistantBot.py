# Import all required libraries.
import telebot
import ast
import time
from telebot import types
from tools.recognizer import *
from telebot.util import async_dec

#* Set our Telegram token.
TOKEN = '987076381:AAEK8oT-VhNvnTKvx3pWTgNnte9EWC__Vf0'
bot = telebot.AsyncTeleBot(TOKEN)

# Set a list of possibles options to request.
stringList = {"1": "Lab 1", "2": "Lab 2", "3": "Lab 3",
              "4": "Móviles", "5": "Miniauditorio", "6": "Lab 210"}

#*  Create a Inline Keyboard.
def makeKeyboard():
    markup = types.InlineKeyboardMarkup()
    for key, value in stringList.items():
        markup.add(types.InlineKeyboardButton(text=value,
                                              callback_data="['value', '" + value + "', '" + key + "']"))
    return markup

#* Set a new handler to manage the default message to show it when the bot starts.
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(
        message, 'Bienvenido al sistema de consulta de estado de los laboratorio de Computación. Ingrese el comando /rooms para iniciar.')

#* Set a new handler to deal with all request to the bot.
@bot.message_handler(commands=['rooms'])
def handle_command_adminwindow(message):
    bot.send_message(chat_id=message.chat.id,
                     text='Laboratorios de la carrera de Computación',
                     reply_markup=makeKeyboard(),
                     parse_mode='HTML')
    
#* Function that response the petition about some room state.
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    print('Waiting')
    if (call.data.startswith("['value'")):
        option = ast.literal_eval(call.data)[1]
        if(option == 'Móviles'):
            status =  getStatus("http://compu:ICSCcomputec@172.24.15.126/mjpg/video.mjpg")
            bot.answer_callback_query(callback_query_id=call.id,
                                    show_alert=True,
                                    text= "Hay aproximadamente %s persona(s) en el %s" % (status, option) )
        
            if(status > 10):
                bot.answer_callback_query(callback_query_id=call.id,
                                    show_alert=True,
                                    text= "%s esta ocupado con aproximadamente %s personas" % (option, status) )
            elif(status > 2):
                 bot.answer_callback_query(callback_query_id=call.id,
                                    show_alert=True,
                                    text= "%s esta semi ocupado con aproximadamente %s personas" % (option, status) )
            elif(status < 2):
                bot.answer_callback_query(callback_query_id=call.id,
                                    show_alert=True,
                                    text= "%s esta semi libre con aproximadamente %s personas" % (option, status) )
        
        
        else: 
             bot.answer_callback_query(callback_query_id=call.id,
                                    show_alert=True,
                                    text= "Esta funcionabilidad estará disponible próximamente.")
while True:
    try:
        bot.polling()
    except:
        time.sleep(10)
