import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
from st_aggrid import AgGrid
from preprocessor import preprocess, w_preprocess
import helper

st.set_page_config(page_title="Olympic Data Analysis", page_icon="analysis.png", layout="wide")

hide_menu_style = """<style> 
                    #MainMenu {visibility:hidden;}
                    footer {visibility:hidden;}
                    </style>"""
st.markdown(hide_menu_style, unsafe_allow_html=True)

df = pd.read_csv("athlete_events.csv")
regions_df = pd.read_csv("noc_regions.csv")

df = preprocess(df, regions_df)

wdf = pd.read_csv("athlete_events.csv")
w_regions_df = pd.read_csv("noc_regions.csv")
wdf = w_preprocess(wdf, w_regions_df)

with st.sidebar:
    index = option_menu(menu_title="Index",
                        options=["Olympics Overview", "Olympic Data", "Analysis", "Insights", "Contact"],
                        icons=["0", "1", "2", "3", "4"],
                        menu_icon="list",
                        styles={
                            "nav-link": {"font-size": "20px",
                                         "text-align": "left"
                                         },
                            "nav-link-selected": {"background-color": "#f03557"}
                        }
                        )

if index == "Olympics Overview":
    st.markdown("<h1 style='text-align: center; color:#9b26c9 ;'>Olympics Overview</h1>", unsafe_allow_html=True)
    st.image("olympic.webp")
    st.write(
        """The modern Olympic Games or Olympics are leading international sporting events featuring summer and winter sports competitions in which thousands of athletes from around the world participate in a variety of competitions. The Olympic Games are considered the world’s foremost sports competition with more than 200 nations participating. The Olympic Games are held every four years, with the Summer and Winter Games alternating by occurring every four years but two years apart.""")

    st.write(
        """The evolution of the Olympic Movement during the 20th and 21st centuries has resulted in several changes to the Olympic Games. Some of these adjustments include the creation of the Winter Olympic Games for snow and ice sports, the Paralympic Games for athletes with a disability, the Youth Olympic Games for athletes aged 14 to 18, the five Continental games (Pan American, African, Asian, European, and Pacific), and the World Games for sports that are not contested in the Olympic Games. The Deaflympics and Special Olympics are also endorsed by the IOC. The IOC has had to adapt to a variety of economic, political, and technological advancements. As a result, the Olympics has shifted away from pure amateurism, as envisioned by Coubertin, to allowing participation of professional athletes. The growing importance of mass media created the issue of corporate sponsorship and commercialisation of the Games. World wars led to the cancellation of the 1916, 1940, and 1944 Games. Large boycotts during the Cold War limited participation in the 1980 and 1984 Games. The latter, however, attracted 140 National Olympic Committees, which was a record at the time.[Official website](https://olympics.com/en/)""")


if index == "Olympic Data":
    st.subheader("About the Dataset")
    st.write("This is a historical dataset on the modern Olympic Games, including all the Games from Athens 1896 to Rio 2016.The Dataset which is used is from [Kaggle](https://www.kaggle.com/datasets/heesoo37/120-years-of-olympic-history-athletes-and-results), authored by the user [rgriffin](https://www.kaggle.com/heesoo37).")
    st.write("Each row corresponds to an individual athlete competing in an individual Olympic event (athlete-events). The columns are:")

    st.write("ID - Unique number for each athlete, Name - Athlete's name, Sex - M or F, Age - Integer, Height - In centimeters, Weight - In kilograms, Team - Team name, NOC - National Olympic Committee 3-letter code, Games - Year and season, Year - Integer, Season - Summer or Winter, City - Host city, Sport - Sport, Event - Event, Medal - Gold, Silver, Bronze, or DNW(Did Not Win)")

    st.markdown("<h1 style='text-align: center; color:#f03557;'>Summer Olympic Data</h1>", unsafe_allow_html=True)
    df.insert(loc=0, column="S.No", value=[i for i in range(1, df.shape[0] + 1)])
    AgGrid(df)
    st.markdown("<h1 style='text-align: center; color:#f03557;'>Winter Olympic Data</h1>", unsafe_allow_html=True)
    wdf.insert(loc=0, column="S.No", value=[i for i in range(1, wdf.shape[0] + 1)])
    AgGrid(wdf)



if index == "Analysis":
    st.markdown("<h1 style='text-align: center; color:#f03557;'>Olympics Data Analysis</h1>", unsafe_allow_html=True)
    st.subheader("Olympic Season")
    olympic_type = st.selectbox("Select Season", ["Select", "Summer Olympics", "Winter Olympics"])

    if olympic_type == "Summer Olympics" or olympic_type == "Winter Olympics":
        select_option = option_menu(menu_title="Analysis",
                                    options=["Medal Tally", "Overall Analysis", "Country-wise Analysis",
                                             "Athlete wise Analysis"],
                                    icons=["0", "1", "2", "3", "4"],
                                    menu_icon="bar-chart-fill",
                                    orientation='horizontal',
                                    styles={
                                        "nav-link": {"font-size": "20px",
                                                     "text-align": "left"
                                                     },
                                        "nav-link-selected": {"background-color": "#f03557"}
                                    })

    if olympic_type == "Summer Olympics":
        if select_option == "Medal Tally":
            st.header("Medal Tally")

            years, country = helper.country_year_list(df)
            selected_year = st.selectbox("Select Year", years)
            selected_country = st.selectbox("Select Country", country)

            if selected_year != 'Select' and selected_country != 'Select':

                medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)
                medal_tally.insert(loc=0, column="S.No", value=[i for i in range(1, medal_tally.shape[0] + 1)])

                if selected_year == 'Overall' and selected_country == 'Overall':
                    st.header("Overall Medal Tally")
                    AgGrid(medal_tally)
                if selected_year != 'Overall' and selected_country == 'Overall':
                    st.header("Medal Tally in " + str(selected_year) + " Olympics")
                    AgGrid(medal_tally)
                if selected_year == 'Overall' and selected_country != 'Overall':
                    st.header(selected_country + " overall performance")
                    AgGrid(medal_tally)
                if selected_year != 'Overall' and selected_country != 'Overall':
                    if selected_year != 'Select' and selected_country != 'Select':
                        st.header(selected_country + " performance in " + str(selected_year) + " Olympics")
                        AgGrid(medal_tally)

                if selected_year == 'Overall' and selected_country == 'Overall':
                    st.header("Top 10 countries with Most Medals")
                    helper.medal_tally_graph(df, selected_year, selected_country)
                if selected_year == 'Overall' and selected_country != 'Overall':
                    st.header("Year-wise Medal Tally of " + selected_country)
                    helper.medal_tally_graph(df, selected_year, selected_country)
                if selected_year != 'Overall' and selected_country == 'Overall':
                    st.header("Top 10 countries with most medals in " + str(selected_year) + " Olympics")
                    helper.medal_tally_graph(df, selected_year, selected_country)

        if select_option == "Overall Analysis":
            st.header("Statistics")
            editions = df['Year'].unique().shape[0] - 1
            cities = df['City'].unique().shape[0]
            sports = df['Sport'].unique().shape[0]
            events = df['Event'].unique().shape[0]
            athletes = df.drop_duplicates(subset=['Name', 'Country']).shape[0]
            nations = df['Country'].unique().shape[0]

            col1, col2, col3 = st.columns(3)
            with col1:
                st.subheader("Editions")
                st.header(editions)
            with col2:
                st.subheader("Hosts")
                st.header(cities)
            with col3:
                st.subheader("Sports")
                st.header(sports)

            col1, col2, col3 = st.columns(3)
            with col1:
                st.subheader("Events")
                st.header(events)
            with col2:
                st.header("Nations")
                st.subheader(nations)
            with col3:
                st.subheader("Athletes")
                st.header(athletes)

            st.header("Which cities hosted olympics and How many Times?")
            host_df = df.drop_duplicates(["Year"])
            host_df = host_df.pivot_table(index=['City'], aggfunc='size')
            fig = px.bar(host_df)
            fig.update_layout(
                width=1200,
                height=600

            )
            st.plotly_chart(fig)
            st.write("It is clearly evident from the Bar chart that Athina,London,Los Angeles and Paris have hosted Summer Olympics more Number of times.")


            nations_year = helper.participating_nations_overtime(df)
            st.header("Participating countries overtime")
            fig = px.line(nations_year, x="Edition", y="No of countries")
            fig.update_layout(
                width=1200,
                height=600
            )
            st.plotly_chart(fig)
            st.write("Now,it is clearly evident from the line chart that participating countries have increased over the years.Number of Countries have come to a saturation point in the last 5 summer games")

            sports_year = helper.sports_overtime(df)
            st.header("No of sports overtime")
            fig1 = px.line(sports_year, x="Edition", y="No of sports")
            fig1.update_layout(
                width=1200,
                height=600
            )
            st.plotly_chart(fig1)
            st.write("Now,it is clearly evident from the line chart that sports have increased over the years.Number of sports have come to a saturation point in the last 5 summer games.34 sports competitions is the maximum in a summer olympic game.")

            events_year = helper.events_overtime(df)
            st.header("No of events overtime")
            fig2 = px.line(events_year, x="Edition", y="No of events")
            fig2.update_layout(
                width=1200,
                height=600
            )
            st.plotly_chart(fig2)
            st.write("Now,it is clearly evident from the line chart that events are continuously increased over the years.Number of events have come to a saturation point in the last 5 summer games.306 events is the maximum in a summer olympic game.")


            athlete_year = helper.athlete_overtime(df)
            st.header("No of athletes overtime")
            fig3 = px.line(athlete_year, x="Edition", y="No of athletes")
            fig3.update_layout(
                width=1200,
                height=600
            )
            st.plotly_chart(fig3)
            st.write("Number of participants have been increasing continuous in every olympic games.")

            st.title("No. of Events over time(Each Sport)")
            fig, ax = plt.subplots(figsize=(20, 20))
            x = df.drop_duplicates(['Year', 'Sport', 'Event'])
            ax = sns.heatmap(
                x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
                annot=True)
            st.pyplot(fig)



        if select_option == "Country-wise Analysis":
            st.header("Country-wise Analysis")
            country_list = np.unique(df['Country'].dropna().values).tolist()
            country_list.sort()
            country_list.insert(0, "select")
            selected_country = st.selectbox("Select Country", country_list)

            if selected_country != "select":
                st.header("Top 10 athletes of " + selected_country)
                top10_df = helper.most_successful_countrywise(df, selected_country)
                st.table(top10_df)

                st.header("Yearly Number of participants from " + selected_country)
                participants_df = df.loc[df["Country"] == selected_country]
                participants_df = participants_df.drop_duplicates(["Year", "Name"])[
                    "Year"].value_counts().reset_index().sort_values("index")
                participants_df = participants_df.rename(columns={"index": "Year", "Year": "No of participants"})
                fig4 = px.line(participants_df, x="Year", y="No of participants")
                fig4.update_layout(
                    width=1200,
                    height=600
                )
                st.plotly_chart(fig4)

                country_df = helper.year_wise_medal_tally(df, selected_country)
                st.header(selected_country + "'s Medal Tally Over the years")
                fig5 = px.line(country_df, x="Year", y="Medal")
                fig5.update_layout(
                    width=1200,
                    height=600
                )
                st.plotly_chart(fig5)

                st.header(selected_country + " excels in the following sports")
                pt = helper.country_event_heatmap(df, selected_country)
                fig, ax = plt.subplots(figsize=(15, 15))
                ax = sns.heatmap(pt, annot=True)
                st.pyplot(fig)



        if select_option == "Athlete wise Analysis":

            st.header("Most successful Athletes")
            sport_list = df['Sport'].unique().tolist()
            sport_list.sort()
            sport_list.insert(0, 'Overall')
            selected_sport = st.selectbox('Select a Sport', sport_list)
            x = helper.most_successful(df, selected_sport)
            x.insert(loc=0, column="S.No", value=[i for i in range(1, x.shape[0] + 1)])
            AgGrid(x)

            st.header("Men Vs Women Participation Over the Years")
            final = helper.men_vs_women(df)
            fig = px.bar(final, x="Year", y=["Male", "Female"], labels={"variable": "sex"})
            fig.update_layout(width=1200, height=600)
            st.plotly_chart(fig)
            st.write("There was dramatic improvement in female participation from 1956 to 2016.Only the first edition of Olympics didn't have any female athletes. There has been a great improvement in female representation ever since. Late 1950s and late 1980s saw significant increase in female representation.")

            athlete_df = df.drop_duplicates(subset=['Name', 'Country'])
            age = athlete_df['Age'].dropna()
            age_gold = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
            age_silver = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
            age_bronze = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

            fig = ff.create_distplot([age, age_gold, age_silver, age_bronze],
                                     ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                                     show_hist=False, show_rug=False)
            fig.update_layout(width=1200, height=600)
            st.header("Distribution of Age")
            st.plotly_chart(fig)

            height = athlete_df['Height'].dropna()
            height_gold = athlete_df[athlete_df['Medal'] == 'Gold']['Height'].dropna()
            height_silver = athlete_df[athlete_df['Medal'] == 'Silver']['Height'].dropna()
            height_bronze = athlete_df[athlete_df['Medal'] == 'Bronze']['Height'].dropna()

            fig = ff.create_distplot([height, height_gold, height_silver, height_bronze],
                                     ['Overall height', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                                     show_hist=False, show_rug=False)
            fig.update_layout(width=1200, height=600)
            st.header("Distribution of height")
            st.plotly_chart(fig)

            weight = athlete_df['Weight'].dropna()
            weight_gold = athlete_df[athlete_df['Medal'] == 'Gold']['Weight'].dropna()
            weight_silver = athlete_df[athlete_df['Medal'] == 'Silver']['Weight'].dropna()
            weight_bronze = athlete_df[athlete_df['Medal'] == 'Bronze']['Weight'].dropna()

            fig = ff.create_distplot([weight, weight_gold, weight_silver, weight_bronze],
                                     ['Overall weight', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                                     show_hist=False, show_rug=False)
            fig.update_layout(width=1200, height=600)
            st.header("Distribution of weight")
            st.plotly_chart(fig)




    if olympic_type == "Winter Olympics":
        if select_option == "Medal Tally":
            st.header("Medal Tally")

            years, country = helper.country_year_list(wdf)
            selected_year = st.selectbox("Select Year", years)
            selected_country = st.selectbox("Select Country", country)

            if selected_year != 'Select' and selected_country != 'Select':
                medal_tally = helper.fetch_medal_tally(wdf, selected_year, selected_country)
                medal_tally.insert(loc=0, column="S.No", value=[i for i in range(1, medal_tally.shape[0] + 1)])

                if selected_year == 'Overall' and selected_country == 'Overall':
                    st.header("Overall Medal Tally")
                    medal_tally = medal_tally.drop("Total", axis=1)
                    medal_tally["Total"] = medal_tally["Gold"] + medal_tally["Silver"] + medal_tally["Bronze"]
                    AgGrid(medal_tally)
                if selected_year != 'Overall' and selected_country == 'Overall':
                    st.header("Medal Tally in " + str(selected_year) + " Olympics")
                    AgGrid(medal_tally)
                if selected_year == 'Overall' and selected_country != 'Overall':
                    st.header(selected_country + " overall performance")
                    AgGrid(medal_tally)
                if selected_year != 'Overall' and selected_country != 'Overall':
                    if selected_year != 'Select' and selected_country != 'Select':
                        st.header(selected_country + " performance in " + str(selected_year) + " Olympics")
                        AgGrid(medal_tally)

                if selected_year == 'Overall' and selected_country == 'Overall':
                    st.header("Top 10 countries with Most Medals")
                    medal_tally = medal_tally.head(10)
                    fig = px.bar(medal_tally, x="Country", y=["Gold", "Silver", "Bronze"], labels={"variable": "medal"})
                    fig.update_layout(
                        width=1200,
                        height=600
                    )
                    st.plotly_chart(fig)

                if selected_year == 'Overall' and selected_country != 'Overall':
                    st.header("Year-wise Medal Tally of " + selected_country)
                    helper.medal_tally_graph(wdf, selected_year, selected_country)
                if selected_year != 'Overall' and selected_country == 'Overall':
                    st.header("Top 10 countries with most medals in " + str(selected_year) + " Olympics")
                    helper.medal_tally_graph(wdf, selected_year, selected_country)

        if select_option == "Overall Analysis":
            st.header("Statistics")
            editions = wdf['Year'].unique().shape[0]
            cities = wdf['City'].unique().shape[0]
            sports = wdf['Sport'].unique().shape[0]
            events = wdf['Event'].unique().shape[0]
            athletes = wdf.drop_duplicates(subset=['Name', 'Country']).shape[0]
            nations = wdf['Country'].unique().shape[0]

            col1, col2, col3 = st.columns(3)
            with col1:
                st.subheader("Editions")
                st.header(editions)
            with col2:
                st.subheader("Hosts")
                st.header(cities)
            with col3:
                st.subheader("Sports")
                st.header(sports)

            col1, col2, col3 = st.columns(3)
            with col1:
                st.subheader("Events")
                st.header(events)
            with col2:
                st.header("Nations")
                st.subheader(nations)
            with col3:
                st.subheader("Athletes")
                st.header(athletes)

            st.header("Which cities hosted olympics and How many Times?")
            host_df = wdf.drop_duplicates(["Year"])
            host_df = host_df.pivot_table(index=['City'], aggfunc='size')
            fig = px.bar(host_df)
            fig.update_layout(
                width=1200,
                height=600

            )
            st.plotly_chart(fig)
            st.write("It is clearly evident from the Bar chart that Innsbruck,Lake Placid and Sankt Mortiz have hosted Winter Olympics more Number of times. ")

            nations_year = helper.participating_nations_overtime(wdf)
            st.header("Participating countries overtime")
            fig = px.line(nations_year, x="Edition", y="No of countries")
            fig.update_layout(
                width=1200,
                height=600
            )
            st.plotly_chart(fig)
            st.write("Now,it is clearly evident from the line chart that participating countries have increased over the years.Number of Countries have come to a saturation point in the last 5 summer games.")

            sports_year = helper.sports_overtime(wdf)
            st.header("No of sports overtime")
            fig1 = px.line(sports_year, x="Edition", y="No of sports")
            fig1.update_layout(
                width=1200,
                height=600
            )
            st.plotly_chart(fig1)
            st.write("Now,it is clearly evident from the line chart that sports have increased over the years.Number of sports have come to a saturation point in the last 5 summer games.15 sports competitions is the maximum in a summer olympic game.")

            events_year = helper.events_overtime(wdf)
            st.header("No of events overtime")
            fig2 = px.line(events_year, x="Edition", y="No of events")
            fig2.update_layout(
                width=1200,
                height=600
            )
            st.plotly_chart(fig2)
            st.write("Now,it is clearly evident from the line chart that events are continuously increased over the years.Number of events have come to a saturation point in the last 5 summer games.98 events is the maximum in a summer olympic game.")

            athlete_year = helper.athlete_overtime(wdf)
            st.header("No of athletes overtime")
            fig3 = px.line(athlete_year, x="Edition", y="No of athletes")
            fig3.update_layout(
                width=1200,
                height=600
            )
            st.plotly_chart(fig3)


            st.title("No. of Events over time(Each Sport)")
            fig, ax = plt.subplots(figsize=(20, 20))
            x = wdf.drop_duplicates(['Year', 'Sport', 'Event'])
            ax = sns.heatmap(
                x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
                annot=True)
            st.pyplot(fig)



        if select_option == "Country-wise Analysis":
            st.header("Country-wise Analysis")
            country_list = np.unique(wdf['Country'].dropna().values).tolist()
            country_list.sort()
            country_list.insert(0, "select")
            selected_country = st.selectbox("Select Country", country_list)

            if selected_country != "select":
                st.header("Top 10 athletes of " + selected_country)
                top10_df = helper.most_successful_countrywise(wdf, selected_country)
                st.table(top10_df)

                st.header("Yearly Number of participants from " + selected_country)
                participants_df = wdf.loc[wdf["Country"] == selected_country]
                participants_df = participants_df.drop_duplicates(["Year", "Name"])[
                    "Year"].value_counts().reset_index().sort_values("index")
                participants_df = participants_df.rename(columns={"index": "Year", "Year": "No of participants"})
                fig4 = px.line(participants_df, x="Year", y="No of participants")
                fig4.update_layout(
                    width=1200,
                    height=600
                )
                st.plotly_chart(fig4)

                country_df = helper.year_wise_medal_tally(wdf, selected_country)
                st.header(selected_country + "'s Medal Tally Over the years")
                fig5 = px.line(country_df, x="Year", y="Medal")
                fig5.update_layout(
                    width=1200,
                    height=600
                )
                st.plotly_chart(fig5)

                st.header(selected_country + " excels in the following sports")
                pt = helper.country_event_heatmap(wdf, selected_country)
                fig, ax = plt.subplots(figsize=(15, 15))
                ax = sns.heatmap(pt, annot=True)
                st.pyplot(fig)
                st.write("There was dramatic improvement in athlete participation over the years.")



        if select_option == "Athlete wise Analysis":
            st.header("Most successful Athletes")
            sport_list = wdf['Sport'].unique().tolist()
            sport_list.sort()
            sport_list.insert(0, 'Overall')
            selected_sport = st.selectbox('Select a Sport', sport_list)
            x = helper.most_successful(df, selected_sport)
            x.insert(loc=0, column="S.No", value=[i for i in range(1, x.shape[0] + 1)])
            AgGrid(x)

            st.header("Men Vs Women Participation Over the Years")
            final = helper.men_vs_women(df)
            fig = px.bar(final, x="Year", y=["Male", "Female"], labels={"variable": "sex"})
            fig.update_layout(width=1200, height=600)
            st.plotly_chart(fig)
            st.write("There was dramatic improvement in female participation over the years.Only the first edition of Olympics didn't have any female athletes. There has been a great improvement in female representation ever since. Late 1950s and late 1980s saw significant increase in female representation.")


            athlete_df = wdf.drop_duplicates(subset=['Name', 'Country'])
            age = athlete_df['Age'].dropna()
            age_gold = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
            age_silver = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
            age_bronze = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

            fig = ff.create_distplot([age, age_gold, age_silver, age_bronze],
                                     ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                                     show_hist=False, show_rug=False)
            fig.update_layout(width=1200, height=600)
            st.header("Distribution of Age")
            st.plotly_chart(fig)

            height = athlete_df['Height'].dropna()
            height_gold = athlete_df[athlete_df['Medal'] == 'Gold']['Height'].dropna()
            height_silver = athlete_df[athlete_df['Medal'] == 'Silver']['Height'].dropna()
            height_bronze = athlete_df[athlete_df['Medal'] == 'Bronze']['Height'].dropna()

            fig = ff.create_distplot([height, height_gold, height_silver, height_bronze],
                                     ['Overall height', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                                     show_hist=False, show_rug=False)
            fig.update_layout(width=1200, height=600)
            st.header("Distribution of height")
            st.plotly_chart(fig)

            weight = athlete_df['Weight'].dropna()
            weight_gold = athlete_df[athlete_df['Medal'] == 'Gold']['Weight'].dropna()
            weight_silver = athlete_df[athlete_df['Medal'] == 'Silver']['Weight'].dropna()
            weight_bronze = athlete_df[athlete_df['Medal'] == 'Bronze']['Weight'].dropna()

            fig = ff.create_distplot([weight, weight_gold, weight_silver, weight_bronze],
                                     ['Overall weight', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                                     show_hist=False, show_rug=False)
            fig.update_layout(width=1200, height=600)
            st.header("Distribution of weight")
            st.plotly_chart(fig)



if index == "Insights":
    st.markdown("<h2 style='text-align: center; color:#f03557;'>Comparison between Summer and Winter Olympics</h2>", unsafe_allow_html=True)
    st.write(" ")
    st.write(" ")

    st.subheader("Number of athletes over years in summer and winter olympics")
    athlete_year = helper.athlete_overtime(df)
    athlete_year2 = helper.athlete_overtime(wdf)
    figure = make_subplots(rows=1, cols=2)

    figure.add_trace(
        go.Scatter(x=athlete_year["Edition"], y=athlete_year["No of athletes"]),
        row=1, col=1
    )

    figure.add_trace(
        go.Scatter(x=athlete_year2["Edition"], y=athlete_year2["No of athletes"]),
        row=1, col=2
    )

    figure = figure.update_layout(height=600, width=1200)
    st.plotly_chart(figure)


    st.subheader("Number of participating countries over years in summer and winter olympics")
    nations_year = helper.participating_nations_overtime(df)
    nations_year2 = helper.participating_nations_overtime(wdf)

    sports_year = helper.sports_overtime(df)
    sports_year2 = helper.sports_overtime(wdf)

    events_year = helper.events_overtime(df)
    events_year2 = helper.events_overtime(wdf)

    athlete_year = helper.athlete_overtime(df)
    athlete_year2 = helper.athlete_overtime(wdf)


    figure = make_subplots(rows=1, cols=2)

    figure.add_trace(
        go.Scatter(x=nations_year["Edition"], y=nations_year["No of countries"]),
        row=1, col=1
    )

    figure.add_trace(
        go.Scatter(x=nations_year2["Edition"], y=nations_year2["No of countries"]),
        row=1, col=2
    )

    figure = figure.update_layout(height=600, width=1200)
    st.plotly_chart(figure)

    st.subheader("Number of sports over years in summer and winter olympics")
    sports_year = helper.sports_overtime(df)
    sports_year2 = helper.sports_overtime(wdf)
    figure = make_subplots(rows=1, cols=2)

    figure.add_trace(
        go.Scatter(x=sports_year["Edition"], y=sports_year["No of sports"]),
        row=1, col=1
    )

    figure.add_trace(
        go.Scatter(x=sports_year2["Edition"], y=sports_year2["No of sports"]),
        row=1, col=2
    )

    figure = figure.update_layout(height=600, width=1200)
    st.plotly_chart(figure)

    st.subheader("Number of events over years in summer and winter olympics")
    events_year = helper.events_overtime(df)
    events_year2 = helper.events_overtime(wdf)
    figure = make_subplots(rows=1, cols=2)

    figure.add_trace(
        go.Scatter(x=events_year["Edition"], y=events_year["No of events"]),
        row=1, col=1
    )

    figure.add_trace(
        go.Scatter(x=events_year2["Edition"], y=events_year2["No of events"]),
        row=1, col=2
    )

    figure = figure.update_layout(height=600, width=1200)
    st.plotly_chart(figure)




    st.header("Key Insights")
    st.write("1.Summer Olympics attract more than 4 times athlete participation than Winter Olympics.")
    st.write("2.Growth in the number of athletes in Summer Olympics have become stagnant in the recent games.")
    st.write("3.34 sports competitions is the maximum in a summer olympic game.")
    st.write("4.Number of events have come to a saturation point in the last 5 summer games.")
    st.write("5.Number of events have come to a saturation point in the last 5 summer games.")
    st.write("6.1916, 1940 & 1944 summer Olympic games and 1940 & 1944 winter Olympic games didn't happen due to the world wars. Neither of the world war breaks affected the athlete participation in the succeeding years.")
    st.write("7.The number of athletes, events, and nations has grown dramatically since 1896, but growth leveled off around 2000 for the Summer Games")
    st.write("8.The Art Competitions were included from 1912 to 1948, and were dominated by Germany, France, and Italy. Nazi Germany was especially dominant in the 1936 Games.")
    st.write("9.Athletics and Swimming are the sports which has the maximum number of events")
    st.write("10.Only the first edition of Olympics didn't have any female athletes. There has been a great improvement in female representation ever since. Late 1950s and late 1980s saw significant increase in female representation.")
    st.write("11.Female participation increased dramatically, and this trend started during the Cold War.")

if index == "Contact":
    st.markdown("<h2 style='text-align: center; color:#f03557;'>Suggestions and Comments</h2>", unsafe_allow_html=True)
    first_name, last_name = st.columns(2)
    first_name.text_input("Enter First Name:", placeholder="First Name")
    last_name.text_input("Enter last Name:", placeholder="Last Name")

    email, number = st.columns([3, 1])
    email.text_input("Enter Email Address:", placeholder="Email Address")
    number.text_input("Enter Mobile number:", placeholder="Mobile Number")

    st.text_area("Suggestions", placeholder="Put your valuable Suggestions here...")
    columns = st.columns((2, 1, 2))
    button_pressed = columns[1].button('Submit')


    if button_pressed:
        st.markdown("<h2 style='text-align: center; color:green;'>Received Your valuable Suggestions and comments</h2>",
                    unsafe_allow_html=True)
        st.balloons()
