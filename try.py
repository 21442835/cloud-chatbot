import configparser
import logging
import pymysql.cursors
import random
global connection

def main():
    global connection
    connection = pymysql.connect(host=(config['mysql']['HOST']), port=int((config['mysql']['PORT'])),
                             user=(config['mysql']['USER']), password=(config['mysql']['PASSWORD']),
                             database=(config['mysql']['DATABASE']))
    getvideo()

def getvideo():#get cook video from sql
    cursor=connection.cursor()
    try:
        sql="select* from cook"
        cursor.execute(sql)
        result=cursor.fetchall()
        print(result)

    except:
        Exception:print('fail')
    cursor.close()

if __name__ == '__main__':
    main()