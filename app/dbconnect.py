import MySQLdb

def connection():
	conn = MySQLdb.connect(
			host="127.0.0.1",
			user="doug",
			passwd="asdf",
			db="moneyky",
		)

	c = conn.cursor()
	return c, conn