import streamlit as st
from functions import *
import pickle

st.title("Welcome, BrightSource Energy")

st.divider()

st.subheader("Details on your project: Ivanpah Solar Field")

m = folium.Map(location=[35, -115.3959], zoom_start=8)
folium.Marker(
    location=[35, -115],
    popup='Ivanpah Solar Field',
    icon=folium.Icon(color='red')
).add_to(m)

st_folium(m, width=725, height=500)

st.header("Review sensitive species at this site:")
species = st.selectbox("Species: Desert Tortoise",
   ["Gopherus agassizii (Cooper, 1861)"],
   placeholder="Select species...",
)


# load data into session state
load_data()
stdf = st.session_state.df_tortise

coords = stdf[['decimalLatitude', 'decimalLongitude']]
coords_unique = coords.drop_duplicates()

# Initialize session state variables
if 'previous_species' not in st.session_state:
    st.session_state.previous_species = ""
if 'df' not in st.session_state:
    st.session_state.df = []

if species:  # Check if the input is not empty
    # Show a loading spinner while data is being fetched
    with st.spinner('Loading data...'):
        if species != st.session_state.previous_species:
            # Fetch data only if the species has changed
            st.session_state.df = gbif_data(species)
            st.session_state.previous_species = species

        # Columns to show in df
        columns_to_display = ['occurrenceStatus',
                              'iucnRedListCategory', 'eventDate',
                              'decimalLatitude', 'decimalLongitude',
                              'lifeStage', 'sex']
        # Display data
        st.dataframe(st.session_state.df[columns_to_display])
        
else:
    # Prompt for input if it is empty
    st.write("Please select a scientific name to search.")


st.title("Predicted Range")

# Load the raster data
distr_rf = load_raster_data("outputs/rf-images/probability_1.0.tif")
distr_et = load_raster_data("outputs/et-images/probability_1.0.tif")
distr_xgb = load_raster_data("outputs/xgb-images/probability_1.tif")

# Calculate the averaged distribution
distr_averaged = (distr_rf + distr_et + distr_xgb) / 3

colormap = linear.YlGnBu_09.scale(0, distr_averaged.max())
colormap.caption = 'Probability Distribution'

st.markdown("<h3 style='text-align: left;'>Desert Tortoise Predicted Range- Current</h3>",
            unsafe_allow_html=True)
create_folium_map(colormap)

# Map caption
caption = """
<small style='font-size: 12px;'>The area outlined in red represents your project site</small>    
<small style='font-size: 12px;'>The color bar indicates the probability that a tortoise is found in that area.</small>   
<small style='font-size: 12px;'>The resolution is 4.5km.</small>
"""
st.markdown(caption, unsafe_allow_html=True)

text = """
**SUMMARY**  
This project has high probability (>70%) of overlap with sensitive habitat for the desert tortoise.   
Mitigation is expected to cost:  
__USD 801/acre* at 4000 acres__,   
totalling __USD 3.2 million__.  

The emission reduction impact of this species is estimated to be:   
**7.8 megatons (7.8 million metric tons)***.  
The total solar output required to mitigate this carbon impact would need to equal:  
**the electricity use of 197,356 homes for one year**. 
        """
st.markdown(text)

reference = """
    <small style='font-size: 9px;'>https://www.wecc.org/Reliability/2013_Mitigation_Cost_Study_FinalReport_EDTF.pdf</small>  
    <small style='font-size: 9px;'>https://legal-planet.org/2021/07/01/the-extinction-cost-of-carbon/</small>  
    <small style='font-size: 9px;'>https://www.epa.gov/energy/greenhouse-gas-equivalencies-calculator#results</small>

    """

st.markdown(reference, unsafe_allow_html=True)

st.title("Predicted Range - 2050")

# Open the raster file to find bounds
with rasterio.open("outputs/rf-images_tortoise_2050/probability_1.0.tif") as src:
    bounds = src.bounds
    crs = src.crs

m = folium.Map(location=[35.5, -115.5], zoom_start=9.5)

# Add the image overlay
folium.raster_layers.ImageOverlay(
    image='outputs/distr_averaged_tortoise_2050.png',
    bounds=[[bounds.bottom, bounds.left], [bounds.top, bounds.right]],
    opacity=0.6,
    interactive=True,
    cross_origin=False,
    zindex=1,
).add_to(m)

# Solar field polygon vertices
coordinates = [
[35.59, -115.50],
[35.599, -115.41],
[35.52, -115.48]
]

# Create polygon and add it to the map
folium.vector_layers.Polygon(
    locations=coordinates,  # List of coordinates
    color='red'          # Color of the polygon's border
).add_to(m)


# Add colormap
colormap.add_to(m)

st_folium(m, width=725, height=500)

caption = """
<small style='font-size: 12px;'>The area outlined in red represents your project site</small>    
<small style='font-size: 12px;'>The color bar indicates the probability that a tortoise is found in that area.</small>   
<small style='font-size: 12px;'>The resolution is 4.5km.</small>
"""
st.markdown(caption, unsafe_allow_html=True)

text2 = """
**SUMMARY**  
This project has low projected probability (<20%) of overlap with habitat for the desert tortoise in 2050.     
Areas of the __Kingston Range Wilderness & Mojave National Preserve__  
should be prioritized for tortoise relocation mitigation efforts.   
        """
st.markdown(text2)
