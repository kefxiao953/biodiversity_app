import folium
from folium import plugins
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from streamlit_folium import folium_static, st_folium
from streamlit_extras.switch_page_button import switch_page

# configure page
st.set_page_config(
    page_title="Biopraedico",
    page_icon=":recycle:",
    layout="wide"
)

st.header("Welcome to Biopraedico :crystal_ball:")
st.divider()
# st.markdown("<h1 style='text-align: center; color: black;'>Predict a Sustainable Future</h1>",
#             unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.write(' ')

with col2:
    st.image("intro.png", output_format='PNG', width=1000)

with col3:
    st.write(' ')

# with col1:
#     st.write(' ')

# with col2:
#     st.write("$125-140 trillion: Estimated value of ecosystem services in US dollars for 2019 ")

# with col3:
#     st.write(' ')

st.markdown("""
<h3 style='text-align: center; color: black;'>Biopraedico enables informed decisions around biodiversity impact. We are empowering everyone from investors
to conservation groups to everyday consumers to make decisions that advance sustainable development
while preserving biodiversity.</h3>""", unsafe_allow_html=True)

# st.markdown("<h2 style='text-align: center; color: green;'>$125-140 trillion</h2>", unsafe_allow_html=True)
# st.markdown("<h3 style='text-align: center; color: black;'>Estimated value of ecosystem services in US dollars for 2019</h3>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: green;'>Become a leader in advancing ecosystems and economies.</h3>", unsafe_allow_html=True)

with col2:
    demo = st.button("Request a Consultation")
    if demo:
        switch_page("pages/2_request_consult")
# st.markdown("""
# <h3 style='text-align: center; color: black;'>Biopraedico enables informed decisions around biodiversity impact. We are empowering everyone from investors
# to conservation groups to everyday consumers to make decisions that advance sustainable development
# while preserving ecosystems.</h3>""", unsafe_allow_html=True)

# text = '''
# Biopraedico enables informed decisions around biodiversity impact. We are empowering everyone from investors
# to conservation groups to everyday consumers to make decisions that advance sustainable development
# while preserving ecosystems.
# :handshake:. 
# '''
# st.markdown(text)
st.divider()

# maptext = """
# Bats can help measure forest health.  
# We have an extensive dataset of bats in Colombia, a major source of global coffee beans.  
# Explore the map or query our dataset to explore how bats and coffee influence ecosystem health.  
# **still in development**
# """
# Folium heatmap of available data so far
# st.markdown(maptext)

# Creating geodataframe
df = pd.read_csv('data/bats.tsv', sep='\t')
df = df[["decimalLatitude", "decimalLongitude"]]
geometry = gpd.points_from_xy(df.decimalLongitude, df.decimalLatitude)
gdf = gpd.GeoDataFrame(df, geometry=geometry)

# Heatmap
heatmap = folium.Map(
    location = [0.75,-74],
    zoom_start = 7
      )

heat_data = [[point.xy[1][0], point.xy[0][0]] for point in gdf.geometry ]
plugins.HeatMap(heat_data).add_to(heatmap)



st_folium(heatmap, width=725, height=500)


# Open the raster file

# file_path = os.path.expanduser(
#     "~/data/bio/inputs/cropped_bioclim_tortoise/wc2.1_2.5m_bio_1_band1.asc")


# cola, colb, colc = st.columns(3)
# with colb:
#     st.markdown("<h3 style='text-align: center;'>Cropped Raster Visualization</h3>",
#                 unsafe_allow_html=True)
#     visualize_raster(file_path)

col2, col3 = st.columns(2)

# with col2:
#     st.markdown("<h3 style='text-align: center;'>Map centered at the given coordinates with a red rectangle overlay</h3>",
#                 unsafe_allow_html=True)
#     create_map_with_rectangle(south, north, west, east)

# with col3:
#     st.markdown("<h3 style='text-align: center;'>Overlays a raster visualized as an image on a Folium map based on the raster bounds.</h3>",
#                 unsafe_allow_html=True)
#     create_folium_map_with_raster_overlay(file_path)


# Path to the bioclimatic variable raster
# raster_path = 'inputs/cropped_bioclim_tortoise/wc2.1_2.5m_bio_1_band1.asc'

# Number of presence points (in dataframe of occurrences)
# length_presences = len(coords_unique)

# # Sample background points
# background_points = sample_background_points(
#     raster_path, length_presences * 2, 1.25)

# # Rename columns to 'lon' and 'lat'
# background_points['decimalLongitude'] = background_points.geometry.x
# background_points['decimalLatitude'] = background_points.geometry.y

# # Create the training data by combining presence and background points
# train = pd.concat([coords_unique, background_points[[
#                   'decimalLongitude', 'decimalLatitude']]], ignore_index=True)

# Create presence-absence column
# pa_train = np.concatenate(
#     [np.ones(len(coords_unique)), np.zeros(len(background_points))])

# Final DataFrame
# train = pd.DataFrame(
#     {'CLASS': pa_train, 'lon': train['decimalLongitude'], 'lat': train['decimalLatitude']})

# train = train.sample(frac=1).reset_index(drop=True)

# # Extract the 'CLASS' column into a separate DataFrame and name the column
# class_pa = pd.DataFrame(train.iloc[:, 0])
# class_pa.columns = ['CLASS']

# Assuming 'train' has longitude in the 2nd column and latitude in the 3rd column
# Create the GeoDataFrame
# geometry = [Point(xy) for xy in zip(train.iloc[:, 1], train.iloc[:, 2])]
# data_map = gpd.GeoDataFrame(class_pa, geometry=geometry)

# data_map.crs = 'EPSG:4326'  # Directly setting EPSG code

# # Write to shapefile
# data_map.to_file('inputs/tortoise.shp', driver='ESRI Shapefile')

# Read shapefile as a geodataframe
# pa = gpd.GeoDataFrame.from_file("inputs/tortoise.shp")

# pa['longitude'] = pa.geometry.x
# pa['latitude'] = pa.geometry.y

# pa = pa[(pa['longitude'] >= -180) & (pa['longitude'] <= 180)]
# pa = pa[(pa['latitude'] >= -90) & (pa['latitude'] <= 90)]


# fig, ax = plt.subplots(figsize=(10, 10))
# world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
# world.plot(ax=ax, color='lightgrey')
# # Plotting your points in red for visibility
# pa.plot(ax=ax, marker='o', color='red', markersize=5)
# st.pyplot(fig)


# pa = pd.read_pickle('inputs/pa.pickle')
# pa = gpd.GeoDataFrame(pa)


# st.subheader('Using pyimpute to generate raster maps of suitability')

# raster_features = sorted(glob.glob(
#     'inputs/cropped_bioclim_tortoise/wc2*.asc'))

# # Split test and train
# train_xs, train_y = load_training_vector(
#     pa, raster_features, response_field='CLASS')
# target_xs, raster_info = load_targets(raster_features)
# # check shape, does it match the size above of the observations?
# train_xs.shape, train_y.shape

