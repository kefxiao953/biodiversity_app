from functions import *

# load data into session state
load_data()
stdf = st.session_state.df_tortise

coords = stdf[['decimalLatitude', 'decimalLongitude']]
coords_unique = coords.drop_duplicates()

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


process_raster_files(input_directory, west, south,
                     east, north, output_directory)


st.header("A focus on the desert tortise :- Gopherus agassizii (Cooper, 1861)")
st.subheader("Overlaying Raster data on folium Map")
st.write("---")


# Open the raster file

file_path = os.path.expanduser(
    "~/data/bio/inputs/cropped_bioclim_tortoise/wc2.1_2.5m_bio_1_band1.asc")


cola, colb, colc = st.columns(3)
with colb:
    st.markdown("<h3 style='text-align: center;'>Cropped Raster Visualization</h3>",
                unsafe_allow_html=True)
    visualize_raster(file_path)

col2, col3 = st.columns(2)

with col2:
    st.markdown("<h3 style='text-align: center;'>Map centered at the given coordinates with a red rectangle overlay</h3>",
                unsafe_allow_html=True)
    create_map_with_rectangle(south, north, west, east)

with col3:
    st.markdown("<h3 style='text-align: center;'>Overlays a raster visualized as an image on a Folium map based on the raster bounds.</h3>",
                unsafe_allow_html=True)
    create_folium_map_with_raster_overlay(file_path)


# Path to the bioclimatic variable raster
raster_path = 'inputs/cropped_bioclim_tortoise/wc2.1_2.5m_bio_1_band1.asc'

# Number of presence points (in dataframe of occurrences)
length_presences = len(coords_unique)

# Sample background points
background_points = sample_background_points(
    raster_path, length_presences * 2, 1.25)

# Rename columns to 'lon' and 'lat'
background_points['decimalLongitude'] = background_points.geometry.x
background_points['decimalLatitude'] = background_points.geometry.y

# Create the training data by combining presence and background points
train = pd.concat([coords_unique, background_points[[
                  'decimalLongitude', 'decimalLatitude']]], ignore_index=True)

# Create presence-absence column
pa_train = np.concatenate(
    [np.ones(len(coords_unique)), np.zeros(len(background_points))])

# Final DataFrame
train = pd.DataFrame(
    {'CLASS': pa_train, 'lon': train['decimalLongitude'], 'lat': train['decimalLatitude']})

train = train.sample(frac=1).reset_index(drop=True)

# Extract the 'CLASS' column into a separate DataFrame and name the column
class_pa = pd.DataFrame(train.iloc[:, 0])
class_pa.columns = ['CLASS']

# Assuming 'train' has longitude in the 2nd column and latitude in the 3rd column
# Create the GeoDataFrame
geometry = [Point(xy) for xy in zip(train.iloc[:, 1], train.iloc[:, 2])]
data_map = gpd.GeoDataFrame(class_pa, geometry=geometry)

# crs_proj4 = '+proj=longlat +datum=WGS84 +no_defs'  # EPSG:4326
# data_map.set_crs(crs_proj4, inplace=True)

data_map.crs = 'EPSG:4326'  # Directly setting EPSG code

# Write to shapefile
data_map.to_file('inputs/tortoise.shp', driver='ESRI Shapefile')

# Read shapefile as a geodataframe
pa = gpd.GeoDataFrame.from_file("inputs/tortoise.shp")

pa['longitude'] = pa.geometry.x
pa['latitude'] = pa.geometry.y

pa = pa[(pa['longitude'] >= -180) & (pa['longitude'] <= 180)]
pa = pa[(pa['latitude'] >= -90) & (pa['latitude'] <= 90)]


fig, ax = plt.subplots(figsize=(10, 10))
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
world.plot(ax=ax, color='lightgrey')
# Plotting your points in red for visibility
pa.plot(ax=ax, marker='o', color='red', markersize=5)
st.pyplot(fig)


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

with open('training_data.pkl', 'rb') as f:
    train_xs, train_y = pickle.load(f)

with open('target_data.pkl', 'rb') as f:
    target_xs, raster_info = pickle.load(f)

st.subheader("Model Evaluations")
perform_model_evaluations(train_xs, train_y, target_xs, raster_info, st)


st.write("Predicted Range")

st.title("Raster Data Visualization")

# Load the raster data
distr_rf = load_raster_data("outputs/rf-images/probability_1.0.tif")
distr_et = load_raster_data("outputs/et-images/probability_1.0.tif")
distr_xgb = load_raster_data("outputs/xgb-images/probability_1.tif")
# distr_lgbm = load_raster_data("outputs/lgbm-images/probability_1.0.tif")

# Calculate the averaged distribution
distr_averaged = (distr_rf + distr_et + distr_xgb) / 3

cola, colb = st.columns(2)
with cola:
    st.markdown("<h3 style='text-align: center;'>Desert Tortoise Predicted Range</h3>",
                unsafe_allow_html=True)
    # Display the plot
    fig = plotit(distr_averaged, "", cmap="Greens")
    st.pyplot(fig, use_container_width=True)


colormap = linear.YlGnBu_09.scale(0, distr_averaged.max())
colormap.caption = 'Probability Distribution'

# Open the raster file to find bounds
with colb:
    st.markdown("<h3 style='text-align: center;'>Desert Tortoise Predicted Range on Map</h3>",
                unsafe_allow_html=True)
    create_folium_map(colormap)
