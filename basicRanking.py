class BasicRanking:

    def __init__(self, result, usernames):
        self.result = result
        self.usernames = usernames
    
    def getRank(self):
        totalLikes = count = avg = 0
        rankPageLikes = []
        rankPostLikes = []
        rankList = []
        for page in self.result:
            #totalLikes = page['page_likes']
            likes = [data.likes for data in page['data']]
            totalLikes = sum(likes)
            avg = totalLikes/len(page['data'])
            rankPageLikes.append({'name': page['name'], 'likes': page['page_likes']})
            rankPostLikes.append({'name': page['name'], 'likes': avg})
            # print("Username: ", page['name'], "Score: ", int(score))
        
        rankPageLikes = sorted(rankPageLikes, key=lambda page : page['likes'], reverse=True)
        rankPostLikes = sorted(rankPostLikes, key=lambda page : page['likes'], reverse=True)
        arrayLen = len(rankPageLikes)

        for i in range(0, arrayLen):
            rankPageLikes[i]['rank'] = rankPostLikes[i]['rank'] = arrayLen - i - 1
        
        for username in self.usernames:
            page = getFromDict(rankPageLikes, 'name', username)
            post = getFromDict(rankPostLikes, 'name', username)
            finalScore = (0.6 * post['rank'] + 0.4 * page['rank'])/arrayLen * 100
            rankList.append({"name":username, 'finalScore': finalScore})

        return rankList


def getFromDict(list, key, value):
    for item in list:
        if(item[key] == value):
            return item
    return {}


