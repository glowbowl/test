import json 
import requests
import datetime
import os
import telebot
from flask import Flask, request

TOKEN = "584253782:AAGNnxIbuHCCXkfL6UGHDBuikDfon093mBI"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates():
    url = URL + "getUpdates"
    js = get_json_from_url(url)
    return js


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def send_message(text, chat_id):
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)
    
#@server.route('/' + TOKEN, methods=['POST'])
#def getMessage():
#    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
 #   return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://rocky-sierra-97001.herokuapp.com/' + TOKEN)
    return "!", 200

text, chat = get_last_chat_id_and_text(get_updates())
send_message(text, chat)

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))