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

unique_species = pd.read_csv('nestle_unique_endangered_species.csv')

st.markdown(text)

companies = ["Meta", "Google", "Nestle", "Tesla"]

# Create a select box for company selection
selected_company = st.selectbox("Select a Company:", companies)
unique_species_count = len(unique_species)
endangered_species_count = sum(unique_species['count'])

# Creating geodataframe
df = pd.read_csv('data/bats.tsv', sep='\t')
df = df[["decimalLatitude", "decimalLongitude"]]
geometry = gpd.points_from_xy(df.decimalLongitude, df.decimalLatitude)
gdf = gpd.GeoDataFrame(df, geometry=geometry)

# Heatmap
heatmap = folium.Map(
    location=[0.75, -74],
    zoom_start=7
)

heat_data = [[point.xy[1][0], point.xy[0][0]] for point in gdf.geometry]
plugins.HeatMap(heat_data).add_to(heatmap)

if selected_company == "Nestle":
    # Assume unique_species is already defined and loaded with data

    st.markdown("""
        ## 🌍 Biodiversity Dashboard
        """, unsafe_allow_html=True)

    st.markdown(f"""
        ### 🔎 Unique Endangered Species
        **Number of Unique Endangered Species:** {unique_species_count}
        """, unsafe_allow_html=True)

    st.markdown(f"""
        ### 🚨 Total Endangered Species
        **Number of Endangered Species Instances:** {endangered_species_count}
        """, unsafe_allow_html=True)

    st_folium(heatmap, width=725, height=500)

# don't forget to add pictures of bird - maybe some from inaturalist to plug community science


unique_species_names = unique_species['species'].unique()[:10]

# Create a select box for species selection
selected_species = st.selectbox("Select a Species:", unique_species_names)

# Display the count of the selected species
if selected_species:
    # Retrieve the count for the selected species from the DataFrame
    # Assuming each species only appears once, we can use .loc to find the count
    species_count = unique_species.loc[unique_species['species']
                                       == selected_species, 'count'].values[0]

    # Write the count to the Streamlit app
    st.write(f"Count of {selected_species}: {species_count}")
