from pymongo import MongoClient

conn = MongoClient('127.0.0.1', 27017)
db = conn.test
house = db.house
