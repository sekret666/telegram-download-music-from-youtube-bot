#!/usr/bin/python3.8
import telebot
import os
from config import * #create config.py file next to this one. config.py example copy from 
import youtube_dl
bot = telebot.TeleBot(token)

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id,'Этот бот конвертирует видео с ютуба в MP3 320kbps\nОтправь мне ссылку на видео, чтобы скачать песню...')
    bot.send_message(owner,'@'+str(message.from_user.username)+' кинул старт')
@bot.message_handler(commands=["help"])
def help(message):
    bot.send_message(message.chat.id,'Этот бот конвертирует видео с ютуба в MP3 320kbps и высылает вам в виде аудио\n\nБота создал @bob_volskiy\nИсходный код: github.com/BobVolskiy/\n\nМои боты:\n@bvsticker_bot\n@bob_musica_bot')
    bot.send_message(owner,'@'+str(message.from_user.username)+' кинул хелп')

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
                name=ydl.extract_info(link)['title'].replace("/", "_")
            k = open(name+'.mp3','r+b')
            bot.send_document(message.chat.id,k)
            k.close()
            os.remove(name+'.mp3')
        except:
            bot.send_message(message.chat.id,'Произошла какая-то ошибка ❌')
    else: bot.send_message(message.chat.id,'Это не похоже на ссылку с ютуба ❌')

print('Бот начал свою работу...')
bot.polling()