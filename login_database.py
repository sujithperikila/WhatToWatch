import sqlite3


class Login_DataBase:
    def __init__(self,db_path):
        self.path = db_path
        self.create_table()
        

    def create_table(self):
        try:
            db = sqlite3.Connection(self.path)
            cursor = db.cursor()
            db_list = []
            q1 = """ CREATE TABLE login_details (
                UserName text PRIMARY KEY,
                Password text NOT NULL 
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
                AND tableName='login_details'; """).fetchall()
        if len(tl)==0:
            self.create_table()

    def verify_login(self,un,pw):
        db = sqlite3.Connection(self.path)
        cursor = db.cursor()
        q="SELECT * From login_details WHERE UserName=? AND Password=?"
        l = cursor.execute(q,(un,pw)).fetchall()
        if len(l)==1:
            print("User : "+str(un)+" Login  Authenticated")
            return True
        else:
            return False

    def register(self,un,pw):
        try:
            db = sqlite3.Connection(self.path)
            cursor = db.cursor()
            q = "INSERT INTO login_details VALUES (?,?)"
            cursor.execute(q,(un,pw))
            db.commit()
            return True
        except Exception as e:
            print(str(e))
            return
    





