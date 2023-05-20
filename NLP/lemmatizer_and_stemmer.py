import nltk
from nltk.stem import WordNetLemmatizer
from nltk.stem import SnowballStemmer
nltk.download('wordnet')
nltk.download('omw-1.4')


class LemmatizerAndStemmer:
    @staticmethod
    def lemmatize_tweet(tweet: str) -> str:
        """
        Lemmatizes a tweet. worst, worse, bad -> bad.
        :param tweet: The tweet to lemmatize.
        :return: The lemmatized tweet.
        """
        lemmatizer = WordNetLemmatizer()
        new_tweet = ""
        for word in tweet.split(' '):
            new_tweet += lemmatizer.lemmatize(word) + ' '
        return new_tweet
    
    
    @staticmethod
    def stem_tweet(tweet: str) -> str:
        """
        Stems a tweet. plays, playing -> play.
        :param tweet: The tweet to stem.
        :return: The stemmed tweet.
        """
        ps = SnowballStemmer("english")
        new_tweet = ""
        for word in tweet.split(' '):
            new_tweet += ps.stem(word) + ' '
        return new_tweet
    
    
    @staticmethod
    def stem_and_lemmatize_tweet(tweet: str) -> str:
        """
        Stems and lemmatizes a tweet.
        :param tweet: The tweet to stem and lemmatize.
        :return: The stemmed and lemmatized tweet.
        """
        return LemmatizerAndStemmer.lemmatize_tweet(LemmatizerAndStemmer.stem_tweet(tweet))