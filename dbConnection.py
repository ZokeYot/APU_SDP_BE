import mysql.connector
from pymongo import MongoClient

class MySQL_DB:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user='root',
            password='20040506',
            database='Testy'
        )
        self.cursor = self.connection.cursor()
        self.error = mysql.connector.Error

        if self.connection.is_connected():
            print("Connected to MySQL database")


class Mongo_DB:
    def __init__(self):
        client = MongoClient('mongodb://localhost:27017')
        print('Connected to MongoDB server successfully.')

        db = client['Testy']
        collection = db['Question']

        cursor = collection.find({} , {'_id' : 0})
        for document in cursor:
            print(document)









