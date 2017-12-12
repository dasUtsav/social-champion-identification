# to run file: pipenv run python main.py
import facebook

from classes.Post import Post
from fbDatafetch import DataFetch_fb
from basicRanking import BasicRanking
from text_cleansing_step1 import text_retrieve


access_token = "EAACEdEose0cBANyudWHRo9CDeLMsW4KnFWAcVsoe35G16DGOa7asUoghIUISCSj5jDLfZAFhXYmHXpAUVpLc21SOptl5ZB6S6QDRAnsNZACfRA6YSbkSfF1YLlEUZA9AJsm0gluAfKbaBkI9d8HB1M1OhspAlfzAGZAKwG7BKN7fxQOjmA1yDzMXwpG3eFseSC5Ix1Ec8KQZDZD"

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
print("Hashtags")
print(hash_tag)

# # Lemmatize the messages
# lemmatized = textAndNoise.lemmatize()
# print(lemmatized[:20]) # to see the lemmatized text

# Instantiate BasicRanking object
# ranking = BasicRanking(result, usernames)

# # Rank result based on likes
# print(ranking.getRank())
