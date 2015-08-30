from flask import Flask
from dbconnect import connection

app = Flask(__name__)
@app.route("/")
def hello():
    return "Moneyky, Hello World"


@app.route("/database")
def database():

	try:
		c, conn = connection()
		return "database page"
	except Exception as e:
		return (str(e))





if __name__ == "__main__":
    app.run(debug=True)
