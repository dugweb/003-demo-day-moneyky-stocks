import MySQLdb
from pprint import pprint

''' reference: http://stackoverflow.com/questions/5687718/how-can-i-insert-data-into-a-mysql-database '''

class Database: 
    #Hardcoded for now
    host="127.0.0.1"
    user="root"
    password="root"
    

    def __init__(self, name):
        self.connection = MySQLdb.connect(self.host, self.user, self.password, name)
        self.cursor = self.connection.cursor()

    def insert_commit(self, query):
        try:
            self.cursor.execute(query)
            self.connection.commit()
            pprint("query success")
        except:
            pprint("query failed")
            self.connection.rollback()
    
    def query(self, query):
        cursor = self.connection.cursor( MySQLdb.cursors.DictCursor )
        cursor.execute(query)

        return cursor.fetchall()

    def __del__(self):
        self.connection.close()
