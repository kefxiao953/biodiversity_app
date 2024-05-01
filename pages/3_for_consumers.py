import folium
from folium import plugins
import geopandas as gpd
import json
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from streamlit_folium import folium_static, st_folium
from streamlit_extras.switch_page_button import switch_page
from functions import *

st.title("Explore corporate sustainability + biodiversity impacts")
text = """
The growth of corporate sustainability has the potential to help reverse species loss.  
But how can we assess corporate commitments and their actual impact on biodiversity conservation?  
We hope that providing this information on companies with sustainability initiatives will better inform  
consumers and help people support businesses with a visible positive impact. 

"""
st.markdown(text)

# don't forget to add pictures of bird - maybe some from inaturalist to plug community science




st.title("Current Predicted Range")

# Open the raster file to find bounds
with rasterio.open("outputs/rf-images_bird/probability_1.0.tif") as src:
    bounds = src.bounds
    crs = src.crs

# Assuming your map's initial focus point and zoom level
m = folium.Map(location=[5, -7], zoom_start=7)

# geojson for Cavally
coordinates = [
    [-8.62, 6.52],
    [-7.90, 6.97],
    [-7.07,5.68],
    [-7.42, 5.63 ]
    
]

geojson = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [coordinates]
            }
        }
    ]
}
# Add outline to map
folium.GeoJson(geojson, name="Cavally Forest").add_to(m)


# Add the image overlay
folium.raster_layers.ImageOverlay(
    image='outputs/distr_averaged_bird.png',
    bounds=[[bounds.bottom, bounds.left], [bounds.top, bounds.right]],
    opacity=0.6,
    interactive=True,
    cross_origin=False,
    zindex=1,
).add_to(m)
st_folium(m, width=725, height=500)


st.title("Predicted Range - 2050")
# Open the raster file to find bounds
with rasterio.open("outputs/rf-images_bird_2050/probability_1.0.tif") as src:
    bounds = src.bounds
    crs = src.crs

# Assuming your map's initial focus point and zoom level
m = folium.Map(location=[5, -7], zoom_start=7)
# geojson for Cavally
coordinates = [
    [-8.62, 6.52],
    [-7.90, 6.97],
    [-7.07,5.68],
    [-7.42, 5.63 ]
    
]

geojson = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [coordinates]
            }
        }
    ]
}
# Add outline to map
folium.GeoJson(geojson, name="Cavally Forest").add_to(m)

# Add the image overlay
folium.raster_layers.ImageOverlay(
    image='outputs/distr_averaged_bird_2050.png',
    bounds=[[bounds.bottom, bounds.left], [bounds.top, bounds.right]],
    opacity=0.6,
    interactive=True,
    cross_origin=False,
    zindex=1,
).add_to(m)

st_folium(m, width=725, height=500)