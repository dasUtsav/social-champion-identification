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


access_token = "EAACEdEose0cBAPqg29CGcba5ajz6IRbG1ZBhs477dhefU2KwDoRx3w22GgrMZBuZCIi067lj1NwXaSahFpzJ8DnLDZANFPW8cLvXfnlTZC8ZB4GphhZCTpQZC2m93Rv2Y4Xsb1CfW0G7MhdCDu8HPJsJpjmDoSqNW4TXGuqZBf1F7s0pQnWIxMSgnNF9qUz0ZBtBQlrLohqfMvzwZDZD"

# Profile usernames
usernames = ['RUR.AreYouReducingReusingRecycling', 'EARTHOHOLICS']

fetchDb = DataFetch_fb(access_token, usernames)

result = fetchDb.fetchPosts()

totalLikes = count = avg = 0

for page in result:
    totalLikes = page['page_likes']
    for data in page['data']:
        count += 1
    avg = totalLikes/count
    rank = (((avg - 0) * 10) / 1000) + 0
    print("Username: ", page['name'], "Rank: ", int(rank))

# for page in result:
#     print(len(page['data']))
#     for data in page['data']:
#         if(data.message):
#             page['data'].remove(data)
#     print("After", len(page['data']))