###################################### New York Bike Ride Dashboard #####################################################

import streamlit as st
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from streamlit_keplergl import keplergl_static
from keplergl import KeplerGl
from datetime import datetime as dt
from PIL import Image

################################## Initial settings for the dashboard ###################################################

st.set_page_config(page_title = 'New York CitiBike Strategy Dashboard', layout='wide')
st.title('New York CitiBike Strategy Dashboard')

# Define side bar
st.sidebar.title("Aspect Selector")
page = st.sidebar.selectbox('Select an aspect of the analysis',
  ["Intro page","Weather component and bike usage",
   "Most popular stations",
    "Interactive map with aggregated bike trips", "Recommendations"])

################################## Importing data #######################################################################

df = pd.read_csv('dual-axis.csv', index_col = 0)
top20 = pd.read_csv('top20.csv', index_col = 0)

################################## Intro Page ###########################################################################

if page == 'Intro page':
    st.markdown('## Where are all the bikes?')
    st.markdown('CitiBike is having a lot of issues with the disribution of its bikes across New York City. This analysis aims to find any possible explanation for this, and how to fix it.')
    st.markdown('- Weather component and bike usage')
    st.markdown('- Most popular stations')
    st.markdown('- Interactive map with aggregated bike trips')
    st.markdown('- Recommendations')
    st.markdown("The dropdown menu on the left 'Aspect Selector' will take you to the different aspects of the analysis our team looked at.")
    myImage = Image.open('Citi Bikes.jpg') #source: https://www.google.com/url?sa=i&url=https%3A%2F%2Fny1.com%2Fnyc%2Fall-boroughs%2Ftransit%2F2024%2F01%2F03%2Fciti-bike-price-increases-to-start-taking-effect-thursday&psig=AOvVaw2GYf1GYjDl4o6t-vBBJiAc&ust=1745878036105000&source=images&cd=vfe&opi=89978449&ved=0CBQQjRxqFwoTCICH0Yed-YwDFQAAAAAdAAAAABAE
    st.image(myImage)

################################## Line Chart ###########################################################################

elif page == 'Weather component and bike usage':

    fig_2 = make_subplots(specs = [[{"secondary_y": True}]])

    fig_2.add_trace(
    go.Scatter(x = df['date'], y = df['daily_bike_rides'], name = 'Daily bike rides',
    marker = {'color' : df['daily_bike_rides'], 'color' : 'blue'}),
    secondary_y = False
    )

    fig_2.add_trace(
    go.Scatter(x=df['date'], y = df['avgTemp'], name = 'Daily temperature',
    marker = {'color' : df['avgTemp'], 'color' : 'red'}),
    secondary_y=True
    )

    fig_2.update_layout(
    title = 'Daily bike rides and temperatures in New York City 2022',
    height = 400
    )

    st.plotly_chart(fig_2, use_container_width=True)
    st.markdown('We can see from this graph that the daily temprature and the number of riders are directly correlated with each other. People are more likely to go outside, and ride one of our bikes, during warmer wether in order to enjoy the nice day. From this we can conclude that the disribution issues peak during the summer.')

################################## Bar Chart ############################################################################

elif page == 'Most popular stations':

    fig = go.Figure(go.Bar(x = top20['start_station_name'], y = top20['value'], marker={'color': top20['value'],'colorscale': 'Blues'}))
    fig.update_layout(
    title = 'Top 20 most popular bike stations in New York City',
    yaxis_title ='Sum of trips',
    xaxis_title = 'Start stations',
    width = 900, height = 600
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("From this bar chart it's easy to see that the top 5 starting stations are way more popular than the other stations, with all the top 5 stations being used over 100,000 time in one year. The gaps between the top 4 stations are also massive, with increases around 8,000 users, and the most popular starting station, W 21 St & 6 Ave, almost totaling 130,000 users. These are major hot spots that we need to pay attention to.")

################################## Adding Map ###########################################################################

elif page == 'Interactive map with aggregated bike trips':

    path_to_html = "New York Bike Trips Aggregated.html" 

    # Read file and keep in variable
    with open(path_to_html,'r') as f: 
        f = open('New York Bike Trips Aggregated.html', encoding="utf8")
        html_data = f.read()

    ## Show in webpage
    st.header("Aggregated Bike Trips in New York City (Interactive map)")
    st.components.v1.html(html_data,height=1000)
    st.markdown("#### Using the filter on the left hand side of the map we can check the 5 most popular trips, and compare them with the most popular starting stations.")
    st.markdown('The top 2 starting stations from the bar chart, W 21 St/6 Ave and West St/Chambers St, show up again in this map. And W 21 St/6 Ave once again takes the top spot. Yet the other three popular trips have starting stations outside of the top 20 bar chart.')
    st.markdown("It's also important to note that in this filter, we see that the vast majority of trips start and end at the same location, and are spread throughout the city.")

################################## Recommendations ######################################################################

else:

    st.header('Conclusions and recommendations')
    bikes = Image.open('Citi Bikes2.webp')  #source: https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.groupon.com%2Fdeals%2Fciti-bike&psig=AOvVaw2GYf1GYjDl4o6t-vBBJiAc&ust=1745878036105000&source=images&cd=vfe&opi=89978449&ved=0CBQQjRxqFwoTCICH0Yed-YwDFQAAAAAdAAAAABAK
    st.image(bikes)
    st.markdown('### From this analysis I have 3 recommendations for what CitiBikes can do moving forward:')
    st.markdown('- Add more stations around the varius hot spot locations around the city, like W 21 St/6 Ave and West St/Chambers St')
    st.markdown('- Make sure that these more popular stations are fully stocked during the summer to keep up with demand, and reduce the number of bikes during the winter to provent the stations from being congested with unused bikes')
    st.markdown('- Conducting further analysis regarding frequented end stations, and finding the difference between a station being used as a starting point and an ending point of a trip')
