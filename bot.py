import tweepy
import os
import time
import emoji
import json

from googletrans import Translator

from dotenv import load_dotenv

#Chamada do documento json que relaciona cada código com cada língua
with open('languages.json') as json_file: 
    languages = json.load(json_file)  
print(len(languages))

# Função que puxa as ultimas 20 mentions
def get_mentions(id):
    
    if id != None:
        print(f"\n----- Puxando mentions desde {id} -----")
        mentions = api.mentions_timeline(since_id=id)
    else:
        print("\n\n----- Puxando todas as mentions -----")
        mentions = api.mentions_timeline()
    
    return mentions  


#Função que filtra apenas as mentions uteis
def filter_mentions(not_filtered_mentions):
    
    filtered = []
    for status in not_filtered_mentions:
        mention_user = api.get_user(status.user.id)
        if  not mention_user.screen_name == "bot_polilingue" and "/translate" in status.text:
            filtered.append(status)

    return filtered


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


#Função que relaciona a flag com a lingua
def get_language(country):
    return languages[country]

translator = Translator()


# Função que transforma o codigo das bandeiras de volta em emojis
def emojize_flag_code(flag_code):
    
    first_letter_code = flag_code[:int(len(flag_code)/2)]
    second_letter_code = flag_code[int(len(flag_code)/2):]
    
    emojized_first_letter = chr(int(first_letter_code))
    emojized_second_letter = chr(int(second_letter_code))
    
    return emojized_first_letter, emojized_second_letter


# Função que remove os emojis do texto
def remove_emoji(another_text):
    return emoji.get_emoji_regexp().sub(r'', another_text)

# ========================================================================================================


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

    mentions_list = filter_mentions(mentions_list)

    for status in mentions_list:

        original_status = api.get_status(status.in_reply_to_status_id)
        translation_needed = remove_emoji(original_status.text)
        print("o tweet a ser traduzido:", translation_needed)

        flags = get_flags_from_mention(status.text)

        buffer = dict()
        print(buffer)
        
        for flag in flags:

            language = get_language(flag)
            base_language = language[0]

            if base_language in buffer:
                translation = buffer[base_language]
            else:
                translation = translator.translate(translation_needed, dest=base_language)
                buffer[base_language] = translation.text
            
            first_letter, second_letter = emojize_flag_code(flag)

            # if len(translation) > 273:
            #     #tweeta os primeiros 273 caracteres assim (xxxx "tex+)
            #     #tweeta o resto assim (to")
            #     a = 0
            # else:
            final_text = first_letter + second_letter + ' "' + translation.text + '"'
            api.update_status(final_text, in_reply_to_status_id=status.id, auto_populate_reply_metadata=True)

            # if len(language) > 1:

            #     for langs in language[1:]:
                    
            #         if langs in buffer:
            #             translation = buffer[langs]
            #         else:
            #             translation = translator.translate(translation_needed, dest=langs)
            #             buffer[langs] = translation.text
                    
            #         if len(translation.text) > 273:
            #             #tweeta os primeiros 273 caracteres assim (xxxx "tex+)
            #             #tweeta o resto assim (to")
            #             a = 0
            #         else:
            #             #tweeta em cadeia com o tweet anterior com o emoji da bandeirinha e " "
            #             a = 0

    time.sleep(15)

