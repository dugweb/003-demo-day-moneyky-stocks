
from dbconnect import Database as DB


class Moneyky(object):


	def __init__():

		# Connect to the databasee
		# if snp_companies table is empty then 
		# seeddb()
		pass




	def seeddb(self):
		''' runs once if there are no companies in the snp_companies file '''
		# snp500_companies = readjson('../spx-companies.json')
		# #pprint (snp500_companies)

		# query = "SHOW TABLES LIKE 'snp_table'"
		# moneykyDB.cursor.execute(query)
		# result = moneykyDB.cursor.fetchone()
		# if result:
		#     # there is a table named "tableName"
		#     pprint("table exists")
		# else:
		#     # there are no tables named "tableName"
		#     query = """CREATE TABLE IF NOT EXISTS snp_table (snp_id INT NOT NULL AUTO_INCREMENT,PRIMARY KEY(snp_id), 
		#     Symbol varchar(10) DEFAULT NULL,  
		#                                         Name varchar(100) DEFAULT NULL);"""
		#     moneykyDB.insert_commit(query)
		#     # Loop through the list and insert Symbol to the snp table
		#     for i in range(0,len(snp500_companies)):
		#         row = [snp500_companies[i]['Symbol'], snp500_companies[i]['Name']]
		#         #pprint ((i,snp500_companies[i]['Name']))
		#         moneykyDB.cursor.execute("""INSERT INTO snp_table(Symbol, Name) VALUES(%s, %s)""", row)
		#     moneykyDB.connection.commit()
		#     pprint("SNP Table loaded to moneykyDB") 

	def portfolio_of_day(self):
		'''This function is the one that will run once per day - Important Function'''
		# get random_portfolio(50)
		# get_ticker_performance('^GSPC') # snp performance

		# set_days_performance() 
		# set_portfolio(holdings) 
		



	def random_portfolio(self, holdings = 10):
		''' creates a list of holdings with their associated performance '''	    
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
