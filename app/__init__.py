from flask import Flask, render_template, g, request
from moneyky import Moneyky



app = Flask(__name__)
moneyky = Moneyky()

@app.route("/")
def hello():
	return render_template('index.html')

@app.route("/seed")
def seed():
	moneyky.seeddb()
	return render_template('seed.html')

@app.route('/random-portfolio')
@app.route('/random-portfolio/<amount>')
def random_portfolio(amount = 5):
	portfolio = moneyky.random_portfolio(amount)
	return render_template('portfolio.html', portfolio = portfolio)

@app.route('/apicall')
def apicall():
	portfolio = moneyky.random_portfolio(1)
	performance = moneyky.get_portfolio_performance(portfolio)
	return render_template('apicall.html', performance = performance)


if __name__ == "__main__":
	app.run(debug=True)
