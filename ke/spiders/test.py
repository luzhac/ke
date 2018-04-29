# Requires pymongo 3.6.0+
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
database = client["keqq"]
collection = database["ke"]

# Created with Studio 3T, the IDE for MongoDB - https://studio3t.com/

query = {}
sort = [ (u"mianfei", 1) ]

cursor = collection.find(query, sort = sort)
try:
    for doc in cursor:
        print(doc)
finally:
    client.close()