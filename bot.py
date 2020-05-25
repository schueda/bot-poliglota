import tweepy
import os
import time
import emoji
import json

from googletrans import Translator

from os import environ

# ========================================================================================================

consumer_key = environ["key"]
consumer_secret = environ["secret"]
access_token = environ["token"]
access_token_secret = environ["token_secret"]
last_id = environ["last_id"]
print(l"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA", last_id)

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# ========================================================================================================


#Chamada do documento json que relaciona cada código com cada língua
with open('languages.json') as json_file: 
    languages_dict = json.load(json_file)  


# Função que puxa as ultimas mentions e evita erros de conexão
def get_mentions(id):
    global api

    try:
        bool_error = False
        if id != None:
            print(f"\n----- Puxando mentions desde {id} -----")
            
            try:
                mentions = api.mentions_timeline(since_id=id)

            except TimeoutError:
                print("-----------------------------ERA PRA TER TRAVADO-----------------------------")
                api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
                mentions = api.mentions_timeline(since_id=id)
                        
        else:
            print("\n\n----- Puxando todas as mentions -----")

            try:
                mentions = api.mentions_timeline()

            except TimeoutError:
                print("-----------------------------ERA PRA TER TRAVADO-----------------------------")
                api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
                mentions = api.mentions_timeline()
    
    except tweepy.TweepError as connect_error:
        
        if (connect_error.api_code == 500 or
            connect_error.api_code == 502 or
            connect_error.api_code == 503 or
            connect_error.api_code == 504):
            
            print("connection error")
            bool_error = True
            
        else:
            raise connect_error
    
    return mentions, bool_error


#Função que filtra apenas as mentions uteis
def filter_mentions(not_filtered_mentions):
    global api
    
    filtered = []
    for status in not_filtered_mentions:
        
        try:
            mention_user = api.get_user(status.user.id)

        except TimeoutError:
            print("-----------------------------ERA PRA TER TRAVADO-----------------------------")
            api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
            mention_user = api.get_user(status.user.id)

        if (not mention_user.screen_name == "bot_poliglota" 
            and "/translate" in status.text 
            and status.in_reply_to_status_id != None):
            
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
    filtered_flags = []
    different_flags = []
    
    for cod in ascii_codes:
            if cod >= 127462 and cod <= 127487:
                filtered_flags.append(str(cod))
            
            if(cod == 127988):
                different_flags.append(str(cod))

    
    return filtered_flags, different_flags


# Função que junta os dois códigos das bandeiras
def unite_flags(normal_separated_flags, different_separated_flags):
    united_flags = []
    i = 0
    
    while i < len(normal_separated_flags)-1:
        united = normal_separated_flags[i] + normal_separated_flags[i+1]
        united_flags.append(united)
        i = i + 2

    if len(different_separated_flags) != 0:
        united_flags.append("127468127463")
    
    return united_flags


#Função que pega a mention e retorna apenas os códigos das bandeiras dectadas
def get_flags_from_mention(mention_text):

    emojis_in_ascii = filter_emojis(mention_text)
    pure_divided_normal_flags, pure_divided_different_flags = filter_flags(emojis_in_ascii)
    flags = unite_flags(pure_divided_normal_flags, pure_divided_different_flags)
    
    return flags


#Função que relaciona a flag com a lingua
def get_language(country):
    return languages_dict[country]

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


# Função que tweeta
def do_tweet(tweet_text, id_to_reply, user_from_original_tweet):
    global api

    try:
        id_to_reply = api.update_status(tweet_text, 
        in_reply_to_status_id=id_to_reply.id, 
        auto_populate_reply_metadata=True,
        exclude_reply_user_ids = user_from_original_tweet.id)
    
    except tweepy.TweepError as dup_error:
    
        if dup_error.api_code == 187:
            print("duplicated message")
        else:
            raise dup_error
    
    except TimeoutError:
        print("-----------------------------ERA PRA TER TRAVADO-----------------------------")
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

        id_to_reply = api.update_status(tweet_text, 
        in_reply_to_status_id=id_to_reply.id, 
        auto_populate_reply_metadata=True,
        exclude_reply_user_ids = user_from_original_tweet.id)
    

    return id_to_reply


# ======================================================================================================================


last_id = environ["last_id"]


while True:


    mentions_list, error = get_mentions(last_id)

    while error:
        time.sleep(45)
        mentions_list, error = get_mentions(last_id)
    
    mentions_list = filter_mentions(mentions_list)


    if len(mentions_list) != 0:
        
        environ["last_id"] = str(mentions_list[0].id)
        last_id = int(mentions_list[0].id)


    for status in mentions_list:
        

        try: 
            original_status = api.get_status(status.in_reply_to_status_id)
            original_user = api.get_user(original_status.user.id)
        
        except tweepy.TweepError as read_error:
            if read_error.api_code == 179:
                print("unable to read the tweet")
                break
            else:
                raise read_error
        
        except TimeoutError:
            print("-----------------------------ERA PRA TER TRAVADO-----------------------------")
            api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
            
            original_status = api.get_status(status.in_reply_to_status_id)
            original_user = api.get_user(original_status.user.id)

       

        if original_status.truncated:
            
            try:
                extended_status = api.get_status(original_status.id, tweet_mode='extended')
                original_text = extended_status._json['full_text']
            
            except TimeoutError:
                print("-----------------------------ERA PRA TER TRAVADO-----------------------------")
                api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

                extended_status = api.get_status(original_status.id, tweet_mode='extended')
                original_text = extended_status._json['full_text']
        
        else:
            original_text = original_status.text

        
        translation_needed = remove_emoji(original_text)
        print("o tweet a ser traduzido:", translation_needed, "\n")


        buffer = dict()

        flags = get_flags_from_mention(status.text)
        
        for flag in flags:


            languages = get_language(flag)
            base_language = languages[0]

            first_letter, second_letter = emojize_flag_code(flag)


            if base_language == "undefined":

                final_text = "translations for " + first_letter + second_letter + " unavaliable"
                do_tweet(final_text, status.id, original_user)

            else:

                tweet_to_reply = status


                for language in languages:
                    

                    if language in buffer:
                        translation = buffer[language]
                    
                    else:
                        translated = translator.translate(translation_needed, dest=language)
                        translation = translated.text
                        buffer[base_language] = translated.text
                    

                    if len(translation) > 273:

                        final_text_part1 = first_letter + second_letter + ' "' + translation[:273] + "+"
                        tweet_to_reply = do_tweet(final_text_part1, tweet_to_reply)

                        final_text_part2 = translation[273:] + '"'
                        do_tweet(final_text_part2, tweet_to_reply, original_user)

                    else:

                        final_text = first_letter + second_letter + ' "' + translation + '"'
                        print(final_text)
                        tweet_to_reply = do_tweet(final_text, tweet_to_reply, original_user)
    
    time.sleep(15)