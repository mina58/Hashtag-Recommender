# # Twitter API Access
# 
# In order to use it to make requests to Twitter's API, you'll need to go to https://dev.twitter.com/apps and create a sample application.
# 
# Under **Key and Access Tokens**, there are four primary identifiers you'll need to note:
# * consumer key,
# * consumer secret,
# * access token, and
# * access token secret (Click on Create Access Token to create those).
# 
# Note that you will need an ordinary Twitter account in order to login, create an app, and get these credentials.

#Libraries Needed
import tweepy
import pandas as pd
import re
import preprocessor as p
import nltk
import string
import os
from dotenv import load_dotenv
nltk.download('stopwords')
nltk.download('punkt')
#A stop word is a commonly used word (such as “the”, “a”, “an”, “in”)
stop_words = set(nltk.corpus.stopwords.words('english'))


#Authorizing an application to access Twitter account data

load_dotenv() # loads environment variables from .env file
#API_key
a_k = os.environ.get('TWITTER_API_KEY')

#API_Secret_Key
a_sk = os.environ.get('TWITTER_API_SECRET_KEY')

#Access_Token
a_t = os.environ.get('TWITTER_ACCESS_TOKEN')

#Access_Token_Secret
a_s = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')

auth = tweepy.OAuthHandler(a_k, a_sk)
auth.set_access_token(a_t, a_s)
api = tweepy.API(auth , wait_on_rate_limit=True)


#Creating the Ouput file and specifying the columns

#New Files
USFile = r"..\NewData\USTweets.csv"
UKFile = r"..\NewData\UKTweets.csv"
AUSFile = r"..\NewData\AUSTweets.csv"
CANFile = r"..\NewData\CANTweets.csv"
IRFile = r"..\NewData\IRTweets.csv"
#Total Files
tUSFile = r"..\Data\USTweets.csv"
tUKFile = r"..\Data\UKTweets.csv"
tAUSFile = r"..\Data\AUSTweets.csv"
tCANFile = r"..\Data\CANTweets.csv"
tIRFile = r"..\Data\IRTweets.csv"
#columns of the csv file
COLS = ['id', 'created_at', 'source', 'original_text','clean_text','favorite_count',
        'retweet_count', 'hashtags','trend']


# # Resetting the New Files to include only New Tweets
for old in [USFile , UKFile , AUSFile , CANFile , IRFile , ]:
    df = pd.read_csv(old, header=None)
    df.head(1).to_csv(old, index=False, header=False)


# Handling unwanted characters in the tweet

#handle emoticons and emojis

happyEmoticons = {':-)', ':)', ';)', ':o)', ':]', ':3', ':c)', ':>', '=]', '8)', '=)', ':}', ':^)', ':-D', ':D', '8-D',
                   '8D', 'x-D', 'xD', 'X-D', 'XD', '=-D', '=D', '=-3', '=3', ':-))', ":'-)", ":')", ':*', ':^*', '>:P',
                   ':-P', ':P', 'X-P', 'x-p', 'xp', 'XP', ':-p', ':p', '=p', ':-b', ':b', '>:)', '>;)', '>:-)', '<3'}

sadEmoticons = {':L', ':-/', '>:/', ':S', '>:[', ':@', ':-(', ':[', ':-||', '=L', ':<', ':-[', ':-<', '=\\', '=/',
                 '>:(', ':(', '>.<', ":'-(", ":'(", ':\\', ':-c', ':c', ':{', '>:\\', ';('}

emoticons = happyEmoticons.union(sadEmoticons)


emojis = re.compile("["
         u"\U0001F600-\U0001F64F"  # emoticons
         u"\U0001F300-\U0001F5FF"  # symbols & pictographs
         u"\U0001F680-\U0001F6FF"  # transport & map symbols
         u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
         u"\U00002702-\U000027B0"
         u"\U000024C2-\U0001F251"
         "]+", flags=re.UNICODE)


# Further Cleaning for the Tweet
def clean_tweets(tweet):
#after tweepy preprocessing the colon symbol still exists after removing mentions
    tweet = re.sub(r':', '', tweet)
#Unhandled symbols to be removed
    tweet = re.sub(r'‚Ä¶', '', tweet)
#replace consecutive non-ASCII characters with a space
    tweet = re.sub(r'[^\x00-\x7F]+',' ', tweet)
#remove emojis from tweet
    tweet = emojis.sub(r'', tweet)
#removing hashtag symbol
    tweet = re.sub("#" ,"" , tweet )
#removing quotation marks
    tweet = re.sub('[\'\"]', '', tweet)
#removing numbers
    tweet = re.sub('[0-9]+','' , tweet)

    word_tokens = nltk.word_tokenize(tweet)
#filter using NLTK library append it to a string
    filtered_tweet = [w for w in word_tokens if not w in stop_words \
                      and w not in emoticons and w not in string.punctuation]
    #convert list to string , space separated.
    return ' '.join(filtered_tweet)


#Retrieving Tweets and Saving the Output in the CSV File
def save_tweets(topic, totalFile, newFile):
    header = not os.path.exists(totalFile)
    df_final = pd.DataFrame(columns=COLS)
    for tweet in tweepy.Cursor(api.search_tweets, q=topic, lang='en', count=10000).items(10000):
        statuses = [tweet]
        for status in statuses:
            parsedData = []
            clean_text = p.clean(status.text)
            filtered_tweet = clean_tweets(str(clean_text).lower())
            if not len(filtered_tweet):
                continue
            parsedData += [status.id, status.created_at,
              status.source, status.text, filtered_tweet,
              status.favorite_count, status.retweet_count]
            hashtags = ", ".join([hashtag_item['text'] for hashtag_item in status.entities['hashtags']])
            hashtags = re.sub('#','',hashtags)
            topic = re.sub('#','',topic)
            parsedData.append(hashtags) #append the hashtags
            parsedData.append(topic) #append the trend allocated to each tweet
            single_tweet_df = pd.DataFrame([parsedData], columns=COLS)
            df_final = pd.concat([df_final, single_tweet_df], ignore_index=True)
    df_final.drop_duplicates(subset=['clean_text'], inplace=True)
    df_final.to_csv(totalFile, columns=COLS, mode='a', index=False, header=header, encoding='utf-8')
    df_final.to_csv(newFile , columns=COLS , mode='a' , index = False , header = False , encoding='utf-8')


#Getting Trending Topics according to the Place ID
def get_trends_and_tweets(place_id , id):
    trends = api.get_place_trends(id = place_id)
    for i in range(10):
       if id == 1:
           save_tweets(trends[0]['trends'][i]['name'] , tUSFile , USFile)
       elif id == 2:
           save_tweets(trends[0]['trends'][i]['name'] , tUKFile , UKFile)
       elif id == 3:
           save_tweets(trends[0]['trends'][i]['name'] , tCANFile , CANFile)
       elif id == 4:
           save_tweets(trends[0]['trends'][i]['name'] , tAUSFile , AUSFile)
       elif id == 5:
           save_tweets(trends[0]['trends'][i]['name'] , tIRFile , IRFile)


# Twitter identifies locations using the Yahoo! Where On Earth ID.
US_WOE_ID = 23424977
UK_WOE_ID = 23424975
Canada_WOE_ID = 23424775
AUS_WOE_ID = 23424748
IR_WOE_ID = 23424803


get_trends_and_tweets(US_WOE_ID , 1)
get_trends_and_tweets(UK_WOE_ID , 2)
get_trends_and_tweets(Canada_WOE_ID , 3)
get_trends_and_tweets(AUS_WOE_ID , 4)
get_trends_and_tweets(IR_WOE_ID , 5)



#Removing Duplicates and Shuffling Rows in CSV File
#When we want to scrap more tweets in the csv file , this could result in adding tweets we already got days ago.
files = [USFile, UKFile, CANFile, AUSFile, IRFile , tIRFile ,
         tUKFile , tUSFile , tCANFile , tAUSFile]
for file in files:
    df = pd.read_csv(file)
    df.drop_duplicates(subset=['clean_text'], inplace=True)
    df = pd.concat([df[:1], df[1:].sample(frac=1)]).reset_index(drop=True)
    df.to_csv(file, header=True, index=False, encoding='utf-8')

