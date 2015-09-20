from dbactions import MoneykyDB
from datetime import datetime, date
import time
import requests
import urllib
import json
from pprint import pprint
from numpy import cumprod, linspace, random
from bokeh.plotting import figure, show, output_file, vplot


class Moneyky(object):


    def __init__(self):

        self.db = MoneykyDB()


    def portfolio_of_day(self, amount = 30, bench = "SPX"):
        '''This function is the one that will run once per day - Important Function'''
        
      

        companies = self.random_portfolio(amount)

        
        holdings = self.get_holdings_performance(companies)
        benchmark = self.get_ticker_performance(bench, True)
        output = {
            'date'				: holdings[0]['today'],
            'performance_ytd' 	: self.average_performance('ytdperformance', holdings),
            'performance_1year' : self.average_performance('1yearperformance', holdings),
            'benchmark_ytd' 	: benchmark['ytdperformance'],
            'benchmark_1year'	: benchmark['1yearperformance'],
            'holdings'			: holdings
        }
        
        self.portfolio = output
        self.save()
        return output

        
    def get_holdings_performance(self, holdings = []):
        ''' creates a list of holdings with their associated performance (Data from http://dev.markitondemand.com) '''	    

        tickerlist = [company[1] for company in holdings if not company == None]

        data = []
        
        for ticker in tickerlist:
            data.append(self.get_ticker_performance(ticker))

        return data


    def get_ticker_performance(self, ticker, index = False):
        ''' helper function to get a single stock's performance from Yahoo Finance'''
        ### Construct API Call ###
        url = "http://www.bloomberg.com/markets/chart/data/1Y/" + ticker

        if index or ticker == 'SPX':
            url += ":IND"
        else:
            url += ":US"
        
        response = requests.get(url)
        result = response.json()

        # For testing
        # response = open('../sample-historical-data.json', 'r')
        # result = json.load(response)		

        prices = result['data_values']
        if prices:
            closingdate = self.timestamp_to_date(prices[-1][0])
            ytdindex = self.find_index_of_date(prices, closingdate, 'ytd')
            yearindex = self.find_index_of_date(prices, closingdate, 'year')
            
            return {	
                'ticker'			: ticker,
                'today'				: self.timestamp_to_date(prices[-1][0], True),
                'close'				: prices[-1][1],
                '1year'				: self.timestamp_to_date(prices[yearindex][0], True),
                '1yearprice'		: prices[yearindex][1],
                '1yearperformance'	: self.percent_growth(prices[yearindex][1], prices[-1][1]),
                'ytd'				: self.timestamp_to_date(prices[ytdindex][0], True),
                'ytdprice'			: prices[ytdindex][1],
                'ytdperformance'	: self.percent_growth(prices[ytdindex][1], prices[-1][1])
            }

    def seeddb(self, amount = 30):
        ''' runs once if there are no companies in the snp_companies file '''
        output = self.db.seed_companies("/var/www/moneyky/spx-companies.json")
       # output += self.portfolio_of_day(amount)
        return output



    def random_portfolio(self, amount = 10):
        return self.db.get_random_companies(amount)

    def save(self):
        ''' Save everything to the database after we're happy with it '''

        if (self.portfolio):
            self.db.set_portfolio(self.portfolio)


    def get_portfolio(self, date = None):
        portfolio = self.db.get_portfolio_and_companies(date)

        if portfolio:
            return portfolio
        else:
            return

    def get_company(self, ticker):
        return self.db.get_company_by_ticker(ticker)


    def chart_results(self):
        portfolios = self.db.get_all_portfolios()
        
        portfolio_results = {
            'portfolios': portfolios,
            'overview'   : {
                'ytd'   : self.average_performance('difference_ytd', portfolios),
                '1year' : self.average_performance('difference_1year', portfolios)
            }
        }
        portfolio_results['overview']['results_ytd'] = self.outperform(portfolio_results['overview']['ytd'])
        portfolio_results['overview']['results_1year'] = self.outperform(portfolio_results['overview']['1year'])


        num_points = len(portfolios)
        pprint(num_points)
        now = time.time()
        dates =[]
        moneyky_perf=[]
        portfolio_perf=[]

        #Form the lists
        for each in portfolios:
            dates.append(each['date'])
            moneyky_perf.append(float(each['difference_ytd']))
            portfolio_perf.append(float(each['difference_1year']))
        TOOLS = "pan,wheel_zoom,box_zoom,reset,save"
        r = figure(x_axis_type = "datetime", tools=TOOLS, plot_width=800, plot_height=400)
        r.line(dates, portfolio_perf, legend='Monkey ytd', color="firebrick", alpha=0.8, line_width=4)
        r.line(dates, moneyky_perf,  legend='Monkey 1 Year', color="navy", alpha=0.8, line_width=4)
        r.title = "Moneyky vs Benchmark Performance"

        r.grid.grid_line_alpha=100
        return (vplot(r)), portfolio_results  # return the plot

    ### ##########################################################
    ### Helper Functions ###

   
    def outperform(self, difference):
        if difference > 0:
            return "outperform"
        elif difference == 0:
            return "inline"
        else:
            return "underperform"

    def find_index_of_date(self, dates = [], closingdate = "", date = 'ytd'):
        '''The first day of trading isn't always January 1st, so this finds the index first day of trading'''
        
        if not closingdate:
            closingdate = datetime.now()

        Datetofind = None
        if (date == 'ytd'):
            Datetofind = datetime(closingdate.year, 1, 1)
        else:
            Datetofind = datetime(closingdate.year - 1, closingdate.month, closingdate.day)

        utcDatetofind = self.date_to_timestamp(Datetofind)

        count = 0
        for time, price in dates:
                
            if utcDatetofind <= time:
                return count
            count += 1

        return

    def average_performance(self, columnname = '1yearperformance', holdings = [] ):
        allperformances = [stock[columnname] for stock in holdings if not stock == None]
        return round(sum(allperformances) / len(allperformances), 2)

    def percent_growth(self, originalprice = 0, currentprice = 0):
        ''' Return the Percent Change '''
        dif = currentprice - originalprice
        return round((dif / originalprice) * 100, 2)	

    def timestamp_to_date(self, timestamp, string = False):
        ''' timestamps are in milliseconds so divide by 1000 '''
        time = datetime.fromtimestamp(timestamp/1000)

        if string:
            return time.strftime("%Y-%m-%d %H:%M:%S")

        return time

    def date_to_timestamp(self, date):
        ''' takes datetime object and returns unix timestamp '''
        return int(time.mktime(date.timetuple()) * 1000)


# judist = Moneyky()
# p = judist.judist()


# r = judist.get_holdings_performance(['AAPL'])
# print r

# print judist.timestamp_to_date(1441382220000)
