import facebook

from classes.Post import Post

from classes.DataFetch_fb import DataFetch_fb

access_token = "EAACEdEose0cBAPZCEA4jZBgxMnoqoMzEqT8714tC2VQVBwF9l4TLfJCnFSHwwjESVwoEhYqppaSYZCJHs2VwQyZAC8OtE23f7dKlLQZCpK0hpV27uRjRytCwF7oZCge4qVZBX9YEM6YattTzLeAGNrllil8iZAKmxCo32vZBqIVwvLZC3GRCUF4YrI9Ef5PFT785oZD"

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
    for data in page['data']:
        likes.append(data.likes)
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
