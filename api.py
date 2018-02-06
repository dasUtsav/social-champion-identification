import json
import pickle
import math
import pandas as pd
import bcrypt
import os
import mongo
from operator import itemgetter
from flask import Flask, request, render_template, redirect, url_for, session    
from twitter import Twitter
from collections import namedtuple
from elasticsearch import Elasticsearch
from ranking import Ranking
from classes.TwitterGraph import TwitterGraph
from Instances import ldamodelInstance

config = json.load(open("config.json", 'r'))


twitterGraph = TwitterGraph("twitterGraph.pickle")
if os.path.isfile("twitterGraph.pickle"):
    twitterGraph.load_pickle()
else:
    twitterGraph.add_candidate('nasw', max_followers, max_follower_friends)
    twitterGraph.save_pickle()


app = Flask(__name__)


@app.route('/')
def success():
    return render_template('landing.html')
    # if 'username' in session:
    #     return render_template('landing.html')
    # return redirect(url_for('login'))
        

@app.route('/addtopics', methods=['POST'])
def addTopics():

    interest_list = []
    
    elasticConfig = config['elasticsearch']
    interests = [request.form[key] for key in request.form.keys()]
    for item in interests:
        topic = { 'name' : item, 'isPresent': False}
        res = ldamodelInstance.search(item)
        if res is not False:
            topic['isPresent'] = True
        interest_list.append(topic)
        print(interest_list)
    print(interest_list)

    for interest in interest_list:
        mongo.topicCollection.update({
            'name': interest['name']
            }, interest
             , True)

    return render_template('upload_candidates.html')
            
@app.route('/addprofile', methods=['POST'])
def addProfile():
    if 'handles' not in request.files:
        flash('No handles part')
        return redirect(request.url)
    twitterFetch = config["twitterFetch"]
    csvFile = pd.read_csv(request.files['handles'])
    handles = csvFile['Handle'].tolist()
    for profile in handles:
        twitterGraph.add_candidate(profile, twitterFetch["max_followers"], 
                                   twitterFetch["max_follower_friends"])
    return redirect("/rank", code=200)

@app.route('/rank', methods=['GET', 'POST'])
def getRank():
    elasticConfig = config['elasticsearch']
    topic_results = mongo.topicCollection.find()
    queries = [topic_result for topic_result in topic_results]
    print(queries)
    filters = []
    if request.method == 'POST':
        filters = [request.form[key] for key in request.form.keys() if key != 'query']
    screen_names = mongo.usersCollection.find()
    sorted_rank = []
    pending_topics = []
    rank_list = []
    final_ranks = []
    screened_tweets = []
    
    for screen_name in screen_names:
        result = mongo.twitterCollection.find({'screen_name': screen_name['screen_name']})
        tweets = []
        for res in result:
            tweets.append(res)
        screened_tweets.append({
            'screen_name': screen_name['screen_name'],
            'tweets': tweets
        })
    for query_dict in queries:
        print("Query_dict is:")
        print(query_dict)
        if query_dict['isPresent'] == False:
            pending_topics.append(query_dict['name'])
            continue
        rankings = []
        query = query_dict['name']
        for screened_tweet in screened_tweets:
            tweets = screened_tweet['tweets']
            doc_topic_dist, sentiment = ldamodelInstance.topicDist(tweets)
            id = ldamodelInstance.search(query)
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
    
    return render_template("form.html",final_ranks = final_ranks, pending_topics = pending_topics)

@app.route('/rank/graphs')
def graphs():
    return render_template('graphs.html')

@app.route('/login', methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        user = mongo.loginCollection
        login_user = user.find_one({ 'name' : request.form['username']})

        if login_user:
            print(login_user)
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

if __name__ == '__main__':
    app.secret_key = "mysecret"
    app.run(host='127.0.0.1', port=8000, debug=True)
