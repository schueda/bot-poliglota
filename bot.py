import tweepy
import os
import time
import emoji

from dotenv import load_dotenv
load_dotenv()

consumer_key = os.getenv("key")
consumer_secret = os.getenv("secret")
access_token = os.getenv("token")
access_token_secret = os.getenv("token_secret")

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

last_id = None

while True:

    if last_id != None:
        print(f"\n----- Puxando mentions desde {last_id} -----")
        mentions = api.mentions_timeline(since_id=last_id)
    else:
        print("\n\n----- Puxando todas as mentions -----")
        mentions = api.mentions_timeline()
   
    if len(mentions) != 0:
        last_id = mentions[0].id

    print("\n----- IMPRIMINDO MENTIONS -----")
    for status in mentions:
        print(status.id, status.text)
        #decode  = status.text.decode('utf-8')
        decode  = status.text
        allchars = [str for str in decode]
        emojis = [c for c in allchars if c in emoji.UNICODE_EMOJI]
        print(emojis)
    time.sleep(10)

