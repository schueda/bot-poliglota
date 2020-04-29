import tweepy
import os

from dotenv import load_dotenv
load_dotenv()

consumer_key = os.getenv("key")
consumer_secret = os.getenv("secret")
access_token = os.getenv("token")
access_token_secret = os.getenv("token_secret")

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

public_tweets = api.home_timeline()
for tweet in public_tweets:
    print(tweet.text)