from flask import Flask, render_template, g, request, redirect, url_for
from moneyky import Moneyky
from bokeh import embed



app = Flask(__name__)
moneyky = Moneyky()

@app.route("/")
def hello():
	portfolio = moneyky.get_portfolio()
	if not portfolio: 
		return redirect(url_for('seed'))
	return render_template('index.html', portfolio = portfolio)

@app.route("/about")
def about():
	return render_template('about.html')

@app.route("/seed")
def seed():
	results = moneyky.seeddb()
	return render_template('seed.html', data = results)

@app.route('/random-portfolio')
@app.route('/random-portfolio/<amount>')
def random_portfolio(amount = 5):
	portfolio = moneyky.random_portfolio(amount)
	return render_template('portfolio.html', portfolio = portfolio)

@app.route('/apicall')
def apicall():
	portfolio = moneyky.random_portfolio(5)
	performance = moneyky.get_holdings_performance(portfolio)
	return render_template('apicall.html', performance = performance)


@app.route('/chart')
def chart():
	plot, portfolio_results = moneyky.chart_results()
	portfolios = portfolio_results['portfolios']
	overview = portfolio_results['overview']
	script, div = embed.components(plot)
	return render_template('chart.html', script=script,  div=div, portfolios = portfolios, overview = overview)

@app.route('/company/<ticker>')
def company(ticker):
	#TODO DOUG
	company = moneyky.get_company(ticker)
	return render_template('detail.html', company = company)


if __name__ == "__main__":
	app.run(debug=True)
