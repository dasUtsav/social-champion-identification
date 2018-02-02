import os
from classes.TwitterGraph import TwitterGraph
from classes.TopicInfluence import TopicInfluence
from Instances import twitterInstance


twitterGraph = TwitterGraph("twitterGraph.pickle")

# twitterGraph.add_candidate('nasw', 10, 5)

max_followers = 10
max_follower_friends = 5

if os.path.isfile("twitterGraph.pickle"):
    twitterGraph.load_pickle()
else:
    twitterGraph.add_candidate('nasw', max_followers, max_follower_friends)

## Run this if you wanna reset the db
# twitterGraph.resetRefetch()

## Run in order to reset the tweet_doc prop
# twitterGraph.reset_prop('tweet_doc')

topicInfluence = TopicInfluence(twitterGraph)

res = twitterInstance.api.get_user('nasw')

print(topicInfluence.compute_rank(10, [res.id]))
