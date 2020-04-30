import tweepy
import os
import time
import emoji

from dotenv import load_dotenv
load_dotenv()


def language_flag(flag_code):
    if flag_code == "a":
        return "english"
    elif flag_code == "b":
        return "german"
    elif flag_code == "c":
        return "italian"
    else:
        return 0


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
        #print(status.id, status.text)
        #decode  = status.text.decode('utf-8')
        decode  = status.text
        allchars = [str for str in decode]
        emojis = [c for c in allchars if c in emoji.UNICODE_EMOJI]
        converted_to_ascii = [ord(c) for c in emojis]
        print("símbolo", emojis)
        print("na ascii", converted_to_ascii)
        bandeiras=[]
        for cod in converted_to_ascii:
            if cod >= 127462 and cod <= 127487:
                bandeiras.append(str(cod))
        print("caracteres de bandeira", bandeiras, "\n")
    
    time.sleep(10)

