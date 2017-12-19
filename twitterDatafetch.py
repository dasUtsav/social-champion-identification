import tweepy
import json
from pymongo import MongoClient

consumer_key = "rLSO59KOXRjjWisGpsuqqaEdJ"
consumer_secret = "rprRhqIsgxY49qFZlpRZmZs7pMXcFoJrGmryoRUUmXRQm6E9v0"

access_token = "420400261-Qknhgi9XaPv1ZklKdV68Ef4ZzbmjyPTFKynzW2WR"
access_token_secret = "B077y0aYdHAntBR0GKB84xHqkofTW2a99qb42iptprDwE"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# op_file = open("output.json", "w")

# public_tweets = api.home_timeline()
# for tweet in public_tweets:
#     print(tweet.text)

user = api.get_user('realDonaldTrump')

# print(user.screen_name)
# print(user.followers_count)
# for friend in user.friends():
#    print(friend.screen_name)
# followers = api.followers(user.screen_name)
# print(len(followers))
# res = {}
# for status in tweepy.Cursor(api.user_timeline, id=user.screen_name, tweet_mode='extended').items(6):
#     res = json.dumps(status._json)
#     op_file.write(res)
# op_file.close()

client = MongoClient('mongodb://localhost:27017/')
db = client['twitter-db']
collection = db['twitter-collection']
collection.remove({})

for status in tweepy.Cursor(api.user_timeline, id=user.screen_name, tweet_mode='extended').items():
    # status = json.loads(status._json)
    # print(status.full_text)
    collection.insert(status._json)

# tweets = collection.find()
# for tweet in tweets:
#     print(tweet['full_text'])
#     print(tweet['retweet_count'])

print(collection.count())