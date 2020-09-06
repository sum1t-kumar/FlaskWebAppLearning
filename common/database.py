import pymongo


class Database:

    # local mongoDB connection
    # URI = "mongodb://127.0.0.1:27017/test_db"
    # DATABASE = pymongo.MongoClient(URI).get_database()

    # Atlas cloud mongoDB connection

    client = pymongo.MongoClient("mongodb+srv://chysumit:ow4MkJTh0dTu07oK@cluster0-elbga.mongodb.net/test?retryWrites=true&w=majority")
    DATABASE = client.test

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def update(collection, query, data):
        Database.DATABASE[collection].update_one(query, data, upsert=True)

    @staticmethod
    def update_many(collection, query, data):
        Database.DATABASE[collection].update_many(query, data, upsert=True)

    @staticmethod
    def remove(collection, query):
        return Database.DATABASE[collection].remove(query)

