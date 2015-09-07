from flask import Flask, render_template, g, request
from moneyky import Moneyky



app = Flask(__name__)
moneyky = Moneyky()

@app.route("/")
def hello():
	return render_template('index.html')

@app.route("/database")
def database():
	return render_template('database.html')
	
@app.route("/seed")
def seed():
	moneyky.seeddb()
	return render_template('seed.html')

@app.route('/random-portfolio')
@app.route('/random-portfolio/<amount>')
def random_portfolio(amount = 5):
	portfolio, performance = moneyky.random_portfolio(amount)
	return render_template('apicall.html', portfolio = portfolio, performance = performance)

if __name__ == "__main__":
	app.run(debug=True)
