import folium
from folium import plugins
import geopandas as gpd
import json
import time
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from streamlit_folium import folium_static, st_folium
from streamlit_extras.switch_page_button import switch_page
from functions import *

# Function to add the raster image to the map
# configure page
st.set_page_config(
    page_title="Biopraedico",
    page_icon=":recycle:",
    layout="wide"
)


def add_raster_layer(map_obj, image_path, rasterio_file):
    with rasterio.open(rasterio_file) as src:
        bounds = src.bounds

    folium.raster_layers.ImageOverlay(
        image=image_path,
        bounds=[[bounds.bottom, bounds.left], [bounds.top, bounds.right]],
        opacity=0.6,
        interactive=True,
        cross_origin=False,
        zindex=1,
    ).add_to(map_obj)

# Function to add geojson coordinates to the map


def add_geojson_layer(map_obj, company):
    # Base coordinates for Nestle
    base_coordinates = {
        "Nestle": [
            [-8.62, 6.52],
            [-7.90, 6.97],
            [-7.07, 5.68],
            [-7.42, 5.63]
        ],
        "Unilever": [
            [-8.55, 4.99],
            [-8.09, 4.65],
            [-8.05, 5.26],
            [-8.20, 5.51]
        ],
        "IKEA": [
            [-7.87, 4.74],
            [-6.91, 4.99],
            [-6.96, 5.24],
            [-7.61, 5.43]
        ],
        "Nike": [
            [-6.40, 5.05],
            [-5.31, 5.85],
            [-5.74, 6.60],
            [-6.25, 6.57]
        ]
    }

    # Define the GeoJSON structure
    geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [base_coordinates[company]]
                }
            }
        ]
    }

    # Define a function to apply style
    def style_function(feature):
        return {
            'color': 'red',  # Outline color
            'fillColor': 'none',
            'fillOpacity': 0,
            'weight': 3,
        }

    # Add the GeoJSON to the map
    folium.GeoJson(geojson, name=f"{company} Area",
                   style_function=style_function).add_to(map_obj)

# Initialize map


def create_map():
    return folium.Map(location=[5, -7], zoom_start=7)


def load_data():
    time.sleep(3)  # Delays for 3 seconds
    return "Data loaded successfully!"


##############################################################

st.title("Explore corporate sustainability + biodiversity impacts")
text = """
The growth of corporate sustainability has the potential to help reverse species loss.  
How can we assess corporate commitments and their actual impact on biodiversity conservation?  
We hope that providing this information on companies with sustainability initiatives will better inform  
consumers and help people support businesses with a visible positive impact. 

"""

st.markdown(text)


# Custom styling
st.markdown("""
<style>
    /* CSS for larger radio buttons */
    div.row-widget.stRadio > div {
        flex-direction: row;
    }
    label.css-1bs6k5e.e1fqkh3o1 {
        padding-right: 20px;
    }
    /* Styling for markdown headers */
    h1, h2 {
        text-align: center;
    }
    /* Image border and spacing */
    .stImage > img {
        border: 2px solid #0099ff;  /* Blue border for images */
        border-radius: 5px;  /* Rounded borders */
        padding: 5px;  /* Padding around images */
    }
</style>
""", unsafe_allow_html=True)

# Layout: three columns for images
col1, col2, col3 = st.columns(3)

# Display images with titles
with col1:
    st.markdown("# Blue-headed Wood-Dove \n ## (Turtur brehmeri)")
    st.image('images/bird1.png', use_column_width=True)

with col2:
    st.markdown("# Timneh African Grey Parrot \n ## (Psittacus timneh)")
    st.image('images/bird2.png', use_column_width=True)

with col3:
    st.markdown("# Finsch's Flycatcher Thrush \n ## (Stizorhina finschi)")
    st.image('images/bird3.png', use_column_width=True)

# Radio button selection below images for better visual flow
bird_selection = st.radio("Select for details", [
                          "Bird 1 - Blue-headed Wood-Dove", "Bird 2 - Timneh Parrot", "Bird 3 - Finsch's Flycatcher Thrush"], key='bird_selection')


# Logic to display details based on radio button selection
if bird_selection == "Bird 1 - Blue-headed Wood-Dove":

    unique_species = pd.read_csv('data/nestle_unique_endangered_species.csv')

    # Write the count to the Streamlit app
    st.write(f"Count of Blue-headed Wood-Dove (Turtur brehmeri): 427")

    companies = ["Unilever", "IKEA", "Nestle", "Nike"]

    # Create a select box for company selection

    unique_species_count = len(unique_species)
    endangered_species_count = sum(unique_species['count'])

    st.markdown("""
        ## 🌍 Biodiversity Dashboard
        """, unsafe_allow_html=True)

    st.markdown(f"""
        ### 🔎 Unique Endangered Species
        **Number of Unique Endangered Species:** {unique_species_count}
        """, unsafe_allow_html=True)

    st.markdown(f"""
        ### 🚨 Total Endangered Species
        **Total Number of Endangered Species:** {endangered_species_count}
        """, unsafe_allow_html=True)

    st.title("Forecasted Predicted Range")

    # Selection for layers using radio buttons
    layer_options = ['None', 'Endangered Species Distribution', 'Company Commitment Area']

    selected_company = st.selectbox("Select a Company:", companies)
    selected_option = st.radio(
        'First select Endangered Species Distribution to view forecast. Then select Company Commitment Area to view the area of company investment.', layer_options)
    generated_predicted = st.checkbox("Run Predicted Range - 2050")

    col1, col2 = st.columns(2)

    with col1:
        st.title("Current Range")
        st.success('Data loaded!')
        if selected_company == "Nestle":
            # Assume unique_species is already defined and loaded with data
            m = create_map()

            # Logic to display layers based on the radio button selection
            if selected_option == 'Endangered Species Distribution':
                add_raster_layer(m, rasterio_file="outputs/rf-images_bird/probability_1.0.tif",
                                 image_path='outputs/distr_averaged_bird.png')
                distr_rf = load_raster_data("outputs/rf-images_bird/probability_1.0.tif")
                colormap = linear.YlGnBu_09.scale(0, distr_rf.max())
                colormap.caption = 'Probability Distribution'
                colormap.add_to(m)
            elif selected_option == 'Company Commitment Area':
                add_raster_layer(m, rasterio_file="outputs/rf-images_bird/probability_1.0.tif",
                                 image_path='outputs/distr_averaged_bird.png')
                add_geojson_layer(m, company=selected_company)
                distr_rf = load_raster_data("outputs/rf-images_bird/probability_1.0.tif")
                colormap = linear.YlGnBu_09.scale(0, distr_rf.max())
                colormap.caption = 'Probability Distribution'
                colormap.add_to(m)

            # Render the map
            st_folium(m, width=725, height=500, key=selected_company)
            caption = """
            <small style='font-size: 12px;'>The area outlined in red represents a project site. (Click Company Commitment Area button to view this.)</small>    
            <small style='font-size: 12px;'>The color bar indicates the probability that the selected species is found in that area.</small>   
            <small style='font-size: 12px;'>The resolution is 4.5km.</small>
            """
            st.markdown(caption, unsafe_allow_html=True)

        if selected_company == "Unilever":
            # Assume unique_species is already defined and loaded with data
            m = create_map()

            # Logic to display layers based on the radio button selection
            if selected_option == 'Endangered Species Distribution':
                add_raster_layer(m, rasterio_file="outputs/rf-images_bird/probability_1.0.tif",
                                 image_path='outputs/distr_averaged_bird.png')
                distr_rf = load_raster_data("outputs/rf-images_bird/probability_1.0.tif")
                colormap = linear.YlGnBu_09.scale(0, distr_rf.max())
                colormap.caption = 'Probability Distribution'
                colormap.add_to(m)
            elif selected_option == 'Company Commitment Area':
                add_raster_layer(m, rasterio_file="outputs/rf-images_bird/probability_1.0.tif",
                                 image_path='outputs/distr_averaged_bird.png')
                add_geojson_layer(m, company=selected_company)
                distr_rf = load_raster_data("outputs/rf-images_bird/probability_1.0.tif")
                colormap = linear.YlGnBu_09.scale(0, distr_rf.max())
                colormap.caption = 'Probability Distribution'
                colormap.add_to(m)
                
            # Render the map
            st_folium(m, width=725, height=500, key=selected_company)
            
            caption = """
            <small style='font-size: 12px;'>The area outlined in red represents a project site. (Click Company Commitment Area button to view this.)</small>    
            <small style='font-size: 12px;'>The color bar indicates the probability that the selected species is found in that area.</small>   
            <small style='font-size: 12px;'>The resolution is 4.5km.</small>
            """
            st.markdown(caption, unsafe_allow_html=True)

        if selected_company == "Nike":
            # Assume unique_species is already defined and loaded with data
            m = create_map()

            # Logic to display layers based on the radio button selection
            if selected_option == 'Endangered Species Distribution':
                add_raster_layer(m, rasterio_file="outputs/rf-images_bird/probability_1.0.tif",
                                 image_path='outputs/distr_averaged_bird.png')
            elif selected_option == 'Company Commitment Area':
                add_raster_layer(m, rasterio_file="outputs/rf-images_bird/probability_1.0.tif",
                                 image_path='outputs/distr_averaged_bird.png')
                add_geojson_layer(m, company=selected_company)

            # Render the map
            st_folium(m, width=725, height=500, key=selected_company)
            caption = """
            <small style='font-size: 12px;'>The area outlined in red represents a project site. (Click Company Commitment Area button to view this.)</small>    
            <small style='font-size: 12px;'>The color bar indicates the probability that the selected species is found in that area.</small>   
            <small style='font-size: 12px;'>The resolution is 4.5km.</small>
            """
            st.markdown(caption, unsafe_allow_html=True)

        if selected_company == "IKEA":
            # Assume unique_species is already defined and loaded with data
            m = create_map()

            # Logic to display layers based on the radio button selection
            if selected_option == 'Endangered Species Distribution':
                add_raster_layer(m, rasterio_file="outputs/rf-images_bird/probability_1.0.tif",
                                 image_path='outputs/distr_averaged_bird.png')
            elif selected_option == 'Company Commitment Area':
                add_raster_layer(m, rasterio_file="outputs/rf-images_bird/probability_1.0.tif",
                                 image_path='outputs/distr_averaged_bird.png')
                add_geojson_layer(m, company=selected_company)

            # Render the map
            st_folium(m, width=725, height=500, key=selected_company)
            caption = """
            <small style='font-size: 12px;'>The area outlined in red represents a project site. (Click Company Commitment Area button to view this.)</small>    
            <small style='font-size: 12px;'>The color bar indicates the probability that the selected species is found in that area.</small>   
            <small style='font-size: 12px;'>The resolution is 4.5km.</small>
            """
            st.markdown(caption, unsafe_allow_html=True)

    with col2:

        if generated_predicted:
            # Show a spinner while loading data

            st.title("Predicted Range - 2050")
            # Display the data after loading
            with st.spinner('Loading data... Please wait.'):
                data = load_data()
            st.success('Data loaded!')

            # Open the raster file to find bounds

            rasterio_2050 = "outputs/rf-images_bird_2050/probability_1.0.tif"
            image_path_2050 = 'outputs/distr_averaged_bird_2050.png'
            m = create_map()

            # Logic to display layers based on the radio button selection
            if selected_option == 'Endangered Species Distribution':
                add_raster_layer(m, rasterio_file=rasterio_2050,
                                 image_path=image_path_2050)
                distr_rf = load_raster_data("outputs/rf-images_bird_2050/probability_1.0.tif")
                colormap = linear.YlGnBu_09.scale(0, distr_rf.max())
                colormap.caption = 'Probability Distribution'
                colormap.add_to(m)
            elif selected_option == 'Company Commitment Area':
                add_raster_layer(m, rasterio_file=rasterio_2050,
                                 image_path=image_path_2050)
                add_geojson_layer(m, company=selected_company)
                distr_rf = load_raster_data("outputs/rf-images_bird_2050/probability_1.0.tif")
                colormap = linear.YlGnBu_09.scale(0, distr_rf.max())
                colormap.caption = 'Probability Distribution'
                colormap.add_to(m)

            # Render the map
            st_folium(m, width=725, height=500, key="IKEA_2050")
            caption = """
            <small style='font-size: 12px;'>The area outlined in red represents a project site. (Click Company Commitment Area button to view this.)</small>    
            <small style='font-size: 12px;'>The color bar indicates the probability that the selected species is found in that area.</small>   
            <small style='font-size: 12px;'>The resolution is 4.5km.</small>
            """
            st.markdown(caption, unsafe_allow_html=True)
