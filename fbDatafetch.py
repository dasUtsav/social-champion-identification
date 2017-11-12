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


access_token = "EAACEdEose0cBAPNRLjZBXVdIKianlDHXiZCMqW2pZBXoqs78azfF4SG1WGkP9xb0gzvV4r6vCMFHjZBMKXo8T5DHjV9sAiuadZAB7VrVeDyXAweiquJHVR1Wz5Xi81PZALLVEt8zMd4PkBv0EVg9hAc91Y4gmiaXVSK63oREHf7yCa7EiAHxTeuXXhVH7NLTdUKRNKcRCZBZCgZDZD"

# Profile usernames
usernames = ['RUR.AreYouReducingReusingRecycling', 'EARTHOHOLICS']

fetchDb = DataFetch_fb(access_token, usernames)

result = fetchDb.fetchPosts()

for page in result:
    for data in page['data']:
        if(data.message):
            page['data'].remove(data)
    print("After", len(page['data']))
    

        

