from model import ClassPredictor
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram_token import token, TG_API_URL, proxy
from dota2_wiki_parser import parser
import torch
from config import reply_texts
import numpy as np
from PIL import Image
from io import BytesIO
import time
import urllib
import requests

model = ClassPredictor()

def send_prediction_on_photo(update, context):
    start_time = time.process_time()
    chat_id = update.message.chat_id
    print("Got image from {}".format(chat_id))

    # получаем информацию о картинке
    image_info = update.message.photo[-1]
    image_file = image_info.get_file()
    image_stream = BytesIO()
    image_file.download(out=image_stream)
    print(image_stream)
    class_ = model.predict(image_stream)
    print('I predict - ', class_)
    result, img_url, audio_url = parser(class_)
    # теперь отправим результат

    text = 'Кажется это - '+ str(class_)+ '\n' \
            'а вот, что я о нем знаю: \n \n' + result

    text = "[​​​​​​​​​​​]({}) {}".format(img_url, text)

    sound = urllib.request.urlopen(audio_url)

    update.message.reply_text(text=text, parse_mode='Markdown')
    update.message.reply_audio(audio=sound)

    print("Sent Answer to user, predicted: {}".format(class_))
    end_time = time.process_time()
    print('Duration of prediction: {}'.format(end_time - start_time))

def do_start(update, context):

    text = "Привет, я бот-новичок в dota2. \n " \
           "Я только начал разбираться в этой игре, \n " \
           "но уже знаю некоторых героев, \n " \
           "пока что это герои на 'A' и 'B', \n" \
           "если ты пришлешь мне фото одного из них, \n " \
           "то я попрубую узнать, как его зовут и \n " \
           "расскажу все, что успел узнать о нем. \n " \
           "Попробуем?"

    update.message.reply_text(text)

def do_echo(update, context):
    start_time = time.process_time()

    text = update.message.text

    if 'http' in text:

        response = requests.get(requests.get([i for i in text.split(' ') if 'http' in i][0]))

        img = BytesIO(response.content)


        class_ = model.predict(img)

        result, img_url, audio_url = parser(class_)

        text = 'Кажется это - ' + str(class_) + '\n' \
               'а вот, что я о нем знаю: \n \n' + result

        text = "[​​​​​​​​​​​]({}) {}".format(img_url, text)

        sound = urllib.request.urlopen(audio_url)

        update.message.reply_text(text=text, parse_mode='Markdown')
        update.message.reply_audio(audio=sound)

        print("Sent Answer to user, predicted: {}".format(class_))

    else:

        update.message.reply_text("ты сказал: \n")

    end_time = time.process_time()
    print('Duration: {}'.format(end_time - start_time))

def main():

    updater = Updater(token=token,
                      base_url=TG_API_URL,
                      request_kwargs={'proxy_url': proxy},
                      use_context=True)

    dp = updater.dispatcher

    start_handler = CommandHandler("start", do_start)
    message_handler = MessageHandler(Filters.text, do_echo)
    photo_handler = MessageHandler(Filters.photo, send_prediction_on_photo)

    dp.add_handler(start_handler)
    dp.add_handler(message_handler)
    dp.add_handler(photo_handler)

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":

    main()