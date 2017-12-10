# to run file: pipenv run python main.py
import facebook

from classes.Post import Post
from fbDatafetch import DataFetch_fb
from basicRanking import BasicRanking
from text_cleansing_step1 import text_retrieve

access_token = "EAACEdEose0cBACX4uoKIC8hF9nwlSAz7oMOMUZCAvWswNirV9zqmePILA9uTSObRZBwgJg4CrhXszNhGmo3uOpP4JjjjdqpmZCZCZAATkok2mMK4beP41tpvVjl2wMNqinFg9zySdQZALZA5XFKJqdQGxwBkclDFp7Ig9pIPyxlWsg09cJgbHWpi5XoMiuphHszPrggjEwfHQZDZD"

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