import dbconnect
from pprint import pprint
from random import randint
from dbconnect import Database
import MySQLdb


def chose_random_snp(moneykyDB):
    query = """SELECT count(*) from snp_table"""
    moneykyDB.cursor.execute(query)
    answer =  moneykyDB.cursor.fetchone()
    num_rows = answer[0]
    portfolio_of_today = []
    #pprint(num_rows)
    for i in range(1,10):
        portfolio_id=randint(0,num_rows)
        moneykyDB.cursor.execute("""SELECT Symbol, Name FROM snp_table WHERE snp_id=%s""" , portfolio_id)
        answer= portfolio_id, moneykyDB.cursor.fetchone() , get_performance(portfolio_id)
        portfolio_of_today.append(answer)
    return portfolio_of_today
    #pprint(num_rows)

def get_performance(snp_id):
    
    return randint(0.0,1000.0)/100.0

