import sqlite3


class User_Database:
    def __init__(self,db_path):
        self.path = db_path
        self.create_table()
        
    def create_table(self):
        try:
            db = sqlite3.Connection(self.path)
            cursor = db.cursor()
            db_list = []
            q1 = """ CREATE TABLE user_shows (
                UserName text NOT NULL,
                ShowID text PRIMARY KEY 
            )
            """
            cursor.execute(q1)
            db.commit()
        except Exception as e:
            print(str(e))

    def check_table(self):
        db = sqlite3.Connection(self.path)
        cursor = db.cursor()
        tl = cursor.execute(
                """SELECT tableName FROM sqlite_master WHERE type='table'
                AND tableName='user_shows'; """).fetchall()
        if len(tl)==0:
            self.create_table()

    def add_show(self,un,id):
        try:
            db = sqlite3.Connection(self.path)
            cursor = db.cursor()
            q = "INSERT INTO user_shows VALUES (?,?)"
            cursor.execute(q,(un,id))
            db.commit()
            return True
        except Exception as e:
            print(str(e))
            return False

    def get_rec_shows(self,un):
        try:
            db = sqlite3.Connection(self.path)
            cursor = db.cursor()
            q = "SELECT ShowID FROM user_shows WHERE UserName=(?)"
            t1 = cursor.execute(q,(un,)).fetchall()
            tmp = []
            for i in t1:
                tmp.append(i[0])
            db.commit()
            return tmp
        except Exception as e:
            print(str(e))
            return []

    def reset_recommendations(self,un):
        try:
            db = sqlite3.Connection(self.path)
            cursor = db.cursor()
            q = "DELETE FROM user_shows WHERE UserName=(?)"
            cursor.execute(q,(un,))
            db.commit()
            return True
        except Exception as e:
            print(str(e))
            return False