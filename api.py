import json
import mongo
import pickle
import math
from operator import itemgetter
from flask import Flask, request, render_template
from twitter import Twitter
from collections import namedtuple
from elasticsearch import Elasticsearch
from ranking import Ranking

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
    return render_template('form.html')

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
        'screen_name': tweet.screen_name,
        'follower_count': tweet.follower_count
    }, True)
    
    return render_template("form.html")

@app.route('/rank', methods=['POST'])
def getRank():
    elasticConfig = config['elasticsearch']
    queries = ['health', 'nasw']
    filters = [request.form[key] for key in request.form.keys() if key != 'query']
    screen_names = mongo.usersCollection.find()
    sorted_rank = []
    sample = []
    rank_list = []
    final_ranks = []
    screened_tweets = []
    lsimodel.index()
    for screen_name in screen_names:
        result = mongo.twitterCollection.find({'screen_name': screen_name['screen_name']})
        tweets = []
        for res in result:
            tweets.append(res)
        screened_tweets.append({
            'screen_name': screen_name['screen_name'],
            'tweets': tweets
        })
    for query in queries:
        rankings = []
        for screened_tweet in screened_tweets:
            tweets = screened_tweet['tweets']
            doc_topic_dist, sentiment = lsimodel.topicDist(tweets)
            res = lsimodel.es.search(doc_type=elasticConfig['doc_type'], body={"query": {"match": {"content": query}}})
            if res['hits']['hits']:
                id = int(res['hits']['hits'][0]['_id'])
            else: 
                return "Topic Not Found"
            topic_relevance = doc_topic_dist[id]
            ranking = Ranking(tweets, topic_relevance, sentiment)
            if len(filters) != 0:
                ranking.rank(filters)
            else:
                ranking.rank()
            followerCountScore = screen_name['follower_count'] / 10000
            relevantTweetsCount = len(ranking.dataframe[ranking.dataframe['topic_relevance'] > 0])
            frequency = (relevantTweetsCount / len(ranking.dataframe)) * math.log(len(ranking.dataframe + 1))
            temp = { 'name' : screened_tweet['screen_name'] , 'rank' : ranking.dataframe['rank'].mean() + followerCountScore + frequency}
            rankings.append(temp)
        rank_list = sorted(rankings, key=itemgetter('rank'), reverse=True)
        rank_list = rank_list[:5]
        for index, ele in enumerate(rank_list):
            ele['rank'] = index + 1
        final_ranks.append({
            'query': query,
            'rank_list': rank_list
        })
    
    return render_template("form.html",final_ranks = final_ranks)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
