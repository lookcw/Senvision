import tweepy
from tweepy import OAuthHandler

consumer_key = 'qHCU3LD8JFPX5BT8aJmoiPl2G'
consumer_secret = 'HSHwRTWeig8ZqmzmcbH6aQL1EngWryLM2RImrI0apWOSEqsuVu'
access_token = '2914951708-hL4NqtOnt1H8i9gq3lxA4HA5wiHFqUPYw8ytALa'
access_secret = 'VOEygo7KbeVrUK13ginfoPSDOEbrEOuZr90kfqs1u6PB4'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

for status in tweepy.Cursor(api.home_timeline).items(10):
	print(status.text)
