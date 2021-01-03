#!/usr/bin/python3.8
import telebot
import os
from config import * #create config.py file next to this one. config.py example copy from 
import youtube_dl
bot = telebot.TeleBot(token)

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id,'✌ Этот бот конвертирует видео с ютуба в mp3\n Отправь мне ссылку на видео, чтобы скачать песню...')
@bot.message_handler(commands=["help"])
def help(message):
    bot.send_message(message.chat.id,'👨‍💻Бота создал @bob_volskiy\nИсходный код: github.com/BobVolskiy/')

@bot.message_handler(content_types=["text"])
def link(message):
    link=message.text
    if link.find('youtu')!=-1:
        try:
            ydl_opts = {
            'outtmpl': '%(title)s.%(ext)s',
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
                }],
            }

            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                name=ydl.extract_info(link)['title']
            k = open(name+'.mp3','r+b')
            bot.send_document(message.chat.id,k)
            k.close()
            os.remove(name+'.mp3')
        except:
            bot.send_message(message.chat.id,'❌ Произошла какая-то ошибка')
    else: bot.send_message(message.chat.id,'❌ Это не похоже на ссылку с ютуба')

print('Бот начал свою работу...')
bot.polling()