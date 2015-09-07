
from dbactions import MoneykyDB
import datetime
import requests
import urllib
import json

class Moneyky(object):


	def __init__(self):

		self.db = MoneykyDB()
		# Connect to the databasee
		# if snp_companies table is empty then 
		# seeddb()
		pass




	def seeddb(self):
		''' runs once if there are no companies in the snp_companies file '''
		
		self.db.seed_companies("../spx-companies.json")


	def portfolio_of_day(self):
		'''This function is the one that will run once per day - Important Function'''
		portfolio = self.db.get_random_companies(50)

		tickerlist = [stock[1] for stock in portfolio]
		performance = self.get_portfolio_performance(tickerlist)

		

		return portfolio, performance
		# get_ticker_performance('^GSPC') # snp performance

		# set_days_performance() 
		# set_portfolio(holdings)

	def random_portfolio(self, amount):
		return self.db.get_random_companies(int(amount))
		
	def get_portfolio_performance(self, holdings = []):
		''' creates a list of holdings with their associated performance (Data from http://dev.markitondemand.com) '''	    
		urlbase = "http://dev.markitondemand.com/Api/v2/InteractiveChart/json?parameters="
		

		

		for ticker in holdings:
			parameters = {
				   "Normalized":False,
				   "NumberOfDays":365,
				   "DataPeriod":"Day",
				   "Elements":[  
					  {  
						 "Symbol":ticker,
						 "Type":"price",
						 "Params":[  
							"c"
						 ]
					  }
				   ]
				}
			url = urlbase	
			url += urllib.quote_plus(json.dumps(parameters))
			


			# response = requests.get(urlbase, params=parameters)
			data = open('../sample-historical-data.json', 'r')
			response = json.load(data)
			return response
			


		# holdings = generate 50 random stocks and select them from spx_companies table
		# (loop) get_ticker_performance()
		 


		# query = """SELECT count(*) from snp_table"""
		# moneykyDB.cursor.execute(query)
		# answer =  moneykyDB.cursor.fetchone()
		# num_rows = answer[0]
		# portfolio_of_today = []
		# num_stocks_to_sample = 10
		# for i in range(0,num_stocks_to_sample):
		#     portfolio_id=randint(0,num_rows)  # Generate rand b/w 0 - 500
		#     moneykyDB.cursor.execute("""SELECT Symbol, Name FROM snp_table WHERE snp_id=%s""" , portfolio_id)
		#     d = moneykyDB.cursor.fetchone()
		#     answer= portfolio_id, d[0] , get_performance(d[0])
		#     pprint(answer)
		#     portfolio_of_today.append(answer)
		# portfolio_of_today.sort()
		# return portfolio_of_today
		pass


	def get_ticker_performance(self, ticker):
		''' helper function to get a single stock's performance from Yahoo Finance'''
		pass

	def get_days_performance(self, date = None):
		''' return days performance'''
		pass

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


judist = Moneyky()
r = judist.get_portfolio_performance(['AAPL'])
print r