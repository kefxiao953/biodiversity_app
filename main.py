from functions import *

# load data into session state
load_data()
stdf = st.session_state.df_tortise

# configure page
st.set_page_config(
    page_title="BIOPRAEDICO Project",
    page_icon=":recycle:",
    layout="wide"
)

st.header("BIOPRAEDICO Project")
st.write("---")

# Streamlit UI
species = st.text_input(
    "Scientific name of animal eg: Gopherus agassizii (Cooper, 1861)")

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
        st.write(st.session_state.df)  # Display the data
else:
    # Prompt for input if it is empty
    st.write("Please enter a scientific name to search.")

coords = stdf[['decimalLatitude', 'decimalLongitude']]
coords_unique = coords.drop_duplicates()


process_raster_files(input_directory, west, south,
                     east, north, output_directory)

file_path = os.path.expanduser(
    "~/data/bio/inputs/cropped_bioclim_tortoise/wc2.1_2.5m_bio_1_band1.asc")


st.header("A focus on the desert tortise :- Gopherus agassizii (Cooper, 1861)")
st.subheader("Overlaying Raster data on folium Map")
st.write("---")


col1, col2, col3 = st.columns(3)

# Open the raster file
with rasterio.open(file_path) as src:
    # Read the first band (assuming the file is single-band)
    st.session_state.data = src.read(1)

    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(10, 10))

    # Use rasterio's show method, which handles GeoTransforms correctly
    show(st.session_state.data, ax=ax, transform=src.transform,
         title='Cropped Raster Visualization')
    # plt.show()
    with col1:
        st.pyplot(fig)


midpoint = [(south + north) / 2, (west + east) / 2]

m = folium.Map(location=midpoint, zoom_start=4)

folium.Rectangle(
    bounds=[[south, west], [north, east]],
    color='red',
    fill=True,
    fill_color='red',
    fill_opacity=0.2,
).add_to(m)

with col2:
    # Display the map
    st_folium(m, width=725, height=500)


# Load your raster data
with rasterio.open('inputs/cropped_bioclim_tortoise/wc2.1_2.5m_bio_1_band1.asc') as src:
    # Make a note of the raster bounds
    bounds = src.bounds

    # Read the data (e.g., first band)
    st.session_state.data = src.read(1)

    # Normalize the data for better visualization
    data = (st.session_state.data - st.session_state.data.min()) / \
        (st.session_state.data.max() - st.session_state.data.min())

    # Create a plot
    fig, ax = plt.subplots(frameon=False, figsize=(10, 10))
    plt.axis('off')
    # You can change the colormap to something appropriate for your data
    colormap = plt.cm.viridis
    show(data, ax=ax, cmap=colormap, transform=src.transform, adjust='datalim')

    # Save the plot to a PNG image in memory
    img = BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight',
                pad_inches=0, transparent=True)
    img.seek(0)
    img_base64 = base64.b64encode(img.read()).decode('utf-8')

# Define the image overlay bounds
image_bounds = [[bounds.bottom, bounds.left], [bounds.top, bounds.right]]

# Create a folium map centered on your data
m = folium.Map(location=[(bounds.top + bounds.bottom) / 2,
               (bounds.left + bounds.right) / 2], zoom_start=4)

# Add the image overlay to the map
folium.raster_layers.ImageOverlay(
    image='data:image/png;base64,' + img_base64,
    bounds=image_bounds,
    opacity=0.6  # Adjust opacity as needed
).add_to(m)

with col3:
    # Display the map
    st_folium(m, width=725, height=500)


st.subheader("Presence & Absence Sampling")
st.write("---")
