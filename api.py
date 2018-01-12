import json
import mongo
import pickle
from flask import Flask, request
from twitter import Twitter
from collections import namedtuple
from elasticsearch import Elasticsearch

config = json.load(open("config.json", 'r'))

twitterCredentials = config['twitter']
consumer_key = twitterCredentials['consumer_key']
consumer_secret = twitterCredentials['consumer_secret']
access_token = twitterCredentials['access_token']
access_token_secret = twitterCredentials['access_token_secret']

with open('lsimodel.pickle', 'rb') as f:
    lsimodel = pickle.load(f)

app = Flask(__name__)

@app.route('/')
def success():
    return "Welcome"

@app.route('/addprofile', methods=['POST'])
def addProfile():
    profile = request.form['profile']
    twitterEg = Twitter(consumer_key, consumer_secret, access_token, access_token_secret)
    tweets = twitterEg.fetchTweets(profile, limit=10)
    for tweet in tweets:
        mongo.twitterCollection.insert(tweet.__dict__)
    mongo.usersCollection.update({
        'screen_name': tweet.screen_name
    }, {
        'screen_name': tweet.screen_name
    }, True)
    
    return profile

@app.route('/rank', methods=['POST'])
def getRank():
    elasticConfig = config['elasticsearch']
    query = request.form['query']
    screen_names = mongo.usersCollection.find()
    for screen_name in screen_names:
        result = mongo.twitterCollection.find({'screen_name': screen_name['screen_name']})
        tweets = []
        for res in result:
            tweets.append(res)
        lsimodel.index()
        doc_topic_dist = lsimodel.topicDist(tweets)
        res = lsimodel.es.search(doc_type=elasticConfig['doc_type'], body={"query": {"match": {"content": query}}})
        id = int(res['hits']['hits'][0]['_id'])
        # topic_relevance = doc_topic_dist[id]
        print(doc_topic_dist[id])
    return query

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
