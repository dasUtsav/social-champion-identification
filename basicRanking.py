import facebook

from classes.Post import Post

from fbDatafetch import DataFetch_fb

access_token = "EAACEdEose0cBAJ1UzpICRKoKk1TREE5bqjFHWZB4X6C8zLBZBvf58skaasUHm4EjZBuPVZBbjPfjtd1TH15o3FZAWZBVaKDnL0R4UUJehv3vWZC9LbmyVCtDWxxxnfhyta9BhZBZByZAsB0AVvPyMunedYpTV17HrAoC03wcPJXiFdnnWeoZAobZAA2vIaQmzken6oUZD"

# Profile usernames
usernames = ['RUR.AreYouReducingReusingRecycling', 'EARTHOHOLICS']

fetchDb = DataFetch_fb(access_token, usernames)

result = fetchDb.fetchPosts()

totalLikes = count = avg = 0
likes = []

rankPageLikes = []
rankPostLikes = []

for page in result:
    #totalLikes = page['page_likes']
    likes = [data.likes for data in page['data']]
    totalLikes = sum(likes)
    avg = totalLikes/len(page['data'])
    rankPageLikes.append({'name': page['name'], 'likes': page['page_likes']})
    rankPostLikes.append({'name': page['name'], 'likes': avg})
    # print("Username: ", page['name'], "Score: ", int(score))

rankPageLikes = sorted(rankPageLikes, key=lambda page : page['likes'], reverse=True)
rankPostLikes = sorted(rankPostLikes, key=lambda page : page['likes'], reverse=True)
#print(rankPostLikes)

rankList = []
arrayLen = len(rankPageLikes)

for i in range(0, arrayLen):
    rankPageLikes[i]['rank'] = rankPostLikes[i]['rank'] = arrayLen - i - 1

def getFromDict(list, key, value):
    for item in list:
        if(item[key] == value):
            return item
    return {}

for username in usernames:
    page = getFromDict(rankPageLikes, 'name', username)
    post = getFromDict(rankPostLikes, 'name', username)
    finalScore = (0.6 * post['rank'] + 0.4 * page['rank'])/arrayLen * 100
    rankList.append({"name":username, 'finalScore': finalScore})

print(rankList)
