from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

import configparser
import logging
import redis
import pymysql.cursors
import random
import os

global redis1

global flag
global cookname
global cookvideo
global cookdescribe
global movieposter
global movieid
global moviename
global movieposter
global connection
flag = 0


def main():
    # Load your token and create an Updater for your Bot

    config = configparser.ConfigParser()
    config.read('config.ini')
    updater = Updater(token=(os.environ['ACCESS_TOKEN']), use_context=True)
    dispatcher = updater.dispatcher

    global redis1
    redis1 = redis.Redis(host=(os.environ['HOSTREDIS']), password=(os.environ['PASSWORDREDIS']),
                         port=(os.environ['REDISPORT']))

    global connection
    connection = pymysql.connect(host=(os.environ['HOSTSQL']), port=int((os.environ['PORTSQL'])),
                                 user=(os.environ['USERSQL']), password=(os.environ['PASSWORDSQL']),
                                 database=(os.environ['DATABASESQL']))



    # You can set this logging module, so you will know when and why things do not work as expected
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    # register a dispatcher to handle message: here we register an echo dispatcher
    echo_handlerp = MessageHandler(Filters.photo, echophoto)
    echo_handlert = MessageHandler(Filters.text & (~Filters.command), echo)
    echo_handlerv = MessageHandler(Filters.video, echovideo)
    dispatcher.add_handler(echo_handlerp)
    dispatcher.add_handler(echo_handlert)
    dispatcher.add_handler(echo_handlerv)
    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("add", add))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("who", who))
    dispatcher.add_handler(CommandHandler("upload", upload))
    dispatcher.add_handler(CommandHandler("cname", uploadcname))
    dispatcher.add_handler(CommandHandler("cdescribe", uploaddescribe))
    dispatcher.add_handler(CommandHandler("cook", cookreply))
    dispatcher.add_handler(CommandHandler("find", findmovie))
    dispatcher.add_handler(CommandHandler("write", mwrite))
    dispatcher.add_handler(CommandHandler("read", mread))
    dispatcher.add_handler(CommandHandler("createm", addmovie))
    dispatcher.add_handler(CommandHandler("start", guid))
    dispatcher.add_handler(CommandHandler("guidance", guid))
    dispatcher.add_handler(CommandHandler("listc", listcook))
    dispatcher.add_handler(CommandHandler("listm", listmovie))

    # To start the bot:
    updater.start_polling()
    updater.idle()


def setdefualt():
    global cooknames
    global cookvideo
    global cookdescribe
    global movieposter
    global moviename
    cookvideo = ''
    cookdescribe = ''
    cooknames = ''
    moviename = ''
    movieposter = ''



def guid(update, context):
    update.message.reply_text('Welcome to team36 chatbot')
    update.message.reply_text('/find + movie name : to view or write the comment of movie ')
    update.message.reply_text('/listm  : to browse the list of movies (random select 4 each time)')
    update.message.reply_text('/createm + movie name : to add a new movie ')
    update.message.reply_text('/cook + food name : to find the cooking video')
    update.message.reply_text('/listc  : to browse the list of cooking videos (random select 4 each time)')
    update.message.reply_text('/upload : to start upload your cooking video ')
    update.message.reply_text('/guidance : to view guidance again ')


def listcook(update, context):
    reply=listcooksql()
    if len(reply) < 4:
        rsample = range(len(reply))
    else:
        rsample = (random.sample(range(1, len(reply)), 4))
    for i in rsample:
        update.message.reply_text('food name: \n' + reply[i][1])

def listcooksql():
    cursor = connection.cursor()
    try:
        sql = 'select * from cook;'
        cursor.execute(sql)
        result = cursor.fetchall()
        return (result)
    except:
        Exception: print("Fail")
    cursor.close()


def listmovie(update, context):
    reply=listmoviesql()
    print(len(reply))
    if len(reply) <=4:
        rsample = range(len(reply))
    else:
        rsample = (random.sample(range(1, len(reply)), 4))
    for i in rsample:
        update.message.reply_text('movie name: \n' + reply[i][1])

def listmoviesql():
    cursor = connection.cursor()
    try:
        sql = 'select * from movie;'
        cursor.execute(sql)
        result = cursor.fetchall()
        return (result)
    except:
        Exception: print("Fail")
    cursor.close()


def uploadcname(update, context):
    global flag
    if flag == 0:
        update.message.reply_text('you have not started upload cook function yet')
    elif flag == 1:
        cname = update.message.text[7:]
        global cookname
        cookname = cname
        update.message.reply_text('discribe your dish, using the function /cdescribe')


def uploaddescribe(update, context):
    global flag
    if flag == 0:
        update.message.reply_text('you have not started upload cook function yet')
    elif flag == 1:
        cd = update.message.text[11:]
        global cookdescribe
        cookdescribe = cd
        update.message.reply_text('now send your cooking video directly')


def upload(update: Update, context: CallbackContext):  # start teh function to upload cookvideo
    global flag
    flag = 1
    update.message.reply_text('Tell me the name of your dish, using the function /cname')


def echophoto(update, context: CallbackContext):
    file = update.message.photo[-1]
    logging.info(context.args)
    logging.info(context)
    global flag
    if flag == 2:
        global moviename
        minserreply=minsert(moviename, file.file_id)
        if minserreply==1:
            update.message.reply_text('upload successfully')
        else:
            update.message.reply_text('please provide a poster with better quality')
        flag = 0
    elif flag == 0:
        update.message.reply_photo(file)


def echovideo(update, context):
    file = update.message.video
    logging.info(file.get_file())
    logging.info(file.file_id)
    global flag
    global cookvideo
    if flag == 1:  # means the following video will be uploaded
        cookvideo = file.file_id
        flag = 0
        uploadcook()
        update.message.reply_text('upload successfully')
    elif flag == 0:
        context.bot.send_video(chat_id=update.effective_chat.id, video=file.file_id)


def uploadcook():
    global cookname
    global cookvideo
    global cookdescribe
    try:
        cursor = connection.cursor()
        sql = 'insert into cook values(0,%s,%s,%s);'
        cursor.execute(sql, [cookname, cookvideo, cookdescribe])
        cursor.fetchall()
        connection.commit()
        setdefualt()
    except:
        Exception: print("Fail")
    cursor.close()


def cookreply(update: Update, context: CallbackContext):  # reply the information of cook to user
    cname = update.message.text[6:]
    logging.info(cname)
    reply = getvideo(cname)
    logging.info(reply[2])
    update.message.reply_text('NAME: ' + reply[1])
    update.message.reply_text('DESCRIBE: ' + reply[3])
    update.message.reply_video(reply[2])


def getvideo(cname):  # get cook video from sql
    cursor = connection.cursor()
    try:
        sql = "select* from cook where cookname=%s"
        cursor.execute(sql, [cname])
        result = cursor.fetchall()
        data = result[0]
        return (data)

    except:
        Exception: print('fail')
    cursor.close()


def findmovie(update: Update, context: CallbackContext):
    global movieid
    mname = update.message.text[6:]
    result = movieinsql(mname)
    if result:
        movieid = result[0][0]
        update.message.reply_text(
            'If you want to write comment, please use function /write + your comment\nIf you want to read comment, please use function /read')

    else:
        update.message.reply_text(
            'No such movie in database, you can create a new one, by using function /createm + movie name')


def movieinsql(mname):
    cursor = connection.cursor()
    try:
        sql = "select * from movie where m_name=%s"
        cursor.execute(sql, [mname])
        result = cursor.fetchall()
        return (result)
    except:
        Exception: print('fail')
    cursor.close()


def mwrite(update, context):
    global movieid
    comment = update.message.text[7:]
    cinsert(movieid, comment)
    update.message.reply_text('comment finish')


def cinsert(id, comment):
    cursor = connection.cursor()
    try:
        sql = 'insert into comment values(0,%s,%s);'
        cursor.execute(sql, [comment, id])
        connection.commit()
    except:
        Exception: print("Fail")
    cursor.close()


def mread(update: Update, context: CallbackContext):
    global movieid
    logging.info(movieid)
    reply = getcomment(movieid)
    reply2 = getposter(movieid)
    if len(reply) < 4:
        rsample = range(len(reply))
    else:
        rsample = (random.sample(range(1, len(reply)), 4))
    update.message.reply_photo(reply2[0][2])
    for i in rsample:
        update.message.reply_text('Comment: \n' + reply[i][1])

    setdefualt()


def getposter(id):
    cursor = connection.cursor()
    try:
        sql = 'select * from movie where mid=%s;'
        cursor.execute(sql, id)
        result = cursor.fetchall()
        return (result)
    except:
        Exception: print("Fail")
    cursor.close()


def getcomment(id):
    cursor = connection.cursor()
    try:
        sql = 'select * from comment where mid=%s;'
        cursor.execute(sql, id)
        result = cursor.fetchall()
        return (result)
    except:
        Exception: print("Fail")
    cursor.close()


def addmovie(update: Update, context: CallbackContext):
    global flag
    global moviename
    moviename = context.args[0]
    if movieinsql(moviename):
        update.message.reply_text(
            'this movie already existed, please use /find +movie name to view or read the function')
    else:
        flag = 2
        update.message.reply_text('please provide a poster for this movie')
        update.message.reply_text(
            'If there is no successful upload notification, please attempt upload a better quality poster')


def minsert(name, poster):

    cursor = connection.cursor()
    try:
        sql = 'insert into movie values(0,%s,%s);'
        cursor.execute(sql, [name, poster])
        connection.commit()
        a=1
        return (a)
    except:
        a=0
        Exception: print("Fail")
        return (a)
    cursor.close()
    setdefualt()




def echo(update, context):
    reply_message = update.message.text.upper()
    logging.info("Update: " + str(update))
    logging.info("context: " + str(context))
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Helping you helping you.')


def add(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /add is issued."""
    try:
        global redis1
        logging.info(context.args)
        logging.info(context.args[0])
        msg = context.args[0]  # /add keyword <-- this should store the keyword
        redis1.incr(msg)
        update.message.reply_text('You have said ' + msg + ' for ' + redis1.get(msg).decode('UTF-8') + ' times.')
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /add <keyword>')


def who(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /hello is issued."""
    update.message.reply_text('I am project chatbot!')


if __name__ == '__main__':
    main()
