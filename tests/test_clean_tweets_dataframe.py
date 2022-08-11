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



if __name__ == "__main__":
    unittest.main()