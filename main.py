# to run file: pipenv run python main.py
import facebook

from classes.Post import Post
from fbDatafetch import DataFetch_fb
from basicRanking import BasicRanking
from text_cleansing_step1 import text_retrieve

access_token = "EAACEdEose0cBAKAFsX2NbZBIVnxOdq4zZAuX8uhtRqNpvGqD4LOQrTAFZBVvxaXU3drtxk57Ynj7EzvJqOZBgmsd0PvxCNpxMcUGLye4JzpsDjOa97B1Yiytz0AQ5OjDdUhOoKrfNZBWg2OOM19lmSZBuOWQxONibP9YZBpdC4oMKPUZCyqAqwNH3x2Giy1ZCowZC4xGabxto4EgZDZD"

# Profile usernames
usernames = ['RUR.AreYouReducingReusingRecycling', 'EARTHOHOLICS']

fetchDb = DataFetch_fb(access_token, usernames)

# Fetch all posts
result = fetchDb.fetchPosts()

# Instantiate noise removal object
textAndNoise = text_retrieve(result)

# Remove noise from result
noiseless = textAndNoise.noise_removal()

# Fetch callouts and hastags from result
callouts, hash_tag = textAndNoise.cal_hashTag_callout()
print(callouts)

# # Lemmatize the messages
lemmatized = textAndNoise.lemmatize()
print(lemmatized[:20]) # to see the lemmatized text

# Instantiate BasicRanking object
# ranking = BasicRanking(result, usernames)

# # Rank result based on likes
# print(ranking.getRank())
