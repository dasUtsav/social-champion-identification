from pymongo import MongoClient

client = MongoClient('localhost:27017')
db = client['sci']
twitterCollection = db['twitter-collection']
usersCollection = db['users']
topicCollection = db['topics']
