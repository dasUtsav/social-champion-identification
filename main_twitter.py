from classes.TwitterGraph import TwitterGraph
from classes.TopicInfluence import TopicInfluence
from Instances import twitterInstance


twitterGraph = TwitterGraph("twitterGraph.pickle")

# twitterGraph.add_candidate('nasw', 10, 5)

twitterGraph.load_pickle()


# for node in twitterGraph.G.nodes():
#     # print(twitterGraph.G.node[node])
#     twitterGraph.G.node[node]['isRetrieve'] = False

topicInfluence = TopicInfluence(twitterGraph)

res = twitterInstance.api.get_user('nasw')

print(topicInfluence.compute_rank(10, [res.id]))
