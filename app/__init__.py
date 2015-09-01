from flask import Flask
from dbconnect import Database
from readjson import readjson
from pprint import pprint


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
		return "SNP Table loaded and updated to moneykyDB"
	except Exception as e:
		return (str(e))


@app.route("/seeddb")
def seeddb():
	return "test"


if __name__ == "__main__":
    app.run(debug=True)
