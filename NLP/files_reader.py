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


class filesReader:
    #csv headings: id, created_at, source, original_text, clean_text, favorite_count, retweet_count, hashtags, trend
    @staticmethod
    def read_file(file_name):
        with open(file_name) as data_file:
            tweets_and_trends = []
            data = csv.reader(data_file)
            data.__next__()
            for row in data:
                new_row = []
                new_row.append(row[4])
                new_row.append(row[8])
                tweets_and_trends.append(new_row)
        return tweets_and_trends


    @staticmethod
    def add_and_shuffle_new_tweets_and_trends(current_tweets_and_trends, new_tweets_and_trends):
        current_tweets_and_trends.append(new_tweets_and_trends)
        random.shuffle(current_tweets_and_trends)
        return current_tweets_and_trends


    @staticmethod
    def split_tweets_and_trends(tweets_and_trends):
        tweets = [row[0] for row in tweets_and_trends]
        trends = [row[1] for row in tweets_and_trends]
        return tweets, trends



