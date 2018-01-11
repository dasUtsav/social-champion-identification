import json
from flask import Flask, request
from twitter import Twitter
from pymongo import MongoClient

config = json.load(open("config.json", 'r'))

twitterCredentials = config['twitter']
consumer_key = twitterCredentials['consumer_key']
consumer_secret = twitterCredentials['consumer_secret']
access_token = twitterCredentials['access_token']
access_token_secret = twitterCredentials['access_token_secret']

app = Flask(__name__)

@app.route('/')
def success():
    return "Welcome"

@app.route('/addprofile', methods=['POST'])
def addProfile():
    profile = request.form['profile']
    twitterEg = Twitter(consumer_key, consumer_secret, access_token, access_token_secret)
    tweets = twitterEg.fetchTweets(profile, limit=10)
    client = MongoClient('mongodb://sciuser:scipass@ds251827.mlab.com:51827/sci')
    db = client['sci']
    collection = db['twitter-collection']
    for tweet in tweets:
        collection.insert(tweet.__dict__)
    return profile

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
