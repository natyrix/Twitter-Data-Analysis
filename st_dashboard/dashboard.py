import numpy as np
import pandas as pd
import streamlit as st
import altair as alt
from wordcloud import WordCloud
import plotly.express as px
from add_data import db_execute_fetch

st.set_page_config(page_title="Day 5", layout="wide")
loaded_df = None
def loadData():
    query = "select * from TweetInformation"
    df = db_execute_fetch(query, dbName="tweets", rdf=True)
    loaded_df = df
    return df

def selectHashTag():
    df = loadData() if loaded_df is None else loaded_df
    hashTags = st.multiselect("choose combaniation of hashtags", list(df['hashtags'].unique()))
    if hashTags:
        df = df[np.isin(df, hashTags).any(axis=1)]
        st.write(df)

def selectLocAndAuth():
    df = loadData() if loaded_df is None else loaded_df
    location = st.multiselect("choose Location of tweets", list(df['place'].unique()))
    lang = st.multiselect("choose Language of tweets", list(df['language'].unique()))

    if location and not lang:
        df = df[np.isin(df, location).any(axis=1)]
        st.write(df)
    elif lang and not location:
        df = df[np.isin(df, lang).any(axis=1)]
        st.write(df)
    elif lang and location:
        location.extend(lang)
        df = df[np.isin(df, location).any(axis=1)]
        st.write(df)
    else:
        st.write(df)

def barChart(data, title, X, Y):
    title = title.title()
    st.title(f'{title} Chart')
    msgChart = (alt.Chart(data).mark_bar().encode(alt.X(f"{X}:N", sort=alt.EncodingSortField(field=f"{Y}", op="values",
                order='ascending')), y=f"{Y}:Q"))
    st.altair_chart(msgChart, use_container_width=True)

def wordCloud():
    df = loadData() if loaded_df is None else loaded_df
    cleanText = ''
    for text in df['full_text']:
        tokens = str(text).lower().split()

        cleanText += " ".join(tokens) + " "

    wc = WordCloud(width=650, height=450, background_color='white', min_font_size=5).generate(cleanText)
    st.title("Tweet Text Word Cloud")
    st.image(wc.to_array())

def stBarChart():
    df = loadData() if loaded_df is None else loaded_df
    dfCount = pd.DataFrame({'Tweet_count': df.groupby(['original_author'])['full_text'].count()}).reset_index()
    dfCount["original_author"] = dfCount["original_author"].astype(str)
    dfCount = dfCount.sort_values("Tweet_count", ascending=False)

    num = st.slider("Select number of Rankings", 0, 50, 5)
    title = f"Top {num} Ranking By Number of tweets"
    barChart(dfCount.head(num), title, "original_author", "Tweet_count")

def sourcePie():
    df = loadData() if loaded_df is None else loaded_df
    dfSourceCount = pd.DataFrame({'Tweet_count': df.groupby(['source'])['full_text'].count()}).reset_index()
    dfSourceCount['source'] = dfSourceCount['source'].astype(str)
    dfSourceCount = dfSourceCount.sort_values("Tweet_count", ascending=False)
    dfSourceCount.loc[dfSourceCount['Tweet_count'] < 10, 'source'] = 'Other sources'
    st.title("Tweet source pie chart")
    fig = px.pie(dfSourceCount, values='Tweet_count', names='source', width=500, height=350)
    fig.update_traces(textposition='inside', textinfo='percent+label')

    colB1, colB2 = st.columns([2.5, 1])

    with colB1:
        st.plotly_chart(fig)
    with colB2:
        st.write(dfSourceCount)

def langPie():
    df = loadData() if loaded_df is None else loaded_df
    dfLangCount = pd.DataFrame({'Tweet_count': df.groupby(['language'])['full_text'].count()}).reset_index()
    dfLangCount["language"] = dfLangCount["language"].astype(str)
    dfLangCount = dfLangCount.sort_values("Tweet_count", ascending=False)
    dfLangCount.loc[dfLangCount['Tweet_count'] < 10, 'lang'] = 'Other languages'
    st.title(" Tweets Language pie chart")
    fig = px.pie(dfLangCount, values='Tweet_count', names='language', width=500, height=350)
    fig.update_traces(textposition='inside', textinfo='percent+label')

    colB1, colB2 = st.columns([2.5, 1])

    with colB1:
        st.plotly_chart(fig)
    with colB2:
        st.write(dfLangCount)


st.title("Data Display")
selectHashTag()
st.markdown("<p style='padding:10px; background-color:#000000;color:#00ECB9;font-size:16px;border-radius:10px;'>Section Break</p>", unsafe_allow_html=True)
selectLocAndAuth()
st.title("Data Visualizations")
wordCloud()
with st.expander("Show More Graphs"):
    stBarChart()
    langPie()

with st.expander("Show Other Graphs"):
    sourcePie()