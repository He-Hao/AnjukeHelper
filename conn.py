from pymongo import MongoClient

conn = MongoClient('127.0.0.1', 27017)
db = conn.Anjuke
house = db.house

