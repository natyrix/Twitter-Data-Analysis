# Twitter-Data-Analysis

**Table of content**

 [Twitter-Data-Analysis](#Twitter-Data-Analysis)
  - [Introduction](#introduction)
  - [About the Data](#about-data)
  - [How to use](#How-to-use)
  - [Project/File Structure](#project-structure)
    - [notebooks](#notebooks)
    - [st_dashboard](#dashboard)
    - [tests](#tests)
    - [clean_tweets_dataframe.py](#clean_tweets_dataframe)
    - [extract_dataframe.py](#extract_dataframe.py)



## introduction

<p>
Topic Modeling and Sentiment Analysis for Twitter Data Collected Based on the Keywords:
[‘chinaus’, ‘chinaTaiwan’, ‘chinaTaiwancrisis’, ‘taiwan’, ‘XiJinping’, ‘USCHINA’, ‘pelosi’, ‘TaiwanStraitsCrisis’, ‘WWIII’, ‘pelosivisittotaiwan’] 
</p>

## about-data
<p>
As mentioned above the data was collected from the twitter API by using the above keywords and the pre-processed data is located on the folder st_dashboard/processed_global_data_tweets.csv, the row data was too big to push to the repo.
</p>

## How to use

To learn more about this project and play around 
        
            git clone https://github.com/natyrix/Twitter-Data-Analysis.git

            cd Twitter-Data-Analysis

            pip install -r requirements.txt
        
  
## Project Structure

### notebooks 
This folder holds the nooteboks used to read, pre-process and visualize the twitter data 
- Data exploration and Preprocessing - holds Exploratory Data Analysis and visualizations
- Sentiment_analyzer_and_topic_modelling - holds topic modeling and sentiment analysis
### st_dashboard 
This folder holds streamlit dashboard codes, including database schema
### tests
This folder holds unit test files, and sample_data for our CI tests
### clean_tweets_dataframe.py
This folder holds all the function for cleaning the raw data. 
### extract_dataframe.py
This folder holds all the function responsible for extracting the raw json data.

