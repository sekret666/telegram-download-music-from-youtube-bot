#!/usr/bin/python3.8
import telebot
import os
from config import *
import youtube_dl
import re
from PIL import Image

bot = telebot.TeleBot('1624907624:AAHe4LwnAC7sLbiyWQJq-5l6uq4BchytHe4')
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id,'Этот бот скачивает песню с ютуба в качестве 320kbps\nОтправь мне ссылку на видео, чтобы скачать песню...')
    bot.send_message(owner,'@'+str(message.from_user.username)+' кинул старт')
@bot.message_handler(commands=["help"])
def help(message):
    bot.send_message(message.chat.id,'Этот бот скачивает песню с ютуба в качестве 320kbps и высылает вам в виде аудио\n\nБота создал @bob_volskiy\nИсходный код: github.com/BobVolskiy/\n\nМои боты:\n@BVSticker_bot\n@BVMusic_bot')
    bot.send_message(owner,'@'+str(message.from_user.username)+' кинул хелп')
@bot.message_handler(content_types=["text"])
def link(message):
    bot.delete_message(message.chat.id, message.message_id)
    link=message.text
    if link.find('youtu')!=-1:
        try:
            ydl_opts = {
                'outtmpl': '%(title)s.%(ext)s',
                'format': 'bestaudio/best',
                'noplaylist': True,
                'writethumbnail': True,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '320',
                }],
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info=ydl.extract_info(link)
            title=info['title']
            name=title.replace("/", "_").replace('"', "'")
            punct = '[—–-]+'
            lst = re.split(punct, title)
            if len(lst)!=1:
                performer = lst[0]
                song_title = lst[1]
            else: 
                performer = info['uploader']
                song_title = title
            k = open(name+'.mp3','r+b')
            try: im=Image.open(name+'.jpg')
            except: im=Image.open(name+'.webp')
            bot.send_photo(message.chat.id,im, caption='youtu.be/'+info['id'])
            bot.send_audio(message.chat.id,k,performer=performer, title=song_title)
            k.close()
            try: os.remove(name+'.jpg')
            except: os.remove(name+'.webp')
            os.remove(name+'.mp3')
        except:
            bot.send_message(message.chat.id,'Произошла какая-то ошибка')
    else: bot.send_message(message.chat.id,'Это не похоже на ссылку с ютуба')
print('Бот начал свою работу...')
bot.polling()
