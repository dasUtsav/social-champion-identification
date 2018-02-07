import networkx as nx
import mongo
import json
from text_cleansing_step1 import Text_retrieve
from Instances import twitterInstance
from gensim.models import ldamodel
from gensim import corpora
from twitter import User

config = json.load(open("config.json", 'r'))

class TwitterGraph:

    def __init__(self, fileName):
        self.G = nx.DiGraph()
        self.file_name = fileName

    def load_pickle(self):
        self.G = nx.read_gpickle(self.file_name)
    
    def write_pickle(self):
        nx.write_gpickle(self.G, self.file_name)
    
    def add_candidate(self, screen_name, max_followers, max_follower_friends, force_fetch = False):
        res = self.fetch_user(screen_name=screen_name)
        if not force_fetch and res.id in self.G.nodes():
            print("Candidate already exists")
            return
        self.G.add_node(res.id, status_count = res.statuses_count, 
                        screen_name = res.screen_name, similarity={},
                        followers_count = res.followers_count,
                        isRetrieve = False)
        users = twitterInstance.fetchFollowers(res.id, limit=max_followers)
        
        for user in users:
            if not user.id in self.G.nodes():
                self.G.add_node(user.id, similarity = {})
            self.G.add_node(user.id, status_count = user.statuses_count, 
                            screen_name = user.screen_name,
                            followers_count = user.followers_count,
                            isRetrieve = False)
            if not self.G.has_edge(user.id, res.id):
                self.G.add_edge(user.id, res.id, retweets=0)
            try:
                friends = twitterInstance.fetchFollowers(user.id, limit=max_follower_friends)
            except:
                friends = []

            for friend in friends:
                if not friend.id in self.G.nodes():
                    self.G.add_node(friend.id, similarity = {})
                self.G.add_node(friend.id, 
                                status_count = friend.statuses_count, 
                                screen_name = friend.screen_name,
                                followers_count = user.followers_count,
                                isRetrieve = False)
                if not self.G.has_edge(user.id, friend.id):
                    self.G.add_edge(user.id, friend.id, retweets=0)

        self.write_pickle()

    def fetch_tweets(self, screen_id, max_tweets):
        if self.G.node[screen_id]['isRetrieve'] == False:
            tweets = self.fetch_and_store(screen_id, max_tweets)
        else:
            tweets = mongo.twitterCollection.find({'user_id': screen_id})
            tweets = [tweet for tweet in tweets]
        text_retrieve = Text_retrieve(tweets)
        tweet_doc = text_retrieve.lemmatize()
        return tweet_doc

    def fetch_user(self, screen_name=None, id=None):
        assert (id is not None or screen_name is not None)
        userMongo = mongo.usersCollection.find({'$or':[ {'screen_name':screen_name}, {'id':id}]})
        if userMongo.count() == 0:
            screen_name = screen_name if screen_name is not None else id
            user = twitterInstance.fetchUser(screen_name)
            mongo.usersCollection.insert(user.__dict__)
        else:
            user = [user for user in userMongo]
            user = User(user[0])
        return user

    def fetch_and_store(self, screen_id, max_tweets):
        tweets = twitterInstance.fetchTweets(screen_id, max_tweets)
        for tweet in tweets:
            mongo.twitterCollection.insert(tweet.__dict__)
        self.G.node[screen_id]['isRetrieve'] = True
        self.write_pickle()
        return tweets

    def fetch_favourites(self, screen_id, max_tweets):
        if self.G.node[screen_id]['isRetrieve'] == False:
            tweets = self.fetch_and_store(screen_id, max_tweets)
            favourite_counts = [tweet.favourite_count for tweet in tweets]
            retweet_counts = [tweet.retweet_count for tweet in tweets]
        else:
            tweets = mongo.twitterCollection.find({'user_id': screen_id})
            tweets = [tweet for tweet in tweets]
            favourite_counts = [tweet['favourite_count'] for tweet in tweets]
            retweet_counts = [tweet['retweet_count'] for tweet in tweets]
        return favourite_counts, retweet_counts

    def set_tweet_doc(self, screen_id, max_tweets):
        tweet_doc = self.fetch_tweets(screen_id, max_tweets)
        # self.G.node[screen_id]['tweet_doc'] = [word for tweet in tweet_doc for word in tweet]
        self.G.node[screen_id]['tweet_doc'] = tweet_doc
        return tweet_doc

    def set_model(self, screen_name, max_tweets, fetchTweetDoc=False):
        res = self.fetch_user(screen_name=screen_name)
        if fetchTweetDoc is True:
            tweet_doc = self.set_tweet_doc(res.id, max_tweets)
        else:   
            tweet_doc = self.G.node[res.id]['tweet_doc']
        self.model, self.dictionary = self.createModel(tweet_doc)

    def createModel(self, doc):
        dictionary = corpora.Dictionary(doc)
        corpus = [dictionary.doc2bow(text) for text in doc]
        model = ldamodel.LdaModel(corpus, num_topics=config["topic_modeling"]["num_topics"], id2word = dictionary)
        return model, dictionary

    def reset_prop(self, prop, value):
        for node in self.G.nodes():
            self.G.node[node][prop] = value

    def resetRefetch(self):
        for node in self.G.nodes():
            self.G.node[node]['isRetrieve'] = False
        mongo.twitterCollection.remove()
        self.write_pickle()

        

        