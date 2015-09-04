import dbconnect
import MySQLdb
from pprint import pprint
from random import randint
from dbconnect import Database
from yahoo_finance import Share
import datetime





def chose_random_snp(moneykyDB):
    query = """SELECT count(*) from snp_table"""
    moneykyDB.cursor.execute(query)
    answer =  moneykyDB.cursor.fetchone()
    num_rows = answer[0]
    portfolio_of_today = []
    num_stocks_to_sample = 10
    for i in range(0,num_stocks_to_sample):
        portfolio_id=randint(0,num_rows)  # Generate rand b/w 0 - 500
        moneykyDB.cursor.execute("""SELECT Symbol, Name FROM snp_table WHERE snp_id=%s""" , portfolio_id)
        d = moneykyDB.cursor.fetchone()
        answer= portfolio_id, d[0] , get_performance(d[0])
        pprint(answer)
        portfolio_of_today.append(answer)
    portfolio_of_today.sort()
    return portfolio_of_today

def get_performance(ticker):
    today = datetime.date.today()
    stock = Share(ticker)
    prev_close= stock.get_prev_close()
    close_price= stock.get_price()
    change = stock.get_change()
    diff = float(close_price) - float(prev_close)
    perf_percent = diff * 100 / float(prev_close)
    #pprint(perf_percent)
    #pprint(change)
    return perf_percent




     
        # #Create the holdings table
        # query = "SHOW TABLES LIKE 'holdings_table'"
        # moneykyDB.cursor.execute(query)
        # result = moneykyDB.cursor.fetchone()
        # if result:
        #     # there is a table named "tableName"
        #     pprint("holdings table exists")
        # else:
        #     query = """CREATE TABLE IF NOT EXISTS holdings_table  (portfolio_id INT NOT NULL AUTO_INCREMENT,PRIMARY KEY(portfolio_id), 
        #                                             Performance DECIMAL(4,2) DEFAULT NULL,
        #                                             snp_id INT NOT NULL,
        #                                             FOREIGN KEY fk_cat(snp_id) REFERENCES snp_table(snp_id)
        #                                             ON UPDATE CASCADE 
        #                                             ON DELETE RESTRICT);"""
        #     moneykyDB.insert_commit(query)
        
    
        # portfolio_of_today = chose_random_snp(moneykyDB)
        
        # pprint(portfolio_of_today)
        # snp_perf = get_performance('^GSPC') 