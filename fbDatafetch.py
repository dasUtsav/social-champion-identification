import facebook

from classes.Post import Post


class DataFetch_fb:
    
    def __init__(self, access_token, usernames):
        self.graph = facebook.GraphAPI(access_token=access_token, version="2.6")
        self.usernames = usernames
    
    def findInListDict(self, list, dictKey, value):
        for item in list:
            if item[dictKey] == value:
                return item
    
    def fetchPosts(self):
        pageDict = []
        for username in self.usernames: 
            pageDict.append({'name': username, 'data': []}) 
            pageDict = sorted(pageDict, key=lambda page: page['name'].lower())

        getPageLikes = self.graph.get_objects(ids=usernames, fields='feed{likes.summary(true), message}, fan_count')

        for username in getPageLikes:
            item = self.findInListDict(pageDict, 'name', username)
            item['page_likes'] = getPageLikes[username]['fan_count']
            for data in getPageLikes[username]['feed']['data']:
                message = ""
                if('message' in data):
                    message = data['message']
                item['data'].append(Post(data['id'], message, data['likes']['summary']['total_count']))

        return pageDict


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



# for page in result:
#     print(len(page['data']))
#     for data in page['data']:
#         if(data.message):
#             page['data'].remove(data)
#     print("After", len(page['data']))