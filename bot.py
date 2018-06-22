import requests  
import datetime
import os
import telebot
from flask import Flask, request


url = "https://api.telegram.org/bot584253782:AAGNnxIbuHCCXkfL6UGHDBuikDfon093mBI/"


TOKEN = '584253782:AAGNnxIbuHCCXkfL6UGHDBuikDfon093mBI'
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)



@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Hello, ' + message.from_user.first_name)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    bot.reply_to(message, message.text)

def last_update(data):
    result = data['result']
    total_updates = len(result) - 1
    return result[total_updates]	
	
def send_mess(chat, text):
    params = {'chat_id': chat, 'text' : text}
    response = requests.post(url + 'sendMessage', data=params)
    return response
	
def get_chat_id(update):
    chat_id = update['message']['chat']['id']
    return chat_id

@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://rocky-sierra-97001.herokuapp.com/' + TOKEN)
    return "!", 200

chat_id = get_chat_id(last_update(get_updates_json(url)))
send_mess(chat_id, 'Suck it')
	
if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))