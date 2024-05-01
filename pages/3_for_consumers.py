import folium
from folium import plugins
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from streamlit_folium import folium_static, st_folium
from streamlit_extras.switch_page_button import switch_page

st.title("Explore corporate sustainability + biodiversity impacts")
text = """
The growth of corporate sustainability has the potential to help reverse species loss.  
But how can we assess corporate commitments and their actual impact on biodiversity conservation?  
We hope that providing this information on companies with sustainability initiatives will better inform  
consumers and help people support businesses with a visible positive impact. 

"""
st.markdown(text)

# don't forget to add pictures of bird - maybe some from inaturalist to plug community science











# # Creating geodataframe
# df = pd.read_csv('data/bats.tsv', sep='\t')
# df = df[["decimalLatitude", "decimalLongitude"]]
# geometry = gpd.points_from_xy(df.decimalLongitude, df.decimalLatitude)
# gdf = gpd.GeoDataFrame(df, geometry=geometry)

# # Heatmap
# heatmap = folium.Map(
#     location = [0.75,-74],
#     zoom_start = 7
#       )

# heat_data = [[point.xy[1][0], point.xy[0][0]] for point in gdf.geometry ]
# plugins.HeatMap(heat_data).add_to(heatmap)



# st_folium(heatmap, width=725, height=500)