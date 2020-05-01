import tweepy
import os
import time
import emoji
import json
from dotenv import load_dotenv

with open('languages.json') as json_file: 
    languages = json.load(json_file)  
  
    print("estados unidos:", languages["127482127480"]) 
    print("suiça:", languages["127464127469"]) 


def emojis_flags_separation(ascii_codes):
    flags = []
    for cod in ascii_codes:
            if cod >= 127462 and cod <= 127487:
                flags.append(str(cod))
    return flags

def flags_junction(separated_flags):
    united_flags = []
    i = 0
    while i < len(separated_flags)-1:
        united = separated_flags[i] + separated_flags[i+1]
        united_flags.append(united)
        i = i + 2
    return united_flags

# def language_flag_relating(final_flags):
#     language_list = []
#     for united_cod in final_flags:
#         if united_cod == "" or united_cod == "":
#             language_list.append("English")
#         elif united_cod == "" or united_cod == "":
#             language_list.append("French")
#         elif united_cod == "" or united_cod == "":
#             language_list.append("Japanese")
#         elif united_cod == "" or united_cod == "":
#             language_list.append("Italian")
#         elif united_cod == "" or united_cod == "":
#             language_list.append("German")
#         elif united_cod == "" or united_cod == "":
#             language_list.append("Chinese")
#         elif united_cod == "" or united_cod == "":
#             language_list.append("Korean")
#         elif united_cod == "" or united_cod == "":
#             language_list.append("Spanish")
#         elif united_cod == "" or united_cod == "":
#             language_list.append("Norwegian")
#         elif united_cod == "" or united_cod == "":
#             language_list.append("Russian")
#         elif united_cod == "" or united_cod == "":
#             language_list.append("Danish")
#         elif united_cod == "" or united_cod == "":
#             language_list.append("Finnish")
#         elif united_cod == "" or united_cod == "":
#             language_list.append("Portuguese")
#         else:
#             language_list.append("Undefined")
#     return language_list()


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
        #print(status.id, status.text)
        
        decode  = status.text #decode  = status.text.decode('utf-8')
        allchars = [str for str in decode]
        emojis = [c for c in allchars if c in emoji.UNICODE_EMOJI]
        print("símbolo         ", emojis)
        
        converted_to_ascii = [ord(c) for c in emojis]
        print("na ascii        ", converted_to_ascii)
        
        pure_divided_flags = emojis_flags_separation(converted_to_ascii)
        print("apenas bandeiras", pure_divided_flags)

        flags = flags_junction(pure_divided_flags)
        print("bandeiras juntas", flags, "\n")

    time.sleep(10)

