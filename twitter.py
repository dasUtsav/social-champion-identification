import tweepy, json

class Tweet:
    def __init__(self, dict_tweet):
        self.favorite_count = dict_tweet['favorite_count']
        self.user_id = str(dict_tweet['user']['id'])
        self.retweet_count = dict_tweet['retweet_count']
        self.hashtags = dict_tweet['entities']['hashtags']
        self.user_mentions = dict_tweet['entities']['user_mentions']
        self.urls = dict_tweet['entities']['urls']
        self.message = dict_tweet['full_text']
        self.created_at = dict_tweet['created_at']
        self.screen_name = dict_tweet['user']['screen_name']
        self.follower_count = dict_tweet['user']['followers_count']
        self.isRetweet = 1 if 'retweeted_status' in dict_tweet else 0

class User:
    def __init__(self, dict_tweet):
        self.profile_image_url = dict_tweet["profile_image_url"]
        self.statuses_count = dict_tweet["statuses_count"]
        self.screen_name = dict_tweet["screen_name"]
        self.followers_count = dict_tweet["followers_count"]
        self.id = str(dict_tweet["id"])

class Twitter:

    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    
    def fetchTweets(self, handle, limit=5):
        tweets = []
        try:
            for status in tweepy.Cursor(self.api.user_timeline, id=handle, tweet_mode='extended').items(limit):
                tweet = Tweet(status._json)
                if status._json["lang"] == "en":
                    tweets.append(tweet)
                    
        except:
            tweets = []
        return tweets

    def fetchUser(self, screen_name):
        user = self.api.get_user(screen_name)
        user = User(user._json)
        return user

    def fetchFollowers(self, handle, limit=5):
        users = []
        for user in tweepy.Cursor(self.api.followers, id=handle).items(limit):
            user = User(user._json)
            users.append(user)
        return users
    
    def fetchFriends(self, handle, limit=5):
        users = []
        for user in tweepy.Cursor(self.api.friends, id=handle).items(limit):
            user = User(user._json)
            users.append(user)
        return users


