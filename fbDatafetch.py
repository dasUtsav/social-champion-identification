import facebook

from classes.Post import Post


class DataFetch_fb:
    
    def __init__(self, access_token, usernames):
        self.graph = facebook.GraphAPI(access_token=access_token, version="2.1")
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


access_token = "EAABZBfg9w4HgBAC58ta4cbc0ZBZA5HNmF6RPmu4IOjdnlnXz376iWUZCnIhXK9k5qmYOwjH5EeaTACmnRvGEGt97eKOVlZAkcFAIk4NIy729sagoVpt1Gr8qpkUXplEyj7ROt1wWTHrdNvRRUNg2Cyr5poFwZB7QjZAK1L8I2ACqefrLw4mHTbzZBJVHzCG9ZAqZBviQL8AjVanQZDZD"

# Profile usernames
usernames = ['RUR.AreYouReducingReusingRecycling', 'EARTHOHOLICS']

fetchDb = DataFetch_fb(access_token, usernames)

print(fetchDb.fetchPosts())
        

