import json
from twitter import Twitter
from topic_modeling import LDAModeling
from classes.TopicInfluence import TopicInfluence

config = json.load(open("config.json", 'r'))

twitterCredentials = config['twitter']
consumer_key = twitterCredentials['consumer_key']
consumer_secret = twitterCredentials['consumer_secret']
access_token = twitterCredentials['access_token']
access_token_secret = twitterCredentials['access_token_secret']

twitterInstance = Twitter(consumer_key, consumer_secret, access_token, access_token_secret)

ldamodelInstance = LDAModeling(config["topic_modeling"]["model_name"])
ldamodelInstance.loadPickle()
# ldamodelInstance.deleteIndex()
ldamodelInstance.index()