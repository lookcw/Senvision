from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time
import json



#        replace mysql.server with "localhost" if you are running via your own server!
#                        server       MySQL username	MySQL pass  Database name.


#consumer key, consumer secret, access token, access secret.
ckey="GkNo1eVzDrIvx4WX0UF2IQvUy"
csecret="u44NuHRf7zWJS3oXNCMruJnDyUqugAKTYReSAV5cykHkQ3vxp5"
atoken="763207677463920640-cTCEshVK13VFegFjrUry1p5tyUa98Ux"
asecret="xx5fQbbIjv6zzGv7FrzUXdqxmpOe0tyO8s48zNApMG84y"

class listener(StreamListener):

    def on_data(self, data):
        all_data = json.loads(data)
        
        tweet = all_data["text"]
        
        username = all_data["user"]["screen_name"]

        print((username,tweet))
        
        return True

    def on_error(self, status):
        print status

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitterStream = Stream(auth, listener())
twitterStream.filter(track=["car"])
