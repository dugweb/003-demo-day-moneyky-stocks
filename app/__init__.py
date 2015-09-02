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

        query = "SHOW TABLES LIKE 'snp_table'"
        moneykyDB.cursor.execute(query)
        result = moneykyDB.cursor.fetchone()
        if result:
            # there is a table named "tableName"
            pprint("table exists")
        else:
            # there are no tables named "tableName"
            query = """CREATE TABLE IF NOT EXISTS snp_table (snp_id INT NOT NULL AUTO_INCREMENT,PRIMARY KEY(snp_id), 
            Symbol varchar(10) DEFAULT NULL,  
                                                Name varchar(100) DEFAULT NULL);"""
            moneykyDB.insert_commit(query)
            # Loop through the list and insert Symbol to the snp table
            for i in range(0,len(snp500_companies)):
                row = [snp500_companies[i]['Symbol'], snp500_companies[i]['Name']]
                #pprint ((i,snp500_companies[i]['Name']))
                moneykyDB.cursor.execute("""INSERT INTO snp_table(Symbol, Name) VALUES(%s, %s)""", row)
            moneykyDB.connection.commit()
            pprint("SNP Table loaded to moneykyDB") 
        
        
        #Create the holdings table
        query = "SHOW TABLES LIKE 'holdings_table'"
        moneykyDB.cursor.execute(query)
        result = moneykyDB.cursor.fetchone()
        if result:
            # there is a table named "tableName"
            pprint("holdings table exists")
        else:
            query = """CREATE TABLE IF NOT EXISTS holdings_table  (portfolio_id INT NOT NULL AUTO_INCREMENT,PRIMARY KEY(portfolio_id), 
                                                    Performance DECIMAL(4,2) DEFAULT NULL,
                                                    snp_id INT NOT NULL,
                                                    FOREIGN KEY fk_cat(snp_id) REFERENCES snp_table(snp_id)
                                                    ON UPDATE CASCADE 
                                                    ON DELETE RESTRICT);"""
            moneykyDB.insert_commit(query)
        
    
        portfolio_of_today = chose_random_snp(moneykyDB)
        portfolio_of_today.sort()
        pprint(portfolio_of_today)
        for stock in portfolio_of_today: # snp_id:stock[0] , symbol: stock[1][0] , name: stock[1][1] , perf: stock[2]
            pprint("----")
            pprint(stock[2])
            moneykyDB.cursor.execute("""INSERT INTO holdings_table (snp_id , Performance) VALUES(%s, %s)""", (stock[0] , stock[2]))
            moneykyDB.connection.commit()
        return render_template('database.html', portfolio_of_today=portfolio_of_today)
    except Exception as e:
        return (str(e))



@app.route("/seeddb")
def seeddb():
    return "test"


if __name__ == "__main__":
    app.run(debug=True)
