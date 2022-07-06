import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st


def medal_tally(df):
    medal_tally = df.drop_duplicates(subset=["Team", "NOC", "Games", "Year", "City", "Sport", "Event", "Medal"])
    medal_tally = medal_tally.groupby("Country").sum()[["Gold", "Silver", "Bronze"]].sort_values("Gold",
                                                                                                 ascending=False).reset_index()
    medal_tally["Total"] = medal_tally["Gold"] + medal_tally["Silver"] + medal_tally["Bronze"]

    medal_tally["Gold"] = medal_tally["Gold"].astype("int")
    medal_tally["Silver"] = medal_tally["Silver"].astype("int")
    medal_tally["Bronze"] = medal_tally["Bronze"].astype("int")
    medal_tally["Total"] = medal_tally["Total"].astype("int")

    return medal_tally


def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, "Overall")
    years.insert(0, "Select")

    country = np.unique(df['Country'].dropna().values).tolist()
    country.sort()
    country.insert(0, "Overall")
    country.insert(0, "Select")

    return years, country


def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year != 'Select' and country != 'Select':

        if year == 'Overall' and country == 'Overall':
            temp_df = medal_df
        if year == 'Overall' and country != 'Overall':
            flag = 1
            temp_df = medal_df[medal_df['Country'] == country]
        if year != 'Overall' and country == 'Overall':
            temp_df = medal_df[medal_df['Year'] == int(year)]
        if year != 'Overall' and country != 'Overall':
            temp_df = medal_df[(medal_df['Year'] == year) & (medal_df['Country'] == country)]

        if flag == 1:
            country_year = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
        else:
            country_year = temp_df.groupby('Country').sum()[['Gold', 'Silver', 'Bronze']].sort_values(
                ['Gold', "Silver", "Bronze"], ascending=False).reset_index()

        country_year['Total'] = country_year['Gold'] + country_year['Silver'] + country_year['Bronze']
        country_year = country_year.loc[country_year["Total"] != 0]

        country_year['Gold'] = country_year['Gold'].astype('int')
        country_year['Silver'] = country_year['Silver'].astype('int')
        country_year['Bronze'] = country_year['Bronze'].astype('int')
        country_year['Total'] = country_year['Total'].astype('int')

        return country_year


def medal_tally_graph(df, year, country):
    graph_df = df.drop_duplicates(subset=['Team', 'NOC', 'Year', 'City', 'Sport', 'Event', 'Medal'])

    if year == 'Overall' and country == 'Overall':
        graph_df = graph_df.groupby('Country').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                               ascending=False).reset_index()
        graph_df['Total'] = graph_df['Gold'] + graph_df['Silver'] + graph_df['Bronze']
        graph_df = graph_df.head(10)
        fig = px.bar(graph_df, x="Country", y=["Gold", "Silver", "Bronze"], labels={"variable": "medal"})
        fig.update_layout(
            width=1200,
            height=600
        )
        st.plotly_chart(fig)

    if year == 'Overall' and country != 'Overall':
        graph_df = graph_df[graph_df['Country'] == country]
        graph_df = graph_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
        graph_df['Total'] = graph_df['Gold'] + graph_df['Silver'] + graph_df['Bronze']
        x = graph_df['Year']
        y = graph_df["Total"]
        plt.bar(x, y)
        plt.xlabel("year")
        plt.ylabel("Total Medals")
        # plt.rcParams["figure.figsize"] = (5, 5)
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()


    if year != "Overall" and country == "Overall":
        graph_df = graph_df[graph_df['Year'] == int(year)]
        graph_df = graph_df.groupby('Country').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                               ascending=False).reset_index()
        graph_df['Total'] = graph_df['Gold'] + graph_df['Silver'] + graph_df['Bronze']
        graph_df = graph_df.head(10)
        fig = px.bar(graph_df, x="Country", y="Total",labels={"variable":"Medal"})
        fig.update_layout(
            width=1200,
            height=600
        )
        st.plotly_chart(fig)


def participating_nations_overtime(df):
    nations_year = df.drop_duplicates(["Year", 'Country'])["Year"].value_counts().reset_index().sort_values("index")
    nations_year.rename(columns={"index": "Edition", "Year": "No of countries"}, inplace=True)

    return nations_year


def sports_overtime(df):
    sports_year = df.drop_duplicates(["Year", 'Sport'])["Year"].value_counts().reset_index().sort_values("index")
    sports_year.rename(columns={"index": "Edition", "Year": "No of sports"}, inplace=True)

    return sports_year


def events_overtime(df):
    events_year = df.drop_duplicates(["Year", 'Event'])["Year"].value_counts().reset_index().sort_values("index")
    events_year.rename(columns={"index": "Edition", "Year": "No of events"}, inplace=True)

    return events_year


def athlete_overtime(df):
    athlete_year = df.drop_duplicates(["Year", 'Name'])["Year"].value_counts().reset_index().sort_values("index")
    athlete_year.rename(columns={"index": "Edition", "Year": "No of athletes"}, inplace=True)

    return athlete_year


def most_successful(df, sport):
    temp_df = df.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    x = temp_df['Name'].value_counts().reset_index().head(15).merge(df, left_on='index', right_on='Name', how='left')[
        ['index', 'Name_x', 'Sport', 'Country']].drop_duplicates('index')
    x.rename(columns={'index': 'Name', 'Name_x': 'Medals'}, inplace=True)
    return x


def year_wise_medal_tally(df, country):
    temp_df = df.loc[df["Medal"] != "DNW"]
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['Country'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()

    return final_df

def country_event_heatmap(df, country):
    temp_df = df.loc[df["Medal"] != "DNW"]
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['Country'] == country]

    pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return pt

def most_successful_countrywise(df, country):
    temp_df = df.loc[df["Medal"] != "DNW"]
    temp_df = temp_df[temp_df['Country'] == country]

    x = temp_df['Name'].value_counts().reset_index().head(10).merge(df, left_on='index', right_on='Name', how='left')[
        ['index', 'Name_x', 'Sport']].drop_duplicates('index')
    x.rename(columns={'index': 'Name', 'Name_x': 'Medals'}, inplace=True)
    return x


def weight_v_height(df, sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'Country'])
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df

def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'Country'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final
