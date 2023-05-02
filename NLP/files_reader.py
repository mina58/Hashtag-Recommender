import csv
import random

US_tweets_file = '../Data/USTweets.csv'
UK_tweets_file = '../Data/UKTweets.csv'
CAN_tweets_file = '../Data/CANTweets.csv'
IR_tweets_file = '../Data/IRTweets.csv'
AUS_tweets_file = '../Data/AUSTweets.csv'
new_US_file = '../NewData/USTweets.csv'
new_UK_file = '../NewData/UKTweets.csv'
new_CAN_file = '../NewData/CANTweets.csv'
new_IR_file = '../NewData/IRTweets.csv'
new_AUS_file = '../NewData/AUSTweets.csv'
new_SA_file = '../NewData/SATweets.csv'
new_SINGA_file = '../NewData/SINGAPORETweets.csv'


class FilesReader:
    #csv headings: id, created_at, source, original_text, clean_text, favorite_count, retweet_count, hashtags, trend
    @staticmethod
    def read_file(file_name):
        with open(file_name, encoding='utf-8') as data_file:
            tweets_and_trends = []
            data = csv.reader(data_file)
            data.__next__()
            for row in data:
                tweets_and_trends.append(row)
        return tweets_and_trends
    

    @staticmethod
    def split_tweets_and_trends(data):
        tweets = [row[4] for row in data]
        trends = [row[8] for row in data]
        return tweets, trends


    @staticmethod
    def split_trends_and_hashtags(data):
        trends = [row[8] for row in data]
        hashtags = []
        for row in data:
            new_row = []
            for word in row[7].split(','):
                new_row.append(word.strip())
            hashtags.append(new_row)
        return trends, hashtags


