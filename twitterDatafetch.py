import tweepy
import json

consumer_key = "rLSO59KOXRjjWisGpsuqqaEdJ"
consumer_secret = "rprRhqIsgxY49qFZlpRZmZs7pMXcFoJrGmryoRUUmXRQm6E9v0"

access_token = "420400261-Qknhgi9XaPv1ZklKdV68Ef4ZzbmjyPTFKynzW2WR"
access_token_secret = "B077y0aYdHAntBR0GKB84xHqkofTW2a99qb42iptprDwE"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

op_file = open("output.json", "w")

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
number=0
res = {}
for status in tweepy.Cursor(api.user_timeline, id=user.screen_name, tweet_mode='extended').items(1):
    res = json.dumps(status._json)
    op_file.write(res)
op_file.close()

    