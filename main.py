# to run file: pipenv run python main.py
import facebook

from classes.Post import Post
from fbDatafetch import DataFetch_fb
from basicRanking import BasicRanking
from text_cleansing_step1 import text_retrieve

access_token = "EAACEdEose0cBANzFckmwv4TAkjQFU1mlJCRACyX1ZAa3Fvs2a2ebyhqdZBbAXpNNf0J3OjYTb9XikVMAEschNLiJ9nBnlxqULWsqnyZA2uTcXdX55o4h9wkaYwhC2Gm1GjvmkKT5f7uFXQWF4hfQ5utZBcLLf3kVWNYZCyaTY1n6ZBzoHDInD9"

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

# Lemmatize the messages
lemmatized = textAndNoise.lemmatize()
# print(lemmatized[:20]) # to see the lemmatized text

# Instantiate BasicRanking object
ranking = BasicRanking(result, usernames)

# Rank result based on likes
print(ranking.getRank())
