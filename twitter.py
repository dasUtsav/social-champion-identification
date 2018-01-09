import tweepy, json

class Tweet:
    def __init__(self, dict_tweet):
        self.favourite_count = dict_tweet['favorite_count']
        self.retweet_count = dict_tweet['retweet_count']
        self.hashtags = dict_tweet['entities']['hashtags']
        self.user_mentions = dict_tweet['entities']['user_mentions']
        self.urls = dict_tweet['entities']['urls']
        self.text = dict_tweet['full_text']

class Twitter:

    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth)
    
    def fetchTweets(self, handle, limit=5):
        tweets = []
        for status in tweepy.Cursor(self.api.user_timeline, id=handle, tweet_mode='extended').items(limit):
            tweet = Tweet(status._json)
            tweets.append(tweet)
        return tweets

consumer_key = "rLSO59KOXRjjWisGpsuqqaEdJ"
consumer_secret = "rprRhqIsgxY49qFZlpRZmZs7pMXcFoJrGmryoRUUmXRQm6E9v0"

access_token = "420400261-Qknhgi9XaPv1ZklKdV68Ef4ZzbmjyPTFKynzW2WR"
access_token_secret = "B077y0aYdHAntBR0GKB84xHqkofTW2a99qb42iptprDwE"

twitterEg = Twitter(consumer_key, consumer_secret, access_token, access_token_secret)

tweets = twitterEg.fetchTweets('realDonaldTrump')
print(tweets[0].__dict__)

