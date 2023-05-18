import tensorflow as tf
from .files_reader import *
import numpy as np
from keras.utils import pad_sequences
from keras.preprocessing.text import Tokenizer
import pickle
from functools import reduce
from NLP.lemmatizer_and_stemmer import LemmatizerAndStemmer


model_file_path = "./NLP/trends_classifier/trends_classifier_model.h5"
tokenizer_file_path = "./NLP/trends_classifier/tweet_tokenizer.pkl"
index_to_trend_map_path = "./NLP/trends_classifier/inv_trends_map.pkl"


class RecommendationEngine:
    """
    The purpose of this class is that it takes a tweet and recommends hashtags for that tweet. 
    The recommender first uses the model to predict the trend of the given tweet and scans the data for the most 
    relevant hashtags belonging to the given trend.
    """
    def __init__(self, data_files_paths, pad_length) -> None:
        """
        The init function consists of several steps:
            1. load the model data.
                1.a load the saved model which will predict the trend that the tweet belongs to.
                1.b load the tokenizer object of the model that contains the mappings of all the words in the current dataset 
                to the index of that word. This tokenizer will be used to transform the passed tweet text to sequence of numbers.
                1.c load the index to trend map of the model that contains the mappings of each trend index to the trend. This
                dictionary will be used to translate the model predictions from an index to a word.
            2. create the trends to hashtags dictionary, the trends to hashtags is a dictionary of dictionaries. Each entry maps 1
            trend to a dictionary of the hashtags that belong to that trend and in the inner dictionary each entry maps each hashtags to
            the number of times this hashtag was used.
                2.a read the data of all the passed files using the file reader.
                2.b iterate over the rows in the data. Each row contains 1 trend and a list of hashtags used in the tweet.
                3.c add the hashtag to the trend in the trends to hashtags, or increment the hashtag if the hashtag already exists.
            3. finally we need to get the top trending hashtags and trends to we just count the frequency of each trend and hashtag
            and make a sorted list of the frequencies and get the most common 10.
        """
        #Step 1.a
        self.__model = tf.keras.models.load_model(model_file_path)
        self.__pad_length = pad_length

        #step 1.b
        with open(tokenizer_file_path, 'rb') as tokenizer_file:
            self.__tokenizer = pickle.load(tokenizer_file)
        
        #step 1.c
        with open(index_to_trend_map_path, 'rb') as index_to_trend_map_file:
            self.__index_to_trend_map = pickle.load(index_to_trend_map_file)

        self.__trends_to_hashtags = {}
        data = []

        #step 2.a
        for data_file_path in data_files_paths:
            data += FilesReader.read_file(data_file_path)

        trends, hashtag_lists = FilesReader.split_trends_and_hashtags(data)

        #step 2.b, 2.c
        for trend, hashtag_list in zip(trends, hashtag_lists):
            for hashtag in hashtag_list:
                hashtag = hashtag.lower()
                if trend not in self.__trends_to_hashtags:
                    self.__trends_to_hashtags[trend] = {}
                    self.__trends_to_hashtags[trend][hashtag] = 1
                elif hashtag not in self.__trends_to_hashtags[trend]:
                    self.__trends_to_hashtags[trend][hashtag] = 1
                else:
                    self.__trends_to_hashtags[trend][hashtag] += 1
                    
        unique_trends, trends_frequency = np.unique(trends, return_counts=True)
        sorted_trends_indices = np.argsort(trends_frequency)[::-1]
        self.__sorted_trends = unique_trends[sorted_trends_indices]
        
        all_hashtags = reduce(lambda x, y: x + y, hashtag_lists)
        unique_hashtags, hashtags_frequency = np.unique(all_hashtags, return_counts=True)
        sorted_hashtags_indices = np.argsort(hashtags_frequency)[::-1]
        self.__sorted_hashtags = unique_hashtags[sorted_hashtags_indices]
        

    def __tweet_to_padded_sequence(self, tweet: str) -> list:
        """
        This function takes a tweet text and turns it into a sequence of numbers using the tokenizer.
        """
        tweet_sequence = self.__tokenizer.texts_to_sequences([tweet])[0]
        padded_tweet_sequence = pad_sequences([tweet_sequence], maxlen=self.__pad_length, padding='post')
        return padded_tweet_sequence

    
    def __predict_trend(self, tweet: str) -> list:
        """
        This function takes a tweet text and predicts the probabilities of each trend to which the tweet may belong to.
        """
        padded_tweet_sequence = self.__tweet_to_padded_sequence(tweet)
        prediction = (self.__model.predict(padded_tweet_sequence))
        trends_indices = np.argsort(prediction, axis=-1)[0][-3:]
        return [(self.__index_to_trend_map[trend_index], prediction[0][trend_index]) for trend_index in trends_indices]
    

    def recommend_hashtags(self, tweet: str) -> list:
        """
        This function takes a tweet text and returns a list of tuples containing the recommended hashtags and the probability
        of each hashtag. The probability of the hashtag is calculated as follows:
            P(hashtag) = (n/N) * T
            where
                n: the number of times the hashtag was used in the context of this trend.
                N: the total number of hashtags used in this trend.
                T: the predicted probability of the model for the trend.
        """
        tweet = LemmatizerAndStemmer.stem_and_lemmatize_tweet(tweet)
        trends = self.__predict_trend(tweet)

        hashtags = {}

        for trend, probability in trends:
            hashtags_count = 0
            trend_hashtags = sorted(self.__trends_to_hashtags[trend].items(), key=lambda x: x[1])
            for hashtag in trend_hashtags[-3:]:
                hashtags_count += hashtag[1]
            for hashtag, count in trend_hashtags[-3:]:
                if hashtag in hashtags:
                    hashtags[hashtag] += probability * count/hashtags_count
                else:
                    hashtags[hashtag] = probability * count/hashtags_count
        
        hashtags = [(hashtag, probability) for hashtag, probability in hashtags.items()]
        returned_list =  sorted(hashtags, key=lambda x: x[1])
        returned_list.reverse()
        return returned_list
    
    
    def get_top_trends(self) -> list:
        """
        This function returns the top trends in the current dataset.
        """
        return self.__sorted_trends[:10]
    
    
    def get_top_hashtags(self) -> list:
        """
        This function returns the top hashtags in the current dataset.
        """
        return self.__sorted_hashtags[:10]
