import facebook

from classes.Post import Post
from fbDatafetch import DataFetch_fb
from basicRanking import BasicRanking
from text_cleansing_step1 import text_retrieve

access_token = "EAACEdEose0cBALnRPZBeUZBEgpxA22X2pxnbV5dXJ17ZBdSRsA8PgCNP33FIr60yNHaWoeGQrNBJg8lBIZCslstMS6EVm1CqtbMcG9huUOrFdkYUoidyEZCHRtAJK8d5vyL4rARg4cX5zPdZAseZBFa9fdmIslB9ZBDdBABzVQlaaygOMh8jWzWRMsJnvMjB280ZD"

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
print(hash_tag)

# Instantiate BasicRanking object
ranking = BasicRanking(result, usernames)

# Rank result based on likes
print(ranking.getRank())
