from classes.TwitterGraph import TwitterGraph

twitterGraph = TwitterGraph("twitterGraph.pickle")
twitterGraph.load_pickle()

print(twitterGraph.G.node['113352671'])