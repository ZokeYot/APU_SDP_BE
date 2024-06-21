import mysql.connector


connection = mysql.connector.connect(
    host="localhost",
    user='root',
    password='',
    database='Testy'
)

cursor = connection.cursor()
error = mysql.connector.Error

if connection.is_connected:
    print("Connected to MySQL database")









