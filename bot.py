import tweepy
import os
import time
import emoji
import json
from googletrans import Translator

from dotenv import load_dotenv

            

# Função que puxa as ultimas 20 mentions
def get_mentions(id):
    
    if id != None:
        print(f"\n----- Puxando mentions desde {id} -----")
        mentions = api.mentions_timeline(since_id=id)
    else:
        print("\n\n----- Puxando todas as mentions -----")
        mentions = api.mentions_timeline()
    
    return mentions  


#Função que filtra apenas as mentions que não começam com a tag
def filter_mentions(not_filtered_mentions):
    
    notstarting = []
    for status in not_filtered_mentions:
        if  not status.text.lower().startswith("@bot_polilingue"):
            notstarting.append(status)
    
    return notstarting


#Função que filtra os emojis do texto e transforma-os em código da ascii
def filter_emojis(text):
    
    decode = text
    allchars = [str for str in decode]
    emojis = [c for c in allchars if c in emoji.UNICODE_EMOJI]
    converted_to_ascii = [ord(c) for c in emojis]
    
    return converted_to_ascii


# Função que separa as bandeiras dos demais emojis
def filter_flags(ascii_codes):
    flags = []
    
    for cod in ascii_codes:
            if cod >= 127462 and cod <= 127487:
                flags.append(str(cod))
    
    return flags


# Função que junta os dois códigos das bandeiras
def unite_flags(separated_flags):
    united_flags = []
    i = 0
    
    while i < len(separated_flags)-1:
        united = separated_flags[i] + separated_flags[i+1]
        united_flags.append(united)
        i = i + 2
    
    return united_flags


#Função que pega a mention e retorna apenas os códigos das bandeiras dectadas
def get_flags_from_mention(mention_text):

    emojis_in_ascii = filter_emojis(mention_text)
    pure_divided_flags = filter_flags(emojis_in_ascii)
    flags = unite_flags(pure_divided_flags)
    
    return flags


#Chamada do documento json que relaciona cada código com cada língua
with open('languages.json') as json_file: 
    languages = json.load(json_file)  

#Função que relaciona a flag com a lingua
def get_language(country):
    return languages[country]

translator = Translator()



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
    
    filtered_mentions = filter_mentions(mentions_list)

    for status in filtered_mentions:
        
        original_status = api.get_status(status.in_reply_to_status_id)
        flags = get_flags_from_mention(status.text)
        
        buffer = []
        for flag in flags:
            language = get_language(flag)
            
            translation = translator.translate(original_status.text, dest=language)

        


        
        
        # Loop de cada bandeira
            # Pega idioma daquele país
            # Loop de cada idioma
                # Verifica se ja existe no buffer
                    # Caso não, traduz pro idioma

                # Guarda em um buffer (caso a pessoa coloque duas bandeiras de países que falam o mesmo idioma)

                # Tweeta (cuidado com tweets muito longos)
                
        # Limpa buffer de idiomas


    time.sleep(10)

