import sqlite3
from globalFile import GlobalData

global_data = GlobalData()


class DbDriver(object):
    def __init__(self):
        self.db = sqlite3.connect(global_data.db_file_path)
        self.cursor = self.db.cursor()
        self.create_table()

    def create_table(self):
        sql = "create table if not exists users(id INTEGER primary key AUTOINCREMENT,identify varchar(255),password varchar(100))"
        self.cursor.execute(sql)
        self.db.commit()

    def store_user(self, identity, password):
        sql = "insert into users(identify,password) values(?,?)"
        self.cursor.execute(sql, (identity, password))
        self.db.commit()

    def find_all_user(self):
        sql = "select identify from users"
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        print(res)


db = DbDriver()
db.find_all_user()
