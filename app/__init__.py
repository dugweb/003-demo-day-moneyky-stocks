from flask import Flask, render_template, g, request
from dbconnect import Database
from readjson import readjson
from pprint import pprint
from dbactions import *
import moneyky

app = Flask(__name__)
@app.route("/")
def hello():
    return "Moneyky, Hello World"

@app.route("/database")
def database():
    try:
        return render_template('database.html', moneyky, snp_perf=snp_perf , moneyky_perf=moneyky_perf)
    except Exception as e:
        return (str(e))

if __name__ == "__main__":
    app.run(debug=True)
