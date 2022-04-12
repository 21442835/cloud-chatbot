import configparser
import logging
import redis
import pymysql.cursors
import random

"""connection = pymysql.connect(host='124.71.41.226', port=3306, user='root', password='Hkbucloud!', database='chatbot',
                             charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)"""

#connection=pymysql.connect(host='124.71.41.226', port=3306, user='root', password='Hkbucloud!', database='chatbot')


global redis1

global flag
global cookname
@@ -20,9 +21,9 @@
global moviename
global movieposter
global connection
flag = 0


flag=0
def main():
    # Load your token and create an Updater for your Bot

@@ -31,30 +32,35 @@ def main():
    updater = Updater(token=(config['TELEGRAM']['ACCESS_TOKEN']), use_context=True)
    dispatcher = updater.dispatcher

    global connection
    global redis1
    redis1 = redis.Redis(host=(config['REDIS']['HOST']), password=(config['REDIS']['PASSWORD']),
                         port=(config['REDIS']['REDISPORT']))

    global connection
    connection = pymysql.connect(host=(config['mysql']['HOST']), port=int((config['mysql']['PORT'])),
                                 user=(config['mysql']['USER']), password=(config['mysql']['PASSWORD']),
                                 database=(config['mysql']['DATABASE']))



    # You can set this logging module, so you will know when and why things do not work as expected
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    # register a dispatcher to handle message: here we register an echo dispatcher
    echo_handlerp = MessageHandler(Filters.photo, echophoto)
    #echo_handlerl = MessageHandler(Filters.photo & Filters.text, upload)
    # echo_handlerl = MessageHandler(Filters.photo & Filters.text, upload)
    echo_handlert = MessageHandler(Filters.text & (~Filters.command), echo)
    echo_handlerv = MessageHandler(Filters.video, echovideo)
    #echo_handler = MessageHandler(Filters.photo & (~Filters.command), echo)
    # echo_handler = MessageHandler(Filters.photo & (~Filters.command), echo)
    dispatcher.add_handler(echo_handlerp)
    dispatcher.add_handler(echo_handlert)
    dispatcher.add_handler(echo_handlerv)
    #dispatcher.add_handler(echo_handlerl)
    # dispatcher.add_handler(echo_handlerl)
    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("add", add))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("who",who))
    dispatcher.add_handler(CommandHandler("who", who))
    dispatcher.add_handler(CommandHandler("upload", upload))
    dispatcher.add_handler(CommandHandler("cname", uploadcname))
    dispatcher.add_handler(CommandHandler("cdescribe", uploaddescribe))
@@ -64,84 +70,84 @@ def main():
    dispatcher.add_handler(CommandHandler("read", mread))
    dispatcher.add_handler(CommandHandler("createm", addmovie))


    # To start the bot:
    updater.start_polling()
    updater.idle()


def setdefualt():
    global cooknames
    global cookvideo
    global cookdescribe
    global movieposter
    global moviename
    cookvideo=''
    cookdescribe=''
    cooknames=''
    moviename=''
    movieposter=''
    cookvideo = ''
    cookdescribe = ''
    cooknames = ''
    moviename = ''
    movieposter = ''


def uploadcname(update, context):
    global flag
    if flag==0:
    if flag == 0:
        update.message.reply_text('you have not started upload cook function yet')
    elif flag==1:
    elif flag == 1:
        cname = update.message.text[7:]
        global cookname
        cookname=cname
        cookname = cname
        update.message.reply_text('discribe your dish, using the function /cdescribe')


def uploaddescribe(update, context):
    global flag
    if flag==0:
    if flag == 0:
        update.message.reply_text('you have not started upload cook function yet')
    elif flag==1:
    elif flag == 1:
        cd = update.message.text[11:]
        global cookdescribe
        cookdescribe=cd
        cookdescribe = cd
        update.message.reply_text('now send your cooking video directly')


def upload (update:Update, context: CallbackContext):#start teh function to upload cookvideo
def upload(update: Update, context: CallbackContext):  # start teh function to upload cookvideo
    global flag
    flag=1
    flag = 1
    update.message.reply_text('Tell me the name of your dish, using the function /cname')


def echophoto(update,context: CallbackContext):
def echophoto(update, context: CallbackContext):
    file = update.message.photo[-1]
    #photo.download()
    #logging.info(update)
    # photo.download()
    # logging.info(update)
    logging.info(context.args)
    logging.info(context)
    #logging.info(file.get_file())#file path
    # logging.info(file.get_file())#file path
    global flag
    print('flaginephotois',flag)
    if flag==2:
        global  moviename
    print('flaginephotois', flag)
    if flag == 2:
        global moviename
        print(file.file_id)
        minsert(moviename,file.file_id)
        flag=0
    elif flag==0:
        minsert(moviename, file.file_id)
        flag = 0
    elif flag == 0:
        update.message.reply_photo(file)


def echovideo(update,context):
def echovideo(update, context):
    file = update.message.video
    #photo.download()
    # photo.download()
    logging.info(file.get_file())
    logging.info(file.file_id)
    global flag
    global cookvideo
    if flag==1:#means the following video will be uploaded
        cookvideo=file.file_id
        #update.message.reply_video('BAACAgUAAxkBAAIBGmI-40QiXhxOHr5_8wXtGVTue-pQAAJpBAACOvn4VeaN3SkeMoWjIwQ')
        flag=0
    if flag == 1:  # means the following video will be uploaded
        cookvideo = file.file_id
        # update.message.reply_video('BAACAgUAAxkBAAIBGmI-40QiXhxOHr5_8wXtGVTue-pQAAJpBAACOvn4VeaN3SkeMoWjIwQ')
        flag = 0
        uploadcook()
        update.message.reply_text('upload successfully')
    elif flag==0:
    elif flag == 0:
        context.bot.send_video(chat_id=update.effective_chat.id, video=file.file_id)


@@ -156,48 +162,51 @@ def uploadcook():
        cursor.fetchall()
        connection.commit()
        setdefualt()
        #cookreply()
        # cookreply()
    except:
        Exception: print("Fail")
    cursor.close()


def cookreply(update:Update, context: CallbackContext): #reply the information of cook to user
def cookreply(update: Update, context: CallbackContext):  # reply the information of cook to user
    cname = update.message.text[6:]
    logging.info(cname)
    reply=getvideo(cname)
    logging.info(reply['video'])
    update.message.reply_text('NAME: '+reply['cookname'])
    update.message.reply_text('DESCRIBE: '+ reply['describe'])
    update.message.reply_video(reply['video'])
    reply = getvideo(cname)
    logging.info(reply[2])
    update.message.reply_text('NAME: ' + reply[1])
    update.message.reply_text('DESCRIBE: ' + reply[3])
    update.message.reply_video(reply[2])


def getvideo(cname):#get cook video from sql
    cursor=connection.cursor()
def getvideo(cname):  # get cook video from sql
    cursor = connection.cursor()
    try:
        sql="select* from cook where cookname=%s"
        cursor.execute(sql,[cname])
        result=cursor.fetchall()
        data=result[0]
        return(data)
        sql = "select* from cook where cookname=%s"
        cursor.execute(sql, [cname])
        result = cursor.fetchall()
        data = result[0]
        return (data)

    except:
        Exception:print('fail')
        Exception: print('fail')
    cursor.close()


def findmovie(update:Update, context: CallbackContext):
def findmovie(update: Update, context: CallbackContext):
    global movieid
    mname = update.message.text[6:]
    result=movieinsql(mname)
    #print('mid:', movieid)
    result = movieinsql(mname)
    print('result is ',result)
    if result:
        movieid = result[0]['mid']
        #update.message.reply_text('If you want to read comment, please use function /read')
        update.message.reply_text('If you want to write comment, please use function /write + your comment\nIf you want to read comment, please use function /read')
        movieid = result[0][0]
        # update.message.reply_text('If you want to read comment, please use function /read')
        update.message.reply_text(
            'If you want to write comment, please use function /write + your comment\nIf you want to read comment, please use function /read')

    else:
        update.message.reply_text('No such movie in database, you can create a new one, by using function /createm + movie name')
        update.message.reply_text(
            'No such movie in database, you can create a new one, by using function /createm + movie name')


def movieinsql(mname):
    cursor = connection.cursor()
@@ -212,14 +221,15 @@ def movieinsql(mname):


def mwrite(update, context):
    global  movieid
    comment=update.message.text[7:]
    #comment=context.args[0:-1]
    global movieid
    comment = update.message.text[7:]
    # comment=context.args[0:-1]
    print(comment)
    cinsert(movieid,comment)
    cinsert(movieid, comment)
    update.message.reply_text('comment finish')

def cinsert(id,comment):

def cinsert(id, comment):
    print(id)
    print(comment)
    cursor = connection.cursor()
@@ -231,29 +241,31 @@ def cinsert(id,comment):
        Exception: print("Fail")
    cursor.close()

def mread(update:Update, context: CallbackContext):

def mread(update: Update, context: CallbackContext):
    global movieid
    logging.info(movieid)
    reply=getcomment(movieid)
    reply2=getposter(movieid)
    if len(reply)<4:
        rsample=range(len(reply))
    reply = getcomment(movieid)
    reply2 = getposter(movieid)
    if len(reply) < 4:
        rsample = range(len(reply))
    else:
        rsample = (random.sample(range(1, len(reply)), 4))
    update.message.reply_photo(reply2[0]['m_image'])
    update.message.reply_photo(reply2[0][2])
    for i in rsample:
        #update.message.reply_text('NAME: '+mname)
        update.message.reply_text('Comment: \n'+ reply[i]['text'])
        # update.message.reply_text('NAME: '+mname)
        update.message.reply_text('Comment: \n' + reply[i][1])

    setdefualt()


def getposter(id):
    cursor = connection.cursor()
    try:
        sql = 'select * from movie where mid=%s;'
        cursor.execute(sql,id)
        cursor.execute(sql, id)
        result = cursor.fetchall()
        return(result)
        return (result)
    except:
        Exception: print("Fail")
    cursor.close()
@@ -263,26 +275,24 @@ def getcomment(id):
    cursor = connection.cursor()
    try:
        sql = 'select * from comment where mid=%s;'
        cursor.execute(sql,id)
        cursor.execute(sql, id)
        result = cursor.fetchall()
        return(result)
        return (result)
    except:
        Exception: print("Fail")
    cursor.close()



def addmovie(update:Update, context: CallbackContext):
def addmovie(update: Update, context: CallbackContext):
    global flag
    global moviename
    moviename = context.args[0]
    flag=2
    print('flaginaddmovie',flag)
    flag = 2
    print('flaginaddmovie', flag)
    update.message.reply_text('please provide a poster for this movie')



def minsert(name,poster):
def minsert(name, poster):
    cursor = connection.cursor()
    try:
        sql = 'insert into movie values(0,%s,%s);'
@@ -294,20 +304,6 @@ def minsert(name,poster):
    setdefualt()
















def echo(update, context):
    reply_message = update.message.text.upper()
    logging.info("Update: " + str(update))
@@ -335,11 +331,10 @@ def add(update: Update, context: CallbackContext) -> None:
        update.message.reply_text('Usage: /add <keyword>')


def who(update: Update,context: CallbackContext) -> None:
def who(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /hello is issued."""
    update.message.reply_text('I am project chatbot!')



if __name__ == '__main__':
    main()
    main()