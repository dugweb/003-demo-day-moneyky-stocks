import pymysql.cursors

def connection():
	conn = pymysql.connect(
			host="localhost",
			user="root",
			passwd="asdf",
			db="moneyky",
			charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
		)

	c = conn.cursor()
	return c, conn