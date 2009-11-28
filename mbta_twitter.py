import twitter
import sqlalchemy


class ConnectUser(XXX):
    api = twitter.Api(username='twitter user', password='twitter pass')

    def ChooseLine(route):
        #Pass this route, return twitter account info

class MakeTweet(status):
    status = api.PostUpdate('content')


class Friends(XXX):
    # To fetch your friends (after being authenticated):
    users = api.GetFriends()
    print [u.name for u in users]
