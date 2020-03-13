import cx_Oracle
import os
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

class DB(object):
    def __init__(self):
        self.conn = cx_Oracle.connect('R5_T2240','R5_T2240','192.168.0.5:1521/r5')
        self.cur = self.conn.cursor()
    
    def __del__(self):
        self.cur.close()
        self.conn.close()
        print("关闭游标，关闭连接")
            
    def query(self,sql):
        self.cur.execute(sql)
        return  self.cur.fetchall()

    def exec(self,sql):
        try:
            self.cur.execute(sql)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print(str(e))