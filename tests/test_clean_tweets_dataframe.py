import unittest
import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join("../Twitter-Data-Analysis/")))

from extract_dataframe import read_json
from extract_dataframe import TweetDfExtractor
from clean_tweets_dataframe import Clean_Tweets

sampletweetsjsonfile = "./tests/sample_global.json"
_, tweet_list = read_json(sampletweetsjsonfile)

class TestCleanTweetsDataFrame(unittest.TestCase):

    def setUp(self) -> pd.DataFrame:
        self.extracted = TweetDfExtractor(tweet_list[:5])
        self.df = self.extracted.get_tweet_df()
        self.clean_df = Clean_Tweets(self.df)

    def test_extract_twitter_source(self):
        vals = ['Twitter for Android','Twitter for Android','Twitter for Android',
        'Twitter for Android','Twitter for iPhone']
        returned_source = self.df["source"].apply(self.clean_df.extract_twitter_source)
        self.assertEqual([x for x in returned_source], vals)
    
    def test_remove_non_english_tweets(self):
        self.assertEqual(len(self.clean_df.remove_non_english_tweets(self.df)), len(self.df))
    
    def test_remove_place_characters(self):
        vals =['','','Netherlands','Netherlands', 'Ayent Schweiz']
        returned_place = [x for x in self.clean_df.remove_place_characters(self.df)['place']]
        self.assertEqual(returned_place, vals)

    def test_convert_to_numbers(self):
        df = self.clean_df.convert_to_numbers(self.df)
        vals = ['float64','float64', 'int64', 'int64', 'int64']
        returned_types = [df['polarity'].dtype,df['subjectivity'].dtype,df['retweet_count'].dtype,
            df['favorite_count'].dtype,df['followers_count'].dtype,]
        self.assertEqual(returned_types, vals)
    
    def test_convert_to_datetime(self):
        df = self.clean_df.convert_to_datetime(self.df)
        self.assertEqual(df['created_at'].dtype, 'datetime64[ns, UTC]')
    
    def test_drop_duplicate(self):
        df = self.clean_df.drop_duplicate(self.df)
        self.assertEqual(len(df), 5)
    
    def test_drop_unwanted_column(self):
        df = self.clean_df.drop_unwanted_column(self.df)
        self.assertEqual(len(df.columns), 16)
        



if __name__ == "__main__":
    unittest.main()