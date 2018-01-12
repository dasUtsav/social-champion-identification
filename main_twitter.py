import os
import pickle
import json
from twitter import Twitter
from text_cleansing_step1 import Text_retrieve
from topic_modeling import LSIModeling
from elasticsearch import Elasticsearch

config = json.load(open("config.json", 'r'))

# Twitter api credentials

twitterCredentials = config['twitter']

consumer_key = twitterCredentials['consumer_key']
consumer_secret = twitterCredentials['consumer_secret']
access_token = twitterCredentials['access_token']
access_token_secret = twitterCredentials['access_token_secret']

# Defining twitter object

twitterEg = Twitter(consumer_key, consumer_secret, access_token, access_token_secret)

save = 'tweets.pickle'

# If the pickle file exists for the tweets, fetch the same directly, else fetch from api

if os.path.exists(os.path.join(os.path.dirname('__file__'), save)):
    with open(save, 'rb') as f:
        tweets = pickle.load(f)
else:
    tweets = twitterEg.fetchTweets('nasw', limit=1000)
    with open(save, 'wb') as f:
        pickle.dump(tweets, f)

textAndNoise = Text_retrieve(tweets)

lemmatized = textAndNoise.lemmatize()

lsimodel = LSIModeling()
lsimodel.train(lemmatized, num_topics=20)

with open('lsimodel.pickle', 'wb') as f:
    pickle.dump(lsimodel, f)

# elasticConfig = config['elasticsearch']

# es = Elasticsearch([{'host': elasticConfig['host'], 'port': elasticConfig['port']}])

# index = elasticConfig['index']
# doc_type = elasticConfig['doc_type']

# if not es.indices.exists(index):
#     print("creating index")
#     for i in range(len(lsimodel.topics)):
#         es.create(index=index, doc_type=doc_type, id=i+1, body={"content": str(lsimodel.topics[i])})

    
