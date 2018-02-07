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
from classes.TopicInfluence import TopicInfluence
from classes.MOI import MOI
from Instances import ldamodelInstance, twitterInstance

config = json.load(open("config.json", 'r'))


twitterGraph = TwitterGraph("twitterGraph.pickle")

if os.path.isfile("twitterGraph.pickle"):
    twitterGraph.load_pickle()
else:
    twitterGraph.write_pickle()

topicInfluence = TopicInfluence(twitterGraph)
moi = MOI(twitterGraph)


#Config variables
twitterFetch = config["twitterFetch"]


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

@app.route('/rank', methods=['GET', 'POST'])
def getRank():
    topic_results = mongo.topicCollection.find()
    queries = [topic_result for topic_result in topic_results]
    filters = []
    if request.method == 'POST':
        filters = [request.form[key] for key in request.form.keys() if key != 'query']
    sorted_rank = []
    pending_topics = []
    rank_list = []
    final_ranks = []
    screen_names = ["kyoag", "ChildAbuse_Sol", "RMP21", "ms_tina_tina", "mike_salter"]

    candidates = []

    for screen_name in screen_names:
        res = twitterGraph.fetch_user(screen_name)
        candidates.append({'id': res.id, 
                           'screen_name': screen_name,
                           'image_url': res.profile_image_url})
    for query_dict in queries:
        if query_dict['isPresent'] == False:
            pending_topics.append(query_dict['name'])
            # continue
        rankings = []
        query = query_dict['name']
        ranks = topicInfluence.compute_rank(twitterFetch["max_tweets"], [
                candidate['id'] for candidate in candidates])
        for candidate in candidates:
            result = filter(lambda rank: rank['node'] == candidate['id'], ranks)
            for res in result:
                res["moiScore"] = moi.fetch_moi_score(candidate['id'], twitterFetch["max_tweets"])
                res["name"] = candidate['screen_name']
                res["id"] = candidate['id']
                res["image_url"] = candidate['image_url']
        ranking = Ranking(ranks)
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
    query = request.args.get('topic_name')
    user = twitterGraph.fetch_user(id=id)
    queryMongo = mongo.topicCollection.find({
        'name': query
    })
    ranks = topicInfluence.compute_rank(twitterFetch["max_tweets"], [user.id])
    ranks[0]['moiScore'] = moi.fetch_moi_score(user.id, twitterFetch["max_tweets"])
    for res in queryMongo:
        query = res["name"]
    return render_template('graphs.html', name=user.screen_name, image_url=user.profile_image_url, topic_name=query, stats=ranks[0])

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
