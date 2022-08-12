import json
import pandas as pd
from textblob import TextBlob
import re
import sys
import os

sys.path.append(os.path.abspath(os.path.join("./scripts/")))
from logger import logger


def read_json(json_file: str) -> list:
    """
    json file reader to open and read json files into a list
    Args:
    -----
    json_file: str - path of a json file

    Returns
    -------
    length of the json file and a list of json
    """

    tweets_data = []
    try:
        for tweets in open(json_file, 'r'):
            tweets_data.append(json.loads(tweets))
        logger.info('Data Loaded')
    except Exception as e:
        logger.error(e)
    return len(tweets_data), tweets_data


class TweetDfExtractor:
    """
    this function will parse tweets json into a pandas dataframe

    Return
    ------
    dataframe
    """

    def __init__(self, tweets_list):

        self.tweets_list = tweets_list

    # an example function
    def find_statuses_count(self) -> list:
        try:
            statuses_count = [tweet['user']['statuses_count']
                          for tweet in self.tweets_list]
            logger.info(f"{len(statuses_count)} Status counts Loaded")
            return statuses_count
        except Exception as e:
            logger.error(e)
            return []

    def find_full_text(self) -> list:
        try:
            text = [tweet['full_text'] for tweet in self.tweets_list]
            text = [tweet['full_text'].replace(',', ' ')
                    for tweet in self.tweets_list]
            logger.info(f"{len(text)} Texts Loaded")
            return text
        except Exception as e:
            logger.error(e)
            return []

    def find_sentiments(self, text) -> list:
        polarity = []
        subjectivity = []
        sentiment = []
        try:
            for t in text:
                each_sentiment = TextBlob(t).sentiment
                polarity.append(each_sentiment.polarity)
                subjectivity.append(each_sentiment.subjectivity)
                if each_sentiment.polarity > 0:
                    sentiment.append("positive")
                elif each_sentiment.polarity < 0:
                    sentiment.append("negative")
                else:
                    sentiment.append("neutral")
            self.subjectivity = subjectivity
            logger.info(f"{len(polarity)} Polarity Loaded, {len(subjectivity)} subjectivity Loaded & {len(sentiment)} sentiment Loaded")
        except Exception as e:
            logger.error(e)
        return polarity, self.subjectivity, sentiment

    def find_created_time(self) -> list:
        try:
            created_at = [tweet['created_at'] for tweet in self.tweets_list]
            logger.info("CREATED AT LOADED")
            return created_at

        except Exception as e:
            logger.error(e)
        return []

    def find_source(self) -> list:
        try:
            source = [tweet['source'] for tweet in self.tweets_list]
            logger.info("SOURCE AT LOADED")
            return source
        except Exception as e:
            logger.error(e)
        return []

    def find_screen_name(self) -> list:
        try:
            screen_name = [tweet['user']['screen_name'].replace(
                ',', ' ') for tweet in self.tweets_list]
            logger.info("SCREEN NAME LOADED")
            return screen_name
        except Exception as e:
            logger.error(e)
        return []

    def find_followers_count(self) -> list:
        try:
            followers_count = [tweet['user']['followers_count']
                            for tweet in self.tweets_list]
            logger.info("FOLLOWERS COUNT LOADED")
            return followers_count
        except Exception as e:
            logger.error(e)
        return []

    def find_friends_count(self) -> list:
        try:
            friends_count = [tweet['user']['friends_count']
                            for tweet in self.tweets_list]
            logger.info("FRIENDS COUNT LOADED")
            return friends_count
        except Exception as e:
            logger.error(e)
        return []

    def is_sensitive(self) -> list:
        try:
            is_sensitive = [tweet['possibly_sensitive'] if 'possibly_sensitive' in tweet else None
                            for tweet in self.tweets_list]
            logger.info("IS SENSITIVE LOADED")
            
        except KeyError:
            logger.error(e)
            is_sensitive = []

        return is_sensitive

    def find_favourite_count(self) -> list:
        try:
            favorite_count = [tweet['user']['favourites_count']
                            for tweet in self.tweets_list]
            logger.info("FAVORITE COUNT LOADED")
            return favorite_count
        except Exception as e:
            logger.error(e)
        return []

    def find_retweet_count(self) -> list:
        try:
            retweet_count = [tweet['retweet_count'] for tweet in self.tweets_list]
            logger.info("RETWEET COUNT LOADED")
            return retweet_count
        except Exception as e:
            logger.error(e)
        return []

    def find_hashtags(self) -> list:
        hashtags = []
        try:
            for tweet in self.tweets_list:
                values = ""
                for hashtag in tweet['entities']['hashtags']:
                    if hashtag['text'] != "" or hashtag['text'] != " ":
                        values = values + \
                            hashtag['text'].replace(',', ' ') + "++++"
                hashtags.append(values)
            logger.info("HASHTAGS LOADED")
            
        except Exception as e:
            logger.error(e)

        return hashtags

    def find_mentions(self) -> list:
        mentions = []
        try:
            for tweet in self.tweets_list:
                values = ""
                for user_mentions in tweet['entities']['user_mentions']:
                    if user_mentions['screen_name'] != "" or user_mentions['screen_name'] != " ":
                        values = values + \
                            user_mentions['screen_name'].replace(',', ' ') + "++++"
                mentions.append(values)
            logger.info("MENTIONS LOADED")
        except Exception as e:
            logger.error(e)
        

        return mentions

    def find_location(self) -> list:
        try:
            location = [tweet['user']['location']
                        for tweet in self.tweets_list]
            logger.info("LOCATIONS LOADED")
            
        except TypeError:
            logger.error(e)
            location = []
        except Exception as e:
            logger.error(e)
            location = []

        return location

    def find_lang(self) -> list:
        try:
            lang = [tweet['lang'] for tweet in self.tweets_list]
            logger.info("LANGUAGES LOADED")
            return lang
        except Exception as e:
            logger.error(e)
            return []

    def find_clean_text(self) -> list:
        try:
            clean_text = [re.sub("[^a-zA-Z0-9#@\s’,_]", "", text)
                        for text in self.find_full_text()]
            clean_text = [re.sub("\s+", " ", text) for text in clean_text]
            logger.info("CLEAN TEXT LOADED")
            return clean_text
        except Exception as e:
            logger.error(e)
            return []

    def get_tweet_df(self, save=False) -> pd.DataFrame:
        """required column to be generated you should be creative and add more features"""

        try:
            columns = ['created_at', 'source', 'full_text', 'polarity', 'subjectivity', 'sentiment','lang', 'favorite_count', 'retweet_count',
                    'original_author', 'followers_count', 'friends_count', 'possibly_sensitive', 'hashtags', 'user_mentions', 'place']

            created_at = self.find_created_time()
            source = self.find_source()
            full_text = self.find_full_text()
            polarity, subjectivity, sentiment = self.find_sentiments(full_text)
            lang = self.find_lang()
            fav_count = self.find_favourite_count()
            retweet_count = self.find_retweet_count()
            screen_name = self.find_screen_name()
            followers_count = self.find_followers_count()
            friends_count = self.find_friends_count()
            sensitivity = self.is_sensitive()
            hashtags = self.find_hashtags()
            mentions = self.find_mentions()
            location = self.find_location()
            full_text = self.find_clean_text()
            data = zip(created_at, source, full_text, polarity, subjectivity, sentiment, lang, fav_count, retweet_count,
                    screen_name, followers_count, friends_count, sensitivity, hashtags, mentions, location)
            df = pd.DataFrame(data=data, columns=columns)

            if save:
                df.to_csv('processed_tweet_data_global.csv', index=False)
                print('File Successfully Saved.!!!')
            logger.info("TWEETS LOADED")
            return df
        except Exception as e:
            logger.error(e)
            return None


if __name__ == "__main__":
    # required column to be generated you should be creative and add more features
    columns = ['created_at', 'source', 'original_text', 'clean_text', 'sentiment', 'polarity', 'subjectivity', 'lang', 'favorite_count', 'retweet_count',
               'original_author', 'screen_count', 'followers_count', 'friends_count', 'possibly_sensitive', 'hashtags', 'user_mentions', 'place', 'place_coord_boundaries']
    _, tweet_list = read_json(
        "./data/global_twitter_data.json")
    tweet = TweetDfExtractor(tweet_list)
    tweet_df = tweet.get_tweet_df(save=True)

    # use all defined functions to generate a dataframe with the specified columns above
