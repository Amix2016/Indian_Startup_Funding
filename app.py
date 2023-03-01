import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import regex

st.set_page_config(layout='wide', page_title='StartUp Analysis')

df = pd.read_csv('startup_cleaned.csv')
df['date'] = pd.to_datetime(df['date'])
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month

# grouping dataframe based on year and startup to find max amount received by startup for every year
grouped_df = df.groupby(['year', 'startup'])['amount'].max().reset_index()


def load_overall_analysis():
    st.title('Overall Analysis of Startups between 2015-2020')

    # total invested amount
    total = round(df['amount'].sum())
    # max amount raised by a startup
    max_amount = df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
    # avg amount invested
    avg_amount = df.groupby('startup')['amount'].sum().mean()
    # total funded startups
    num_startups = df['startup'].nunique()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric('Total Amount raised', str(total) + ' Cr')
    with col2:
        st.metric('Maximum amount raised', str(max_amount) + ' Cr')
    with col3:
        st.metric('Average amount raised', str(round(avg_amount, 2)) + ' Cr')
    with col4:
        st.metric('Funded StartUps', str(num_startups))

    # Month wise Analysis
    st.header('Month on Month Analysis')
    selected_option = st.selectbox('Select Type', ['Total', 'Count'])
    if selected_option == 'Total':
        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
        temp_df['x_axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')

        fig, ax = plt.subplots()
        ax.plot(temp_df['x_axis'], temp_df['amount'])
        plt.xticks(rotation=90)
        plt.xlabel('Month-Year')
        plt.ylabel('Amount in Crores')
        plt.title('Month wise Investment in Crores')
        st.pyplot(fig)
    else:
        temp_df = df.groupby(['year', 'month'])['startup'].count().reset_index()
        temp_df['x_axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')

        fig, ax = plt.subplots()
        ax.plot(temp_df['x_axis'], temp_df['startup'])
        plt.xticks(rotation=90)
        plt.xlabel('Month-Year')
        plt.ylabel('Number of Startup')
        plt.title('Month wise Investment Graph')
        st.pyplot(fig)

    # sector wise analysis
    st.header('Sector Wise Analysis')
    col1, col2 = st.columns(2)

    with col1:
        # top 5 sector by amount
        sector_series_amt = df.groupby('vertical')['amount'].sum().sort_values(ascending=False).head()

        st.subheader('5 Biggest Sectors Value wise')
        fig1, ax1 = plt.subplots()
        # ax1.barh(sector_series_amt.index,sector_series_amt.values)
        ax1.pie(sector_series_amt, labels=sector_series_amt.index, autopct='%0.01f%%')

        st.pyplot(fig1)

    with col2:
        sector_series_count = df.groupby('vertical')['startup'].count().sort_values(ascending=False).head()

        st.subheader('5 Biggest Sectors by count')
        fig1, ax1 = plt.subplots()
        # ax1.barh(sector_series_count.index, sector_series_count.values)
        ax1.pie(sector_series_count, labels=sector_series_count.index, autopct='%0.01f%%')

        st.pyplot(fig1)

    # Type of funding
    st.header('Top 5 funding round by Value')
    funding_series = df.groupby('round')['amount'].sum().sort_values(ascending=False).head()
    fig, ax = plt.subplots()
    ax.barh(funding_series.index, funding_series.values)

    st.pyplot(fig)

    # City wise analysis
    st.header('City Wise Funding')
    col1, col2 = st.columns(2)
    with col1:
        city_series = df.groupby('city')['amount'].sum().sort_values(ascending=False).head()
        st.subheader('Top 5 city by amount invested')
        fig1, ax1 = plt.subplots()
        ax1.pie(city_series, labels=city_series.index, autopct='%0.01f%%')

        st.pyplot(fig1)

    with col2:
        city_series_count = df.groupby('city')['startup'].count().sort_values(ascending=False).head()
        st.subheader('Top 5 city by companies registered')
        fig1, ax1 = plt.subplots()
        ax1.pie(city_series_count, labels=city_series_count.index, autopct='%0.01f%%')

        st.pyplot(fig1)

    # Top Startups yearwise
    st.header('Top StartUps Year Wise')
    option_top = st.selectbox('Select One', grouped_df['year'].unique())
    top_df_year = grouped_df[grouped_df['year'] == option_top].sort_values(by='amount', ascending=False).head()

    fig, ax = plt.subplots()
    ax.barh(top_df_year['startup'], top_df_year['amount'])

    st.pyplot(fig)

    # Top startups overall
    st.header('Top StartUps Overall')
    top_startup_overall = df.groupby('startup')['amount'].max().sort_values(ascending=False).head(10)

    fig, ax = plt.subplots()
    ax.barh(top_startup_overall.index, top_startup_overall.values)

    st.pyplot(fig)

    # Top Investors
    st.header('Top Investors')
    top_investor_series = df.groupby('investors')['amount'].sum().sort_values(ascending=False).head(10)

    fig, ax = plt.subplots()
    ax.barh(top_investor_series.index, top_investor_series.values)

    st.pyplot(fig)


def load_investor_details(investor):
    st.title(investor)

    # load the recent 5 investments of the investor
    last5_df = df[df['investors'].str.contains(investor)][
        ['date', 'startup', 'vertical', 'city', 'round', 'amount']].head()
    st.subheader('Most Recent Investments')
    st.dataframe(last5_df)

    col1, col2 = st.columns(2)
    with col1:
        # biggest 5 investment
        big_series = df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(
            ascending=False).head()
        st.subheader('5 Biggest Investments')
        fig, ax = plt.subplots()
        ax.bar(big_series.index, big_series.values)

        st.pyplot(fig)

    with col2:
        vertical_series = df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum()
        st.subheader('Sectors invested in')
        fig1, ax1 = plt.subplots()
        ax1.pie(vertical_series, labels=vertical_series.index, autopct='%0.01f%%')

        st.pyplot(fig1)

    col3, col4 = st.columns(2)
    with col3:
        round_series = df[df['investors'].str.contains(investor)].groupby('round')['amount'].sum()
        st.subheader('Round-wise investment')
        fig1, ax1 = plt.subplots()
        ax1.pie(round_series, labels=round_series.index, autopct='%0.01f%%')

        st.pyplot(fig1)

    with col4:
        city_series = df[df['investors'].str.contains(investor)].groupby('city')['amount'].sum()
        st.subheader('City-wise investment')
        fig1, ax1 = plt.subplots()
        ax1.pie(city_series, labels=city_series.index, autopct='%0.01f%%')

        st.pyplot(fig1)

    year_series = df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()
    st.subheader('YOY Investment')
    fig, ax = plt.subplots()
    ax.plot(year_series.index, year_series.values)

    st.pyplot(fig)


# Startup Analysis
def load_startup_details(startup):
    st.title(startup)

    # industry type
    industry = df[df['startup'] == startup]['vertical'].values[0]

    # sub-industry type
    sub_industry = df[df['startup'] == startup]['subvertical'].values[0]

    # location
    startup_city = df[df['startup'] == startup]['city'].values[0]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric('Industry', industry)
    with col2:
        st.metric('Sub-Industry', sub_industry)
    with col3:
        st.metric('City', startup_city)

    # funding rounds analysis


st.sidebar.title('Startup Funding Analysis')

option = st.sidebar.selectbox('Select One', ['Overall Analysis', 'Investor', 'Startup'])

if option == 'Overall Analysis':
    load_overall_analysis()
elif option == 'Investor':
    selected_investor = st.sidebar.selectbox('Select Investor', sorted(set(df['investors'].str.split(',').sum())))
    btn1 = st.sidebar.button('Find Investor Details')
    if btn1:
        load_investor_details(selected_investor)
else:
    selected_startup = st.sidebar.selectbox('Select Startup', sorted(df['startup'].unique().tolist()))
    btn2 = st.sidebar.button('Find Startup Details')
    if btn2:
        load_startup_details(selected_startup)
