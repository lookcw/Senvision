import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

class MyListener(StreamListener):
	def on_data(self, data):
		try:
			with open('python.json', 'a') as f:
				f.write(data)
				return True
		except BaseException as e:
			print("Error on_data: %s" % str(e))
		return True
	def on_error(self, status):
		print(status)
		return True

consumer_key = 'qHCU3LD8JFPX5BT8aJmoiPl2G'
consumer_secret = 'HSHwRTWeig8ZqmzmcbH6aQL1EngWryLM2RImrI0apWOSEqsuVu'
access_token = '2914951708-hL4NqtOnt1H8i9gq3lxA4HA5wiHFqUPYw8ytALa'
access_secret = 'VOEygo7KbeVrUK13ginfoPSDOEbrEOuZr90kfqs1u6PB4'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

twitter_stream = Stream(auth, MyListener())
twitter_stream.filter(track=['$INTC'])
