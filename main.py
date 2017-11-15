import facebook

from classes.Post import Post
from fbDatafetch import DataFetch_fb
from basicRanking import BasicRanking
from text_cleansing_step1 import text_retrieve

access_token = "EAACEdEose0cBAJ1UzpICRKoKk1TREE5bqjFHWZB4X6C8zLBZBvf58skaasUHm4EjZBuPVZBbjPfjtd1TH15o3FZAWZBVaKDnL0R4UUJehv3vWZC9LbmyVCtDWxxxnfhyta9BhZBZByZAsB0AVvPyMunedYpTV17HrAoC03wcPJXiFdnnWeoZAobZAA2vIaQmzken6oUZD"

# Profile usernames
usernames = ['RUR.AreYouReducingReusingRecycling', 'EARTHOHOLICS']

fetchDb = DataFetch_fb(access_token, usernames)

# Fetch all posts
result = fetchDb.fetchPosts()

# Instantiate noise removal object
textAndNoise = text_retrieve(result)

# Remove noise from result
textAndNoise.noise_removal()

# Fetch callouts and hastags from result
callouts, hash_tag = textAndNoise.cal_hashTag_callout()

# Instantiate BasicRanking object
ranking = BasicRanking(result, usernames)

# Rank result based on likes
print(ranking.getRank())
