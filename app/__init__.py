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

		#Delete the table if it exists (#TODO :should be removed at production time)
		query = """DROP TABLE IF EXISTS snp_table"""
		moneykyDB.insert_commit(query)
		query = """CREATE TABLE snp_table (id INT NOT NULL AUTO_INCREMENT,PRIMARY KEY(id), Symbol varchar(10) DEFAULT NULL,  Name varchar(100) DEFAULT NULL);"""
		moneykyDB.insert_commit(query)

		# Loop through the list and insert Symbol to the snp table
		for i in range(0,len(snp500_companies)):
			row = [snp500_companies[i]['Symbol'], snp500_companies[i]['Name']]
			#pprint ((i,snp500_companies[i]['Name']))
			moneykyDB.cursor.execute("""INSERT INTO snp_table(Symbol, Name) VALUES(%s, %s)""", row)
		moneykyDB.connection.commit()
		pprint("SNP Table loaded to moneykyDB")		
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
