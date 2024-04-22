import streamlit as st
import pandas as pd
import numpy as np
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
import pydeck as pdk

path = 'RainDaily_Tabular.csv'

@st.cache_data
def load_data():
    data = pd.read_csv(path)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    return data

data = load_data()
provinces = data['province'].unique()
data['date'] = pd.to_datetime(data['date'])

st.title('Rainfall Data Analysis')
st.sidebar.header('Sidebar Controls')
province = st.sidebar.selectbox('Select Province', provinces, index=None)
start_date = st.sidebar.date_input('Select Start Date', min_value=data['date'].min(), max_value=data['date'].max(), value=data['date'].min())
end_date = st.sidebar.date_input('Select End Date', min_value=start_date, max_value=data['date'].max(), value=data['date'].max())

filtered_data = data[data['province'] == province] if province is not None else data
filtered_by_date_data = data[(data['date'] <= pd.to_datetime(end_date)) & (data['date'] >= pd.to_datetime(start_date))]

st.write('Average Rain Data in Each Province between', start_date, 'and', end_date)
st.bar_chart(filtered_by_date_data.groupby('province')['rain'].mean())

if province == None :
    st.write('Average Rain Data in Each Date of All Provinces')
    st.bar_chart(filtered_data.groupby('date')['rain'].mean())
else :
    st.write('Average Rain Data in Each Date of', province)
    st.bar_chart(filtered_data.groupby('date')['rain'].mean())

heatmap_data = filtered_by_date_data.groupby(['latitude', 'longitude'])['rain'].sum().reset_index()

st.write('Rainfall Heatmap in Thailand between',start_date, 'and', end_date)

color_range = [
    [0, 0, 128, 128],  
    [0, 0, 255, 255]
]

layer = pdk.Layer(
    'HeatmapLayer',
    data=heatmap_data,
    get_position=['longitude', 'latitude'],
    auto_highlight=True,
    get_weight='rain',  
    opacity=0.8,
    radius_scale=20,
    elevation_scale=5,
    elevation_range=[0, 1000],
    pickable=True,
    color_range=color_range
)

view_state = pdk.ViewState(
    latitude=13.736717,
    longitude=100.523186,
    zoom=6,
    min_zoom=5,
    max_zoom=15,
)

deck = pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=view_state,
    layers=[layer]
)

st.pydeck_chart(deck)

st.write('Summary of Analysis')
highest_province = data.groupby('province')['rain'].mean().idxmax()
highest_date = data.groupby('date')['rain'].mean().idxmax()
st.write('From the chart, we can see that the average rainfall between', start_date, 'and', end_date, 'in', highest_province ,'is the highest among all provinces. And the average rainfall of all is the highest on', highest_date)

st.header("Source Code")
file = "6430246621_assignment.py"
with open(file, "r") as f:
    code = f.read()
st.code(code, language="python")
