import MySQLdb
from pprint import pprint

class Database(object): 
    #Hardcoded for now
    host="127.0.0.1"
    user="root"
    password="root"
    

    def __init__(self, name):
        self.connection = MySQLdb.connect(self.host, self.user, self.password, name)
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()
