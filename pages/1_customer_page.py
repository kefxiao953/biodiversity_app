import streamlit as st
from functions import *
import pickle

st.header("Welcome, BrightSource Energy")

st.divider()

st.subheader("Details on your project: Ivanpah Solar Field")

m = folium.Map(location=[35, -115.3959], zoom_start=8)
folium.Marker(
    location=[35, -115],
    popup='Ivanpah Solar Field',
    icon=folium.Icon(color='red')
).add_to(m)

st_folium(m, width=725, height=500)

species = st.selectbox(
   "Review sensitive species at this site",
   ["Gopherus agassizii (Cooper, 1861)"],
   placeholder="Select species...",
)


# load data into session state
load_data()
stdf = st.session_state.df_tortise

coords = stdf[['decimalLatitude', 'decimalLongitude']]
coords_unique = coords.drop_duplicates()

# Streamlit UI
# species = st.text_input(
#     "Scientific name of animal eg: Gopherus agassizii (Cooper, 1861)")

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


# process_raster_files(input_directory, west, south,
#                      east, north, output_directory)


# st.header("A focus on the desert tortise :- Gopherus agassizii (Cooper, 1861)")
# st.write("---")

# with open('training_data.pkl', 'rb') as f:
#     train_xs, train_y = pickle.load(f)

# with open('target_data.pkl', 'rb') as f:
#     target_xs, raster_info = pickle.load(f)

# st.subheader("Model Evaluations")
# perform_model_evaluations(train_xs, train_y, target_xs, raster_info, st)


st.title("Predicted Range")

# Load the raster data
distr_rf = load_raster_data("outputs/rf-images/probability_1.0.tif")
distr_et = load_raster_data("outputs/et-images/probability_1.0.tif")
distr_xgb = load_raster_data("outputs/xgb-images/probability_1.tif")

# Calculate the averaged distribution
distr_averaged = (distr_rf + distr_et + distr_xgb) / 3

# cola, colb = st.columns(2)
# with cola:
#     st.markdown("<h3 style='text-align: center;'>Desert Tortoise Predicted Range</h3>",
#                 unsafe_allow_html=True)
#     # Display the plot
#     fig = plotit(distr_averaged, "", cmap="Greens")
#     st.pyplot(fig, use_container_width=True)


colormap = linear.YlGnBu_09.scale(0, distr_averaged.max())
colormap.caption = 'Probability Distribution'

# with colb:
st.markdown("<h3 style='text-align: left;'>Desert Tortoise Predicted Range- Current</h3>",
            unsafe_allow_html=True)
create_folium_map(colormap)

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
st.write('add these forecasts next. need raster predictions for the future.')
