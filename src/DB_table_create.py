import mysql.connector

remote = mysql.connector.connect(
    host = "database-1.ciifx43v3wkq.ap-northeast-2.rds.amazonaws.com",
    port = 3306,
    user = "root",
    password = "qaz51133",
    database = "IOT"
)

cursor = remote.cursor()
sql = open("creating_table.sql").read()
cursor.execute(sql)

remote.close()