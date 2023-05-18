import csv
import random


files_directory_prefix = ''

US_tweets_file = files_directory_prefix + 'Data/USTweets.csv'
UK_tweets_file = files_directory_prefix + 'Data/UKTweets.csv'
CAN_tweets_file = files_directory_prefix + 'Data/CANTweets.csv'
IR_tweets_file = files_directory_prefix + 'Data/IRTweets.csv'
AUS_tweets_file = files_directory_prefix + 'Data/AUSTweets.csv'
new_US_file = files_directory_prefix + 'NewData/USTweets.csv'
new_UK_file = files_directory_prefix + 'NewData/UKTweets.csv'
new_CAN_file = files_directory_prefix + 'NewData/CANTweets.csv'
new_IR_file = files_directory_prefix + 'NewData/IRTweets.csv'
new_AUS_file = files_directory_prefix + 'NewData/AUSTweets.csv'
new_SA_file = files_directory_prefix + 'NewData/SATweets.csv'
new_SINGA_file = files_directory_prefix + 'NewData/SINGAPORETweets.csv'


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


