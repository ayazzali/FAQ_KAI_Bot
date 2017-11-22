# -*- coding: utf-8 -*-
from telegram.ext import Updater  # пакет называется python-telegram-bot, но Python-
from telegram.ext import CommandHandler  # модуль почему-то просто telegram ¯\_(ツ)_/¯
from telegram.ext import MessageHandler, Filters
from telegram.ext import RegexHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, bot,ParseMode
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram.update import Update, Message
import sqlite3
import hashlib
from cleaner import Porter
from operator import attrgetter
from Db import Db
from config import Config as cfg
# import threading

needed_column = 2   

col_indx = (needed_column * 2) - 1

T_Question_Answer="T_Question_Answer"
QUESTION="Versions_of_a_formulation" # used Question
T_TELEGRAM_MESSAGES='T_Telegram_Messages'
DB_NAME='db_001.db'


def start(bot, update):# нам сёда пришел поисковый запрос от Юзера
    # подробнее об объекте update: https://core.telegram.org/bots/api#update
    print(update.message.chat.username)
    if str(update.message.text).startswith("/start"):
        update.message.reply_text("Привет! \r\nТы можешь написать вопрос про *Каи*. :) \r\nА я скину тебе лучшие. \r\nБаза была набрана в основном из 'Подслушано Каи' и офтильтрована нами. \r\nС наилучшими пожеланиями, команда 'Бот Номер Один'. ")
        return
    results = search(update.message.text, T_Question_Answer, QUESTION)# TODO: поменять бд
    sort = sorted(results, key=lambda k: k['matchedCount'])[:-4:-1]
    fma=For_more_answers()
    fma.message_id_from_usersText=(update.message.message_id)
    # выдаёт только ВопросОтвет
    for item in sort:
        keyboard = [[InlineKeyboardButton("Показать ответ:", callback_data=item['question'][0])]]
        reply = InlineKeyboardMarkup(keyboard)
        t = item['question'][1]
        t=update.message.reply_text(str(t), reply_markup=reply)
        fma.messages.append(str(item['question'][0])+','+str(t.message_id))
    gg=fma.Compress_for_recieve()
    keyboard = [[InlineKeyboardButton("Показать еще!", callback_data= gg)]]# TODO: ссылка на мессадж
    reply = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("____У нас есть еще:)_____", reply_markup=reply)
    t=Db().Execute(DB_NAME,"INSERT INTO "+T_TELEGRAM_MESSAGES+"(message_id, Text, User) VALUES("
        +str(update.message.message_id)+", '"+update.message.text+"', '"+ str(update.message.chat).replace("'",'"') +"' )")        # bot.sendMessage(chat_id=update.message.chat_id, text=str(t), reply_markup=reply)

def giveAnswer (bot, update):
    print('[giveAnswer]:')
    query = update.callback_query
    print('[giveAnswer]' +query.message.text)
    # query = update.callback_query
    message_id_Of_user_text=query.data.split(';')[0]
    if query.data.find(';')!=-1:
        fma= For_more_answers().Decompress(query.data)
        t=Db().ExecuteSingle(DB_NAME,"SELECT Text FROM "+T_TELEGRAM_MESSAGES+" WHERE message_id="+fma.message_id_from_usersText)
        
        results = search(t[0], T_Question_Answer, QUESTION)# TODO: поменять бд
        results = sorted(results, key=lambda k: k['matchedCount'])
        fma_answer_ids=[f.split(',')[0] for f in fma.messages]
        fma_messages_ids=[f.split(',')[1] for f in fma.messages if f.split(',')[1] != '']# used not now
        sort=[]
        for x in results :
            alredy_exists=False
            for fmm_id in fma_answer_ids:
                if int(fmm_id)== x['question'][0]:
                    alredy_exists=True
                    break
            if not alredy_exists:
                sort.append(x)
            
        sort=sort[:-4:-1] 
        
        for i, item in enumerate(sort):
            keyboard = [[InlineKeyboardButton("Показать ответ:", callback_data=item['question'][0])]]
            reply = InlineKeyboardMarkup(keyboard)
            t = item['question'][1]
            try:
                bot.edit_message_text(text=str(t),
                                chat_id=query.message.chat_id,
                                message_id=int(fma_messages_ids[i]),#TODO think
                                reply_markup=reply
                                )
            except BaseException : 
                print('BaseException')
            fma.messages.append(str(item['question'][0])+',')
        
        gg=fma.Compress_for_recieve()
        if gg==query.data:
            if len(sort) == 0:
                print("больше нечего выдавать")
                pass
            keyboard = [[InlineKeyboardButton("Больше нет :(", callback_data= gg)]]
        else:
            keyboard = [[InlineKeyboardButton("Показать еще!", callback_data= gg)]]# TODO: ссылка на мессадж
        reply = InlineKeyboardMarkup(keyboard)
        try:
            bot.edit_message_text(text="____У нас есть еще:)_____",
                                chat_id=query.message.chat_id,
                                message_id=query.message.message_id,
                                reply_markup=reply
                                )
        except BaseException:
            print( "Дошли до предела callback_data")
            bot.edit_message_text(text="____ЭТО КОНЕЦ :(_____",
                                chat_id=query.message.chat_id,
                                message_id=query.message.message_id
                                )
    else:
        #print(update.message.chat.username+' [giveAnswer]'+'\r\n'+query.message.text+'\r\n')
        t='<b>'+query.message.text+'</b> \r\n'+Db().GetByColumnName('db_001.db', 'T_Question_Answer', 'id',query.data)[0][2]
        bot.edit_message_text(text=t,
                            chat_id=query.message.chat_id,
                            message_id=query.message.message_id, 
                            parse_mode=ParseMode.HTML)

def search(text, table, column):
    resByAllWordsArr = []  # [[][][]]
    justMmm = []
    for word in word_cleaner(text):  # TODO: or 2 or 3 spaces
        temp = Db().search_by_word_with_like(DB_NAME, table, column, word)
        resByAllWordsArr.append(temp)  # append добавляет мссив в первую ячейку
        justMmm += temp
    r = []

    for resByWordArr in list(set(justMmm)): #list(set(resAllWords)) - все вопросы которые сматчились в поиске предыдущем, ни не повторяются
        for resArr in resByAllWordsArr:  # []
            for machedQuestion in resArr:
                if (machedQuestion == resByWordArr):
                    temp_hash = hashlib.md5(str(machedQuestion[0]).encode("utf-8")).digest()
                    firstStepForThisItem = True
                    for q in r:
                        # Done q1, q2, q3=q# todo: how q['hash']
                        if q['hash'] == temp_hash:  # or q1==temp_hash or q2==temp_hash:
                            firstStepForThisItem = False
                            q['matchedCount'] += 1
                    # t=any ( tt )
                    if (firstStepForThisItem):  # count ==0
                        r.append({'hash': temp_hash, 'question': machedQuestion, 'matchedCount': 1})
                        # else:

    return r

def word_cleaner(lst):
    except_words = ['', 'и', 'да', 'также', 'тоже', 'а', 'но', 'зато', 'однако', 'однако же', 'все же', 'или', 'что',
               'чтобы', 'как', 'когда',
               'лишь', 'едва', 'чтобы', 'дабы', 'если', 'если бы', 'коли', 'хотя', 'хоть', 'пускай', 'как',
               'как будто', 'эт', 'бы']

    lst = lst.replace(',', '').replace('!', '').replace('?', '').replace('-', '').replace('.', '')
    lst = lst.split(' ')

    counter = 0
    for souz in except_words:
            lst = [Porter.stem(x) for x in lst if souz != x]

    return lst
    # todo count maches


class For_more_answers:
    """1024;1023,23;1021,12;1022,4"""

    def __init__(self):
        self.messages=[]
    
    message_id_from_usersText=''
    """ ['5,1063', '23,1064', '19,1065'] """
    messages=[]

    def Compress_for_recieve(self):
        """message_id_from_usersText,arr_str_message_ids_with_id_in_Db"""
        return str(self.message_id_from_usersText)+';'+';'.join(self.messages)

    def Decompress(self,str_from_callbackQueryData):
        self.message_id_from_usersText=str_from_callbackQueryData.split(';')[0]
        self.messages=str_from_callbackQueryData.split(';')[1:]#todo:..
        return self
# @kai7_bot 
updater = Updater(token=cfg().getToken())  # тут токен, который выдал вам Ботский Отец!

# start_handler = CommandHandler('', start)  # этот обработчик реагирует
# только на команду /start
start_handler = RegexHandler('.+', start)

updater.dispatcher.add_handler(start_handler)  # регистрируем в госреестре обработчиков
updater.dispatcher.add_handler(CallbackQueryHandler(giveAnswer))
updater.start_polling()  # поехали!

#updater.idle()
input("started")

