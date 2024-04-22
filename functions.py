import matplotlib.pyplot as plt
import geopandas as gpd
import streamlit as st
import pandas as pd
import numpy as np
import rasterio
import requests
import pickle
import folium
import base64
import glob
import os

# from pyimpute import load_training_vector, load_targets, impute
from streamlit_folium import folium_static, st_folium
from rasterio.windows import from_bounds
from shapely.geometry import Point, box
from branca.colormap import linear
from rasterio.plot import show
from io import BytesIO
from pylab import plt

# from sklearn.ensemble import RandomForestClassifier
# from sklearn.ensemble import ExtraTreesClassifier
# from sklearn import model_selection
# from xgboost import XGBClassifier
# from lightgbm import LGBMClassifier

######################################
# Function to load data, if not already in session state


def load_data():
    if 'df_tortise' not in st.session_state:
        dfs = os.path.expanduser("data/tortoise.tsv")
        st.session_state.df_tortise = pd.read_csv(dfs, sep='\t')


######################################
# Function to get data from GBIF API

def gbif_data(scientificName, max_pages=1):
    base_url = 'https://api.gbif.org/'
    endpoint_path = 'v1/occurrence/search'
    full_url = base_url + endpoint_path

    # Start with an offset of 0
    offset = 0
    limit = 300  # Set a reasonable limit per page

    all_results = []

    for page in range(max_pages):
        params = {
            'scientificName': scientificName,
            # 'year': 1899,
            # 'continent': 'SOUTH_AMERICA',
            # 'country': 'CO',
            'limit': limit,
            'offset': offset
        }

        response = requests.get(full_url, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            all_results.extend(data['results'])
            # Update offset for the next page
            offset += limit
        else:
            print('Request failed with status code:', response.status_code)
            break

    return pd.DataFrame(all_results)

# Specify the directory containing the raster files
input_directory = os.path.expanduser("data/wc2")
output_directory = os.path.expanduser(
    "inputs/cropped_bioclim_tortoise")

# Define geographic coordinates for the bounding box
# example for tortoises
west, south, east, north = -120, 24, -100, 45


# def process_raster_files(directory, west, south, east, north, output_dir):
#     """
#     Crop the bioclim raster files to an area of interest.

#     Args:
#     directory (str): Directory where bioclim rasters live.
#     west (numeric): Westernmost extent desired
#     south (numeric): Southmost extent desired
#     east (numeric): Easternmost extent desired
#     north (num): Northmost extent desired
#     """
#     # Create the output directory if it does not exist
#     if not os.path.exists(output_dir):
#         os.makedirs(output_dir)

#     # Walk through all files in the input directory
#     for root, dirs, files in os.walk(directory):
#         for file in files:
#             if file.endswith('.tif'):
#                 file_path = os.path.join(root, file)
#                 with rasterio.open(file_path) as src:
#                     # Convert geographic coordinates to raster window
#                     window = from_bounds(
#                         west, south, east, north, src.transform)

#                     # Read the data in the window, cropping to the extent
#                     data = src.read(window=window)

#                     # Loop through each band and write to ASCII
#                     for i in range(1, src.count + 1):
#                         output_path = os.path.join(
#                             output_dir, f'{os.path.splitext(file)[0]}_band{i}.asc')
#                         with rasterio.open(output_path, 'w', driver='AAIGrid', height=window.height, width=window.width,
#                                            count=1, dtype=data.dtype, transform=rasterio.windows.transform(window, src.transform)) as dst:
#                             # Write each band to a new file
#                             dst.write(data[i-1], 1)


# def visualize_raster(file_path):
#     """
#     Visualizes a single-band raster file.

#     Using the streamlit Matplotlib display
#     Args:
#     file_path (str): The path to the raster file.
#     """
#     with rasterio.open(file_path) as src:
#         # Read the first band
#         data = src.read(1)

#         # Create a figure and axis
#         fig, ax = plt.subplots(figsize=(10, 10))

#         # Display the raster data in streamlit
#         show(data, ax=ax, transform=src.transform)
#         st.pyplot(fig)


# def create_map_with_rectangle(south, north, west, east):
#     """
#     Creates a Folium map centered at the midpoint of given bounds with a rectangle overlay.

#     Args:
#     south (float): The southern boundary latitude.
#     north (float): The northern boundary latitude.
#     west (float): The western boundary longitude.
#     east (float): The eastern boundary longitude.
#     """
#     # Calculate the midpoint for the map center
#     midpoint = [(south + north) / 2, (west + east) / 2]

#     # Create a map centered at the midpoint
#     m = folium.Map(location=midpoint, zoom_start=4)

#     # Add a rectangle to the map
#     folium.Rectangle(
#         bounds=[[south, west], [north, east]],
#         color='red',
#         fill=True,
#         fill_color='red',
#         fill_opacity=0.2,
#     ).add_to(m)

#     # Return the map object
#     return st_folium(m, width=725, height=500)


# def create_folium_map_with_raster_overlay(file_path):
#     """
#     Creates a Folium map with a specified raster overlay.

#     Args:
#     file_path (str): Path to the raster file.
#     """
#     with rasterio.open(file_path) as src:
#         # Get the raster bounds
#         bounds = src.bounds

#         # Read the first band
#         data = src.read(1)

#         # Normalize the data for better visualization
#         normalized_data = (data - data.min()) / (data.max() - data.min())

#         # Create a plot
#         fig, ax = plt.subplots(frameon=False, figsize=(10, 10))
#         plt.axis('off')
#         colormap = plt.cm.viridis  # Change the colormap to something appropriate for your data
#         show(normalized_data, ax=ax, cmap=colormap,
#              transform=src.transform, adjust='datalim')

#         # Save the plot to a PNG image in memory
#         img = BytesIO()
#         plt.savefig(img, format='png', bbox_inches='tight',
#                     pad_inches=0, transparent=True)
#         img.seek(0)
#         img_base64 = base64.b64encode(img.read()).decode('utf-8')

#     # Define the image overlay bounds
#     image_bounds = [[bounds.bottom, bounds.left], [bounds.top, bounds.right]]

#     # Create a folium map centered on your data
#     m = folium.Map(location=[(bounds.top + bounds.bottom) / 2,
#                    (bounds.left + bounds.right) / 2], zoom_start=4)

#     # Add the image overlay to the map
#     folium.raster_layers.ImageOverlay(
#         image='data:image/png;base64,' + img_base64,
#         bounds=image_bounds,
#         opacity=0.6  # Adjust opacity as needed
#     ).add_to(m)

#     return st_folium(m, width=725, height=500)


################## PRESENCE & ABSENCE SAMPLING ##################

# def sample_background_points(raster, num_points, extent_factor):
#     """
#     Generates background points based on extent of presence points.
#     """
#     with rasterio.open(raster) as src:
#         # Create a bounding box that is 25% larger (sampling from a larger area helps with edge effects)
#         b = src.bounds
#         width = (b.right - b.left) * (extent_factor - 1) / 2
#         height = (b.top - b.bottom) * (extent_factor - 1) / 2
#         # larger_extent = box(b.left - width, b.bottom -
#         #                     height, b.right + width, b.top + height)

#         # Generate random points within the larger extent
#         xs = np.random.uniform(b.left - width, b.right + width, num_points)
#         ys = np.random.uniform(b.bottom - height, b.top + height, num_points)

#         # Filter points to lie within the original raster extent
#         points = gpd.GeoDataFrame(geometry=gpd.points_from_xy(xs, ys))
#         original_extent = box(b.left, b.bottom, b.right, b.top)
#         points = points[points.geometry.within(original_extent)]

#     return points


# def perform_model_evaluations(train_xs, train_y, target_xs, raster_info, st):
#     """
#     Perform model fitting, cross-validation, and spatial prediction for multiple classifiers.

#     Args:
#     train_xs (array-like): Training data features.
#     train_y (array-like): Training data labels.
#     target_xs (array-like): Target data features for spatial prediction.
#     raster_info (dict): Information or metadata about the raster data used in spatial prediction.
#     st (module): The Streamlit module for logging outputs in a Streamlit app.
#     """

#     CLASS_MAP = {
#         'rf': RandomForestClassifier(),
#         'et': ExtraTreesClassifier(),
#         'xgb': XGBClassifier(),
#     }

#     # Model fitting and spatial range prediction
#     for name, model in CLASS_MAP.items():
#         # Cross validation for accuracy scores (displayed as a percentage)
#         k = 5  # k-fold
#         kf = model_selection.KFold(n_splits=k)
#         accuracy_scores = model_selection.cross_val_score(
#             model, train_xs, train_y, cv=kf, scoring='accuracy')
#         st.write(f"{name} {k}-fold Cross Validation Accuracy: {accuracy_scores.mean() * 100:.2f} (+/- {accuracy_scores.std() * 200:.2f})")

#         # Spatial prediction
#         model.fit(train_xs, train_y)
#         output_directory = 'outputs/' + name + '-images'
#         if not os.path.exists(output_directory):
#             os.makedirs(output_directory)

#         impute(target_xs, model, raster_info, outdir=output_directory,
#                class_prob=True, certainty=True)


def load_raster_data(filepath):
    """Helper function to load raster data from a file."""
    with rasterio.open(filepath) as src:
        return src.read(1)


def plotit(x, title, cmap="Blues"):
    """
    Creates a heatmap plot of the array 'x' with a color map.

    Args:
    x (array-like): 2D array of data to plot.
    title (str): Title of the plot.
    cmap (str): Color map name for the plot.
    """
    fig, ax = plt.subplots(figsize=(10, 10))
    cax = ax.imshow(x, cmap=cmap, interpolation='nearest')
    fig.colorbar(cax)
    ax.set_title(title, fontweight='bold')
    return fig


def create_folium_map(colormap):
    """
    Creates a Folium map with a raster image overlay, a marker, and a colormap.

    Args:
    raster_path (str): Path to the raster file to extract bounds and CRS.
    image_path (str): Path to the image file to overlay on the map.
    popup_location (list): Latitude and longitude as a list for placing the popup marker.
    popup_text (str): Text content for the popup marker.
    colormap: Folium colormap object to be added to the map.
    initial_location (list): Latitude and longitude as a list for the initial focus point of the map.
    zoom_start (int): Initial zoom level for the map.

    Returns:
    folium.Map: The constructed Folium map object.
    """
    # Open the raster file to find bounds and CRS
    with rasterio.open("outputs/rf-images/probability_1.0.tif") as src:
        bounds = src.bounds
        crs = src.crs

    # Map's initial focus point and zoom level
    m = folium.Map(location=[35.5, -115.5], zoom_start=11)

    # Add the image overlay
    folium.raster_layers.ImageOverlay(
        image='outputs/distr_averaged.png',
        bounds=[[bounds.bottom, bounds.left], [bounds.top, bounds.right]],
        # bounds = mojave_bounds,
        opacity=0.6,
        interactive=True,
        cross_origin=False,
        zindex=1,
    ).add_to(m)

    # Add colormap
    colormap.add_to(m)

    # Solar field polygon vertices
    coordinates = [
    [35.59, -115.50],
    [35.599, -115.41],
    [35.52, -115.48]
    ]

    # Create polygon and add it to the map
    folium.vector_layers.Polygon(
        locations=coordinates,  # List of coordinates
        color='blue'          # Color of the polygon's border
    ).add_to(m)

    return st_folium(m, width=725, height=500)
