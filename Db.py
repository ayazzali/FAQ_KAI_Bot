import sqlite3

class Db:
    """работа с базой данной происходяит только отсюда"""

    def search_by_word_with_like(self, database, table_name, column_where, word):
        self.db = sqlite3.connect(database)
        with self.db:
            cur = self.db.cursor()
            cur.execute("SELECT * "
                    "FROM " + table_name + " "
                                      "WHERE " + column_where + " LIKE '%" + word + "%'")
            t=cur.fetchall()
            #self.db.close()
            return t
            
    
    def GetByColumnName(self,database, table_name, column_where, value):
        self.db = sqlite3.connect(database)
        with self.db:
            cur = self.db.cursor()
            cur.execute("SELECT * "
                    "FROM " + table_name + " "
                                        "WHERE " + column_where + " = '" + value + "'")
            t=cur.fetchall()
            #self.db.close()
            return t

    def Execute (self,database,query):
        self.db = sqlite3.connect(database)
        with self.db:
            cur = self.db.cursor()
            cur.execute(query)
            
            t=cur.fetchall()
            self.db.commit()
            return t

    def ExecuteSingle (self,database,query):
        return self.Execute(database,query)[0]

    def Close(self):
        self.db.close()


conn1=sqlite3.connect("db_001.db")
cur1= conn1.cursor()
tName='T_Telegram_Messages'
cur1.execute("CREATE TABLE IF NOT EXISTS "+tName+" (message_id INTEGER PRIMARY KEY , Text TEXT, Created DATETIME);")# maybu user_id?
