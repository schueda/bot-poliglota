import tweepy
import os
import time
import emoji
import json
from dotenv import load_dotenv
  


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


with open('languages.json') as json_file: 
    languages = json.load(json_file)  

def language_flag_relate(final_flags):
    language_list = []
    for united_cod in final_flags:
        language_list.append(str(languages[united_cod]))
    language_list = list(dict.fromkeys(language_list))
    return language_list
    

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

    ## Transforme em uma função que retorna as mentions
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

        # Adicione uma verificação pra ver se a mention começa com o @ do bot
        
        ## Transforme em una função que faça esse processo em outro lugar
        # Daqui
        decode  = status.text #decode  = status.text.decode('utf-8')
        allchars = [str for str in decode]
        emojis = [c for c in allchars if c in emoji.UNICODE_EMOJI]
        print("símbolo         ", emojis)
        
        converted_to_ascii = [ord(c) for c in emojis]
        print("na ascii        ", converted_to_ascii)
        
        pure_divided_flags = filter_flags(converted_to_ascii)
        print("apenas bandeiras", pure_divided_flags)

        flags = unite_flags(pure_divided_flags)
        # Até aqui

        print("bandeiras juntas", flags)

        languages_required = language_flag_relate(flags)
        print("lista de linguas", languages_required, "\n")

        # Loop de cada bandeira
            # Pega idioma daquele país
            # Loop de cada idioma
                # Verifica se ja existe no buffer
                    # Caso não, traduz pro idioma

                # Guarda em um buffer (caso a pessoa coloque duas bandeiras de países que falam o mesmo idioma)

                # Tweeta (cuidado com tweets muito longos)
                
        # Limpa buffer de idiomas


    time.sleep(10)

