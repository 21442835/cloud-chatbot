from calendar import c
from pydoc import describe
from this import d
from pymysql import connect


class GUEST_OP(object):
    """user类"""
    def __init__(self):
        """连接数据库"""
        self.conn = connect(host='124.71.41.226' ,port=3306 ,user='root' ,password='Hkbucloud!' ,database='chatbot')
        self.cursor = self.conn.cursor()

    def __del__(self):
        """关闭数据库"""
        self.cursor.close()
        self.conn.close()

    def execute_sql(self,sql):
        """执行Sql语句"""
        self.cursor.execute(sql)
        for temp in self.cursor.fetchall():
            print(temp)


    def function_info(self):
        """功能界面"""
        while True:
            print("--------功能界面--------")
            print("1:查询所有电影信息")
            print("2:查询所有评论信息")
            print("3:编写评论")
            print("4:查询菜谱信息")
            print("5:编写菜谱信息")
            num = input("请输入你想要的功能序号：")
            if num == "1":
                self.moiveselect()
            elif num == "2":
                self.commentselect()
            elif num == "3":
                self.commentadd()
            elif num == "4":
                self.cookselect()
            elif num == "5":
                self.cookadd()    
            elif num == "7":
                break
        
    def moiveselect(self):
        """查询电影信息"""
        mname=input('请输入你要买查询的电影')
        sql = 'select m_name from movie where m_name=%s;'
        self.cursor.execute(sql,[mname])
        print(self.cursor.fetchall())

    def cookselect(self):
        """查询商品信息"""
        cname=input('请输入你要买查询的菜谱：')
        sql = 'select * from cook where cookname=%s;'
        self.cursor.execute(sql,[cname])
        print(self.cursor.fetchall())

    def cookadd(self):
        """增加菜谱"""
        cname = input('请输入你要增加点菜谱的名称：')
        cvideo = input('请输入video：')
        cdescribe = input('请输入你的描述：')
        sql = 'insert into cook values(0,%s,%s,%s);'
        self.cursor.execute(sql,[cname,cvideo,cdescribe])
        self.conn.commit()
        print('------>已成功增加菜谱<--------')
        
    def commentselect(self):
        """评论查询"""
        cmname=input('请输入你要买查询的评论：')
        sql = 'select text from comment where mid IN (select mid from movie where m_name=%s);'
        self.cursor.execute(sql,[cmname])
        cmtext=self.cursor.fetchall()
        for i in cmtext:
            print(i)

    def commentadd(self):
        """增加评论"""
        cmname = input('请输入电影名：')
        sql_m = 'select mid from movie where m_name = %s'
        mid = int(self.cursor.execute(sql_m,[cmname]))
        if mid :
            cmtext = input('请输入评论：')
            sql_cm = 'insert into comment values(0,%s,%s);'
            self.cursor.execute(sql_cm,[cmtext,mid])
            self.conn.commit()
            print('------>已成功增加评论<--------')
        else :
            print('------>没有这部电影<--------')

    def order_details(self,goods_id,goods_quantity):
        """向订单详情表中添加数据"""
        sql2 = 'select id from ORDER_INFO order by id desc;' #降序查询获取最新订单的id
        sql3 = 'insert into ORDER_DETAIL values(0,%s,%s,%s);'
        self.cursor.execute(sql2)
        order_id = self.cursor.fetchone()
        self.cursor.execute(sql3,[order_id,goods_id,goods_quantity])
        self.conn.commit()


def main():
    customer = GUEST_OP()
    customer.function_info()


if __name__ == '__main__':
    main()
