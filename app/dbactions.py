import MySQLdb
from dbconnect import Database as DB
import json

class MoneykyDB(object):

	def __init__(self):
		self.db = DB('moneyky')
		self.cursor = self.db.cursor

		self.tables = {
			'companies'	: "spx_companies",
			'portfolios': "moneykyvsnp",
			'holdings'	: "portfolio_holding"
		}

		pass

	def get_random_companies(self, amount = 50):
		''' Return n companies from companies table'''		
		query = """SELECT * FROM """ +  self.tables['companies'] + """ ORDER BY RAND() LIMIT %s"""
		self.cursor.execute(query, amount)

		result = self.cursor.fetchall()

		return result

	def seed_companies(self, jsonfile = "../spx-companies.json"):
		''' Only needs to be run once. Get the SPX companies in there then it's done'''

		rawjson = open(jsonfile, 'r')
		jsondata = json.load(rawjson)
		data = []

		if (self.table_has_data('spx_companies')):
			return "Table already has data."

		for row in jsondata:
			data.append((row['Symbol'], row['Name'], row['Sector'], row['Dividend Yield'], row['Price/Earnings'], row['Earnings/Share'], row['52 week low'], row['52 week high'], row['Market Cap'], row['SEC Filings']))

		# This query looks weird because table names can't be variables in MySQLdb
		self.cursor.executemany(
			""" INSERT INTO """ + self.tables['companies'] + """ (ticker, companyname, sector, dividend, price_earnings, earnings_share, year_low, year_high, market_cap, sec_filings)
				VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """,
				data
		)

		self.db.connection.commit()

		return "Successfully Seeded"


	def table_exists(self, tablename = ""):

		self.cursor.execute("SHOW TABLES LIKE %s", ("%" + tablename + "%"))
		result = self.cursor.fetchone()
		if result:
			return True

		return False

	def table_has_data(self, tablename = ""):

		result = False

		if self.table_exists(tablename):
			self.cursor.execute("SELECT id FROM %s" % tablename)
			result = self.cursor.rowcount

		return result

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