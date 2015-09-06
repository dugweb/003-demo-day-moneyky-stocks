
from dbconnect import Database
from readjson import readjson
from pprint import pprint
from dbactions import *
from yahoo_finance import Share

class Moneyky(object):


    def __init__(self):

        # Connect to the databasee
        self.moneykyDB = Database('moneyky')
        # if snp_companies table is empty then 
        self.seeddb()
        self.portfolio_of_day()

    def seeddb(self):
        ''' runs once if there are no companies in the snp_companies file '''
        snp500_companies = readjson('../spx-companies.json')
        #pprint (snp500_companies)

        query = "SELECT * FROM snp_table"
        self.moneykyDB.cursor.execute(query)
        result = self.moneykyDB.cursor.fetchone()
        if result:
            # there is a table named "tablename"
        	pprint("snp table exists")
        else:        	
            # Loop through the list and insert Symbol to the snp table
            pprint("Filling up the snp table")
            for i in range(0,len(snp500_companies)):
                row = [snp500_companies[i]['Symbol'], snp500_companies[i]['Name']]
                pprint ((i,snp500_companies[i]['Name']))
                self.moneykyDB.cursor.execute("""INSERT INTO snp_table(Symbol, Name) VALUES(%s, %s)""", row)
            self.moneykyDB.connection.commit()
            pprint("SNP Table loaded to moneykyDB") 

    def portfolio_of_day(self):
        '''This function is the one that will run once per day - Important Function'''
        self.random_portfolio(10)
        # get_ticker_performance('^GSPC') # snp performance

        # set_days_performance() 
        # set_portfolio(holdings) 
        pass
        



    def random_portfolio(self, num_holdings = 10):
        ''' creates a list of holdings with their associated performance '''
        query = """SELECT count(*) from snp_table"""
    	self.moneykyDB.cursor.execute(query)
    	answer =  self.moneykyDB.cursor.fetchone()
    	num_rows = answer[0]
    	portfolio_ids= []
    	holdings= []
    	pprint(num_rows)
        for i in range(0,num_holdings):
        	portfolio_id = randint(0,num_rows)  # Generate rand b/w 0 - 500
        	self.moneykyDB.cursor.execute("""SELECT Symbol, Name FROM snp_table WHERE id=%s""" , portfolio_id)
        	d = self.moneykyDB.cursor.fetchone()
        	ticker = d[0]
        	perf = self.get_ticker_performance(ticker)
        	holdings.append((portfolio_id, ticker, perf))
        holdings.sort()
        pprint(holdings)
        return holdings

    def get_ticker_performance(self, ticker):
        ''' helper function to get a single stock's performance from Yahoo Finance'''
        today = datetime.date.today()
    	stock = Share(ticker)
    	prev_close= stock.get_prev_close()
    	close_price= stock.get_price()
    	diff = float(close_price) - float(prev_close)
    	perf_percent = diff * 100 / float(prev_close)
	    #pprint(perf_percent)
    	return perf_percent

    def get_days_performance(self, date = None):
        ''' return days performance'''
        moneyky_perf = sum(moneyky_stock[2] for moneyky_stock in portfolio_of_today) / float(len(portfolio_of_today))


    def set_days_performance(self):
        ''' calculate average of holdings to insert into moneyky vs snp'''
        # insert holding into DB

        pass

    def set_portfolio_holdings(self, holdings = []):
        # moneyky_perf = sum(moneyky_stock[2] for moneyky_stock in portfolio_of_today) / float(len(portfolio_of_today))
        # pprint("^^^^^^^^^^")
        # pprint(snp_perf) 
        # pprint(moneyky_perf) 
        # pprint("^^^^^^^^^^")
        # for stock in portfolio_of_today: # snp_id:stock[0] , symbol: stock[1][0] , name: stock[1][1] , perf: stock[2]
        #    moneykyDB.cursor.execute("""INSERT INTO holdings_table (snp_id , Performance) VALUES(%s, %s)""", (stock[0] , stock[2]))
        #    moneykyDB.connection.commit()
        pass


    def save(self):
        ''' Save everything to the database after we're happy with it '''
        # DBActions
        # Insert portfolio
        # Insert Holdings
        pass
