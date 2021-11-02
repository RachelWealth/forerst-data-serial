# 线程将数写入数据库
import sqlite3


# noinspection PyAttributeOutsideInit
class WriteIntoSQL:
    def __init__(self, table_name):
        self.table_name = table_name
        self.GPS_table_name = 'GPS' + table_name

    # click START the first time everyday and create the table
    def create_table(self):
        self.open_SQL()
        sql = 'CREATE TABLE IF NOT EXISTS ' + self.table_name + '(time TEXT, node TEXT, temperature TEXT, ' \
                                                                'humidity TEXT, concentrateMQ2 TEXT, concentrateMQ4 TEXT, light TEXT, state TEXT)'
        sql_1 = 'CREATE TABLE IF NOT EXISTS ' + self.GPS_table_name + '(node TEXT, latitude TEXT, longitude TEXT)'

        self.cursor_1.execute(sql)
        self.cursor_2.execute(sql_1)

        self.conn_1.commit()
        self.conn_2.commit()
        self.close_SQL()

    # to facilitate the
    def open_SQL(self):
        self.conn_1 = sqlite3.connect('android.db')  # 节点数据数据库
        self.conn_2 = sqlite3.connect('GPS.db')  # 节点GPS数据库

        self.cursor_1 = self.conn_1.cursor()
        self.cursor_2 = self.conn_2.cursor()

    def close_SQL(self):
        self.conn_1.close()
        self.conn_2.close()

    def writeInto_datatable(self, time, state, data=None):
        if data is None:
            data = []
        sql = 'INSERT INTO ' + self.table_name + ' VALUES(?,?,?,?,?,?,?,?)'
        if not state:
            state0 = 'd'
        else:
            state0 = 's'
        self.cursor_1.execute(sql, (time, data[0], data[1], data[2], data[3], data[4], data[5], state0))
        self.conn_1.commit()

    def writeInto_GPStable(self, data=None):
        if data is None:
            data = []
        sql = 'INSERT INTO ' + self.GPS_table_name + ' VALUES(?,?,?)'
        self.cursor_2.execute(sql, (data[0], data[1], data[2]))
        self.conn_2.commit()
