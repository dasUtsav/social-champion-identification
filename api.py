import json
import math
import pandas as pd
import bcrypt
import os
import mongo
import re
from flask import Flask, request, render_template, redirect, url_for, session    
from twitter import Twitter
from elasticsearch import Elasticsearch
from ranking import Ranking
from classes.TwitterGraph import TwitterGraph
from classes.TopicInfluence import TopicInfluence
from classes.MOI import MOI
from Instances import ldamodelInstance, twitterInstance
from classes.utility import fetchTimeSeries

config = json.load(open("config.json", 'r'))


twitterGraph = TwitterGraph("twitterGraph.pickle")

if os.path.isfile("twitterGraph.pickle"):
    twitterGraph.load_pickle()
else:
    twitterGraph.write_pickle()

# twitterGraph.resetRefetch()
topicInfluence = TopicInfluence(twitterGraph)
moi = MOI(twitterGraph)


#Config variables
twitterFetch = config["twitterFetch"]


app = Flask(__name__)


@app.route('/addtopics', methods=['GET'])
def success():
    return render_template('landing.html')
    # if 'username' in session:
    #     return render_template('landing.html')
    # return redirect(url_for('login'))
        

@app.route('/addtopics', methods=['POST'])
def addTopics():

    interest_list = []
    
    interests = [request.form[key] for key in request.form.keys()]
    for item in interests:
        topic = { 'name' : item, 'isPresent': False}
        res = ldamodelInstance.search(item)
        if res is not False:
            topic['isPresent'] = True
        interest_list.append(topic)

    for interest in interest_list:
        mongo.topicCollection.update({
            'name': interest['name']
            }, interest
             , True)
    print("ggwp", interest_list)
    return render_template('upload_candidates.html')
            
@app.route('/addprofile', methods=['POST'])
def addProfile():
    if 'handles' not in request.files:
        flash('No handles part')
        return redirect(request.url)
    csvFile = pd.read_csv(request.files['handles'])
    handles = csvFile['Handle'].tolist()
    for profile in handles:
        twitterGraph.add_candidate(profile, twitterFetch["max_followers"], 
                                   twitterFetch["max_follower_friends"])
    return redirect("/rank", code=200)

@app.route('/rank', methods=['GET'])
def getRank():
    topic_results = mongo.topicCollection.find()
    queries = [topic_result for topic_result in topic_results]
    filters = []
    pending_topics = []
    rank_list = []
    final_ranks = []
    df = pd.read_csv("./handles.csv")
    screen_names = df.values.tolist()

    candidates = []

    for screen_name in screen_names:
        res = twitterGraph.fetch_user(screen_name[1])
        candidates.append({'id': res.id, 
                           'screen_name': screen_name[1],
                           'name': screen_name[0],
                           'topic_relevance': 0,
                           'image_url': res.profile_image_url})

    ranks = topicInfluence.compute_rank(twitterFetch["max_tweets"], [
                           candidate['id'] for candidate in candidates])
    for i, rank in enumerate(ranks):
        candidates[i] = dict(candidates[i], **rank)
        candidates[i]["moiScore"] = moi.fetch_moi_score(candidates[i]['id'], twitterFetch["max_tweets"])
    
    for query_dict in queries:
        topic_dist = 0
        query = query_dict['name']
        if query_dict['isPresent'] == False:
            pending_topics.append(query_dict['name'])
            for candidate in candidates:
                candidate["topic_relevance"] = 0
        else:
            rankings = []
            for candidate in candidates:
                candidateTweets = twitterGraph.fetch_preprocessed_tweets(candidate['id'], twitterFetch["max_tweets"])
                candidate["topic_relevance"] = ldamodelInstance.getTopicDistFromQuery(candidateTweets, query)
            
        ranking = Ranking(candidates)
        ranking.rank()
        rank_list = ranking.dataframe.to_dict(orient='records')

        final_ranks.append({
            'query': query,
            'rank_list': rank_list
        })
    return render_template("form.html",final_ranks = final_ranks, pending_topics = pending_topics)

@app.route('/rank/graphs')
def graphs():
    id = request.args.get('id')
    name = request.args.get('name')
    query = request.args.get('topic_name')
    user = twitterGraph.fetch_user(id=id)
    ranks = {
        'influence': float(request.args.get('influence')) * 100,
        'moiScore': float(request.args.get('moiScore')) * 100,
        'topic_relevance': float(request.args.get('topic_relevance')) * 100,
    }
    ranks = sorted(ranks.items())
    user.profile_image_url = re.sub(r'_normal', '', user.profile_image_url)

    tweets, retweets = twitterGraph.fetch_favorites(user.id, twitterFetch['max_tweets'])
    tweet_time_series, retweet_time_series = fetchTimeSeries(tweets, 'count'), fetchTimeSeries(retweets, 'count')
    tweet_time_series, retweet_time_series = sorted(tweet_time_series['count'].items()), sorted(retweet_time_series['count'].items())
    return render_template('graphs.html', tweet_time_series=tweet_time_series, 
                            retweet_time_series=retweet_time_series,
                            name=name,
                            screen_name=user.screen_name, image_url=user.profile_image_url, topic_name=query, stats=ranks)

@app.route('/login', methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        user = mongo.loginCollection
        login_user = user.find_one({ 'name' : request.form['username']})

        if login_user:
            if bcrypt.hashpw(request.form["pwd"].encode('utf-8'), login_user["password"]) == login_user["password"]:
                session['username'] = request.form['username']
                redirect(url_for('success'))
        return "Invalid username/password combination"
    return render_template("login.html")

@app.route('/register', methods = ["POST" , "GET"])
def register():
    if request.method == "POST":
        users = mongo.loginCollection
        exist = users.find_one({ 'name' : request.form['username']})
        
        if exist is None:
            hashpass = bcrypt.hashpw(request.form['pwd'].encode('utf-8'),bcrypt.gensalt())
            mongo.loginCollection.insert({ 'name' : request.form['username'] , 'password' : hashpass})
            session["username"] = request.form['username']
            return redirect(url_for("success"))
        return "Username already exist" 
    
    return render_template('register.html')

@app.route('/')
def home():
    return render_template("home.html")


if __name__ == '__main__':
    app.secret_key = "mysecret"
    app.run(host='127.0.0.1', port=8000, debug=True)
