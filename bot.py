import tweepy
import os
import time
import emoji
import json
from dotenv import load_dotenv



def get_mentions(id):
    
    if id != None:
        print(f"\n----- Puxando mentions desde {id} -----")
        mentions = api.mentions_timeline(since_id=id)
    else:
        print("\n\n----- Puxando todas as mentions -----")
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

#não sei bem o que fazer aqui ainda


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

    mentions_list = get_mentions(last_id)
   
    if len(mentions_list) != 0:
        last_id = mentions_list[0].id

    print("\n----- IMPRIMINDO MENTIONS -----\n")
    
    print("todas as mentions:")
    
    for status in mentions_list:

        print(status.text)

    print("\n-------------------------------------------------------------------------------\n")
    print("ESSAS NÃO PODEM:")
    for status in mentions_list:

        if status.text.startswith('@_schueda_') or status.text.startswith(' @_Schueda_'):
            print(status.text)
            mentions_list.remove(status)
    print("\n-------------------------------------------------------------------------------\n")
    
    print("lista filtrada:")
    for status in mentions_list:

        print(status.text)

    

        # Adicione uma verificação pra ver se a mention começa com o @ do bot
        
        # Loop de cada bandeira
            # Pega idioma daquele país
            # Loop de cada idioma
                # Verifica se ja existe no buffer
                    # Caso não, traduz pro idioma

                # Guarda em um buffer (caso a pessoa coloque duas bandeiras de países que falam o mesmo idioma)

                # Tweeta (cuidado com tweets muito longos)
                
        # Limpa buffer de idiomas


    time.sleep(10)

