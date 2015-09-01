from flask import Flask, render_template, g, request
from dbconnect import Database
from readjson import readjson
from pprint import pprint
from dbactions import *


app = Flask(__name__)
@app.route("/")
def hello():
    return "Moneyky, Hello World"


@app.route("/database")
def database():
	try:
		moneykyDB = Database("moneyky")
		snp500_companies = readjson('../spx-companies.json')
		#pprint (snp500_companies)
		Cols = snp500_companies[0].keys()
		Rows = snp500_companies[0].values()
		#pprint (insertCols)

		#Delete the table if it exists (#TODO :should be removed at production time)
		query = """DROP TABLE IF EXISTS snp"""
		moneykyDB.insert_commit(query)
		query = """CREATE TABLE snp (id INT NOT NULL AUTO_INCREMENT,PRIMARY KEY(id), Symbol varchar(10) DEFAULT NULL);"""
		moneykyDB.insert_commit(query)

		# Loop through the list and insert Symbol to the snp table
		for i in range(0,len(snp500_companies)):
			#pprint ((i,snp500_companies[i]['Symbol']))
			moneykyDB.cursor.execute("""INSERT INTO snp(Symbol) VALUES(%s)""", (snp500_companies[i]['Symbol']))
		moneykyDB.connection.commit()
		pprint("SNP Table loaded and updated to moneykyDB")		
		portfolio_of_today = chose_random_snp(moneykyDB)
		portfolio_of_today.sort()
		pprint(portfolio_of_today)
		return render_template('database.html', portfolio_of_today=portfolio_of_today)
	except Exception as e:
		return (str(e))



@app.route("/seeddb")
def seeddb():
	return "test"


if __name__ == "__main__":
    app.run(debug=True)
