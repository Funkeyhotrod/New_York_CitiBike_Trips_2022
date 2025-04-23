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

################################## Initial settings for the dashboard ###################################################

st.set_page_config(page_title = 'New York CitiBike Strategy Dashboard', layout='wide')
st.title('New York CitiBike Strategy Dashboard')
st.markdown('CitiBike is having a lot of issues with the disribution of its bikes across New York City. This analysis aims to find any possible explanation for this, and how to fix it.')

################################## Importing data #######################################################################

df = pd.read_csv('dual-axis.csv', index_col = 0)
top20 = pd.read_csv('top20.csv', index_col = 0)

################################## Bar Chart ############################################################################

fig = go.Figure(go.Bar(x = top20['start_station_name'], y = top20['value'], marker={'color': top20['value'],'colorscale': 'Blues'}))
fig.update_layout(
    title = 'Top 20 most popular bike stations in New York City',
    xaxis_title = 'Start stations',
    yaxis_title ='Sum of trips',
    width = 1500, height = 1000
)
st.plotly_chart(fig, use_container_width=True)

################################## Line Chart ###########################################################################

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
    height = 800
)

st.plotly_chart(fig_2, use_container_width=True)

################################## Adding Map ###########################################################################

path_to_html = "New York Bike Trips Aggregated.html" 

# Read file and keep in variable
with open(path_to_html,'r') as f: 
    f = open('New York Bike Trips Aggregated.html', encoding="utf8")
    html_data = f.read()

## Show in webpage
st.header("Aggregated Bike Trips in New York City")
st.components.v1.html(html_data,height=1000)
