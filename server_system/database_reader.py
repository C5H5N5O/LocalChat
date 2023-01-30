import sqlite3

class DB:
    
    def __init__(self, database_path):
        
        self.database_path = database_path


    def create_database(self, cur):
        cur.execute("CREATE TABLE users(id, name)")
        cur.execute("CREATE TABLE chats(name, users, massages)")


    def connect(self):
        connection = sqlite3.connect(self.database_path)
        cur = connection.cursor()
        if cur.fetchall() == []:
            self.create_database(cur)


    def read(self):
        pass


    def post(self, data):
        pass


    #проверяет логин и пороль, при совпадении в базе данных возвращает id пользователя
    def check_user_password(self, login, password):
        pass