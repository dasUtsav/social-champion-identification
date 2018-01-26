import tweepy, json

class Tweet:
    def __init__(self, dict_tweet):
        self.favourite_count = dict_tweet['favorite_count']
        self.retweet_count = dict_tweet['retweet_count']
        self.hashtags = dict_tweet['entities']['hashtags']
        self.user_mentions = dict_tweet['entities']['user_mentions']
        self.urls = dict_tweet['entities']['urls']
        self.message = dict_tweet['full_text']
        self.screen_name = dict_tweet['user']['screen_name']
        self.follower_count = dict_tweet['user']['followers_count']
        self.isRetweet = 1 if 'retweeted_status' in dict_tweet else 0

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


