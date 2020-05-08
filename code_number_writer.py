import tweepy
import os
import time
import emoji
import json
from dotenv import load_dotenv
  


def get_mentions(id):
    if id != None:
        mentions = api.mentions_timeline(since_id=id)
    else:
        mentions = api.mentions_timeline()
    return mentions


def filter_flags(ascii_codes):
    flags = []
    for cod in ascii_codes:
            if cod >= 127462 and cod <= 127487:
                flags.append(str(cod))
    return flags


def unite_flags(separated_flags):
    united_flags = []
    i = 0
    while i < len(separated_flags)-1:
        united = separated_flags[i] + separated_flags[i+1]
        united_flags.append(united)
        i = i + 2
    return united_flags


def get_flags_from_mention(mention_text):
    decode = mention_text
    allchars = [str for str in decode]
    emojis = [c for c in allchars if c in emoji.UNICODE_EMOJI]
    converted_to_ascii = [ord(c) for c in emojis]
    pure_divided_flags = filter_flags(converted_to_ascii)
    flags = unite_flags(pure_divided_flags)
    return flags


with open('languages.json') as json_file: 
    languages = json.load(json_file) 
json_file.close()

load_dotenv()

consumer_key = os.getenv("key")
consumer_secret = os.getenv("secret")
access_token = os.getenv("token")
access_token_secret = os.getenv("token_secret")

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


mentions_list = get_mentions(None)

for status in mentions_list:
    
    flags_list = get_flags_from_mention(status.text)
    
    for number in flags_list:
        languages.update({number: [""]})

print(languages)
print(len(languages))
with open('languages.json', 'w') as json_file: 
    json.dump(languages, json_file, indent=4)
