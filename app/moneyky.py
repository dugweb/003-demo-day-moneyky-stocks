
from dbactions import MoneykyDB
from datetime import datetime
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

		

		return portfolio
		# get_ticker_performance('^GSPC') # snp performance

		# set_days_performance() 
		# set_portfolio(holdings)

	def random_portfolio(self, amount):
		return self.db.get_random_companies(int(amount))
		
	def get_portfolio_performance(self, holdings = []):
		''' creates a list of holdings with their associated performance (Data from http://dev.markitondemand.com) '''	    

		data = []
		
		for ticker in holdings:
			data.append(self.get_ticker_performance(ticker[1]))
		

		return data


	def get_ticker_performance(self, ticker):
		''' helper function to get a single stock's performance from Yahoo Finance'''
		### Construct API Call ###
		urlbase = "http://dev.markitondemand.com/Api/v2/InteractiveChart/json?parameters="
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
		
		response = requests.get(url)
		result = response.json()
		
		### For testing ###
		# response = open('../sample-historical-data.json', 'r')
		# result = json.load(response)

		prices = result['Elements'][0]['DataSeries']['close']['values']
		ytdindex = self.find_index_of_ytd(result['Dates'])

		return {	
			'ticker'			: ticker,
			'today'				: result['Dates'][-1],
			'currentprice'		: prices[-1],
			'1year'				: result['Dates'][0],
			'1yearprice'		: prices[0],
			'1yearperformance'	: self.percent_growth(prices[0], prices[-1]),
			'ytd'				: result['Dates'][ytdindex],
			'ytdprice'			: prices[ytdindex],
			'ytdperformance'	: self.percent_growth(prices[ytdindex], prices[-1])
		}


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


	def find_index_of_ytd(self, dates = []):
		'''The first day of trading isn't always January 1st, so this finds the index first day of trading'''
		index = 0
		count = 0
		while not index:
			try:
				index = dates.index(str(datetime.now().year) + '-01-0%sT00:00:00' %count)
			except ValueError:
				count += 1
				continue

		return index

	def percent_growth(self, originalprice = 0, currentprice = 0):
		dif = currentprice - originalprice
		return dif / originalprice


# judist = Moneyky()
# r = judist.get_portfolio_performance(['AAPL'])
# print r


