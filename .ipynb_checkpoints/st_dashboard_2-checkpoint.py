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
    st.markdown('CitiBike is a bike sharing/rental system located in New York City. Throughout the city are many bike stations that people can walk up to and rent out a bike for the day, and afterwards they can return the bike to any of the stations.')
    st.markdown('CitiBike is having a lot of issues with the disribution of bikes across its many stations, with some of them ether being empty or overstocked with bikes.')
    st.markdown('The objective of this analysis is to find any possible explanations for why this is happening, and making recommendations to fix it.')
    st.markdown("To do this I'll be going through the data CitiBike has on each trip that was taken during 2022 with these questions as my research starting points.")
    st.markdown('- Does weather have an effect on the number of trips?')
    st.markdown('- What are the most popular starting stations?')
    st.markdown('- What are the most common bike trips?')
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
    st.markdown('We can see from this graph that the daily temprature and the number of bike trips are directly correlated with each other. People are more likely to go outside, and ride one of our bikes, during warmer wether in order to enjoy the nice day.')
    st.markdown('From this we can conclude that bikes will be used a lot more during the summer, when the demand for bikes is at its highest. And during the winter, when demand is at its lowest, there would be a lot less bikes being used')

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
    st.markdown('This bar chart shows the 20 most frequented starting stations, with all of them having been used over 85,000 times in one year. That averages out to having over 230 users each day for each of those 20 station.')
    st.markdown('The most frequented starting station is W 21 St/6 Ave, with its total number of trips during 2022 being 129,000. This averages out to having over 350 users each day.')
    st.markdown('With the immense amount of people using these more popular stations, the chances of these stations losing there supply of bikes throughout the day and being compleatly empty when more people show up are very high.')

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
    st.markdown("This map has been filtered to only show the bike trips that have been used over 3,000 times. At a glance there's no obvious pattern to where these common trips are located.")
    st.markdown('Even though there are no specific landmarks, or geographic trait that draw people in, we can see from this map that there are many dense clusters of bike trips that are only distributed between a few stations.')
    st.markdown('Also, the most common trip between two different stations starts at the most frequented starting stations we looked at earlier, W 21 St/6 Ave.')
    st.markdown('These dense clusters of trips have a high volume of users that can quickly drain the supply of bikes from the nearby stations.')

################################## Recommendations ######################################################################

else:

    st.header('Conclusions and recommendations')
    bikes = Image.open('Citi Bikes2.webp')  #source: https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.groupon.com%2Fdeals%2Fciti-bike&psig=AOvVaw2GYf1GYjDl4o6t-vBBJiAc&ust=1745878036105000&source=images&cd=vfe&opi=89978449&ved=0CBQQjRxqFwoTCICH0Yed-YwDFQAAAAAdAAAAABAK
    st.image(bikes)
    st.markdown('### From this analysis I have 3 recommendations for what CitiBikes can do moving forward:')
    st.markdown('- Adding 1 or 2 new bike stations in locations with a dense amount of trips, and by the most used starting stations, will provide more bikes to areas with high amounts of user activity.')
    st.markdown('- Make sure that these more popular stations are fully stocked during the summer to keep up with demand, and reduce the number of available bikes by 40% or 50% during the winter to prevent the stations from being congested with unused bikes.')
    st.markdown('- Conducting a further analysis on both starting and ending stations to see which stations are gaining more bikes, or losing more bikes throughout the day. This info can help determin which stations are in need for more bikes in there givin area.')
