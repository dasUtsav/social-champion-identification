from pymongo import MongoClient

client = MongoClient('mongodb://sciuser:scipass@ds251827.mlab.com:51827/sci')
db = client['sci']
twitterCollection = db['twitter-collection']
usersCollection = db['users']
