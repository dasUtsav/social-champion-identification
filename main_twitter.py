from classes.TwitterGraph import TwitterGraph


twitterGraph = TwitterGraph("twitterGraph.pickle")

twitterGraph.load_pickle()

twitterGraph.fetch_tweets_model("nasw", 5)

print(twitterGraph.G.nodes())

