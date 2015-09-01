import dbconnect
from pprint import pprint
from random import randint
from dbconnect import Database
import MySQLdb


def chose_random_snp(moneykyDB):
    query = """SELECT count(*) from snp"""
    moneykyDB.cursor.execute(query)
    answer =  moneykyDB.cursor.fetchone()
    num_rows = answer[0]
    portfolio_of_today = []
    #pprint(num_rows)
    for i in range(1,10):
        portfolio_id=randint(0,num_rows)
        query = ("""SELECT Symbol FROM snp WHERE id=%d""" , portfolio_id)
        moneykyDB.cursor.execute("""SELECT Symbol FROM snp WHERE id=%s""" , portfolio_id)
        answer= portfolio_id, moneykyDB.cursor.fetchone()
        portfolio_of_today.append(answer)
    return portfolio_of_today
    #pprint(num_rows)



