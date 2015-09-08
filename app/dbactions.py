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
		self.cursor.execute(query, amount )

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

		self.commit()

		return "Successfully seeded " + str(len(data)) + " companies."


	def set_portfolio(self, portfolio):

		portfoliovalues = (portfolio['date'], portfolio['performance_ytd'], portfolio['performance_1year'], portfolio['benchmark_ytd'], portfolio['benchmark_1year'])

		#insert portfolio
		self.cursor.execute("""
				INSERT INTO """ + self.tables['portfolios'] + """ (date, performance_ytd, performance_1year, benchmark_ytd, benchmark_1year)
				VALUES (%s, %s, %s, %s, %s) """,
				portfoliovalues
			)
		self.commit()
		
		#insert holdings
		self.cursor.execute(""" SELECT LAST_INSERT_ID() """)
		lastid = self.cursor.fetchone()[0]

		holdingsvalues = []
		for holding in portfolio['holdings']:
			holdingsvalues.append((holding['ticker'], lastid, holding['close'], holding['1yearprice'], holding['1yearperformance'], holding['ytdprice'], holding['ytdperformance']))

		self.cursor.executemany("""
			INSERT INTO """ + self.tables['holdings'] + """ (company_id, portfolio_id, close, 1yearprice, 1yearperformance, ytdprice, ytdperformance)
			VALUES ((SELECT `id` FROM """ + self.tables['companies'] + """ WHERE `ticker` = %s LIMIT 1), %s, %s, %s, %s, %s, %s)""",
			holdingsvalues
		)
		self.commit()
	
	def get_all_portfolios(self):
		''' returns a dictionary of all the portfolios '''
		self.cursor.execute("""
			SELECT * FROM """ + self.tables['portfolios'] + """ LIMIT 200
		""")

		portfolios = self.cursor.fetchall()
		result = []
		for portfolio in portfolios:
			result.append({
				'id'				: portfolio[0],
				'date'				: portfolio[1],
				'performance_ytd'	: portfolio[2],
				'performance_1year'	: portfolio[3],
				'benchmark_ytd'		: portfolio[4],
				'benchmark_1year'	: portfolio[5]
			})

		return result

	def get_portfolio_and_companies(self):
		self.cursor.execute(""" 
				SELECT p.date, p.performance_ytd, p.performance_1year, p.benchmark_ytd, p.benchmark_1year
				FROM """ + self.tables['portfolios'] + """ p
				WHERE p.id = ( SELECT MAX(id) FROM """ + self.tables['portfolios'] + """)
			""")

		portfolio = self.cursor.fetchone()


		self.cursor.execute(""" 
				SELECT 	h.close, h.1yearprice, h.1yearperformance, h.ytdprice, h.ytdperformance, 
						c.ticker, c.companyname, c.sector, c.price_earnings, c.earnings_share, c.market_cap, c.sec_filings
				FROM """ + self.tables['portfolios'] + """ p
				JOIN """ + self.tables['holdings'] + """ h ON h.`portfolio_id` = p.id
				JOIN """ + self.tables['companies'] + """ c ON c.id = h.company_id
				WHERE p.id = ( SELECT MAX(id) FROM """ + self.tables['portfolios'] + """)
			""")

		companies = self.cursor.fetchall()
		holdings = []


		if not portfolio or holdings:
			return
			
		for company in companies:
			holdings.append({
				'close'				: company[0],
				'1yearprice'		: company[1],
				'1yearperformance'	: company[2],
				'ytdprice'			: company[3],
				'ytdperformance'	: company[4],
				'ticker'			: company[5],
				'companyname'		: company[6],
				'sector'			: company[7],
				'price_earnings'	: company[8],
				'earnings_share'	: company[9],
				'market_cap'		: company[10],
				'sec_filings'		: company[11],
				})

		results = {
			'portfolio' : {
				'date'				: portfolio[0],
				'performance_ytd'	: portfolio[1],
				'performance_1year'	: portfolio[2],
				'benchmark_ytd'		: portfolio[3],
				'benchmark_1year'	: portfolio[4]
			},
			'holdings'	: holdings
		}

		return results

	def commit(self):
		try:
			self.db.connection.commit()
		except:
			self.db.session.rollback()

	### ####################################################
	### Helper Functions ###

	def table_exists(self, tablename = ""):
		'''Returns if a table with the supplied name exists'''
		self.cursor.execute("SHOW TABLES LIKE %s", ("%" + tablename + "%",))
		result = self.cursor.fetchone()
		if result:
			return True

		return False

	def table_has_data(self, tablename = ""):
		'''Tells you if the table has any data already in there'''
		result = False

		if self.table_exists(tablename):
			self.cursor.execute("SELECT id FROM %s" % tablename)
			result = self.cursor.rowcount

		return result