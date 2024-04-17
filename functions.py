import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import rasterio
import requests
import folium
import base64
import os

from rasterio.windows import from_bounds
from streamlit_folium import st_folium
from rasterio.plot import show
from io import BytesIO


######################################
# Function to load data, if not already in session state

def load_data():
    if 'df_tortise' not in st.session_state:
        dfs = os.path.expanduser("~/data/bio/data/tortoise.tsv")
        st.session_state.df_tortise = pd.read_csv(dfs, sep='\t')


######################################
# Function to get data from GBIF API

def gbif_data(scientificName, max_pages=10):
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


# cropping Bioclim Raster Files
# Define the Colombian Amazon extent: latitude ~12°N and ~4°S and between longitudes ~67° and ~79°W.
lat_extent = [12, -4.3]
long_extent = [-79, -67]
# Define the extent coordinates (west, south, east, north)
# west, south, east, north = -79, -4.3, -67, 12
west, south, east, north = -76, -4.5, -67, 5
# Define the extent of the desert tortoise range
west, south, east, north = -120, 24, -100, 45

# Specify the directory containing the raster files
input_directory = os.path.expanduser("~/data/bio/data/wc2")
output_directory = os.path.expanduser(
    "~/data/bio/inputs/cropped_bioclim_tortoise")

# Define geographic coordinates for the bounding box
west, south, east, north = -120, 24, -100, 45


def process_raster_files(directory, west, south, east, north, output_dir):
    # Create the output directory if it does not exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Walk through all files in the input directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.tif'):
                file_path = os.path.join(root, file)
                with rasterio.open(file_path) as src:
                    # Convert geographic coordinates to raster window
                    window = from_bounds(
                        west, south, east, north, src.transform)

                    # Read the data in the window, cropping to the extent
                    data = src.read(window=window)

                    # Loop through each band and write to ASCII
                    for i in range(1, src.count + 1):
                        output_path = os.path.join(
                            output_dir, f'{os.path.splitext(file)[0]}_band{i}.asc')
                        with rasterio.open(output_path, 'w', driver='AAIGrid', height=window.height, width=window.width,
                                           count=1, dtype=data.dtype, transform=rasterio.windows.transform(window, src.transform)) as dst:
                            # Write each band to a new file
                            dst.write(data[i-1], 1)

# Function to generate background points based on extent of presence points


def sample_background_points(raster, num_points, extent_factor):
    with rasterio.open(raster) as src:
        # Create a bounding box that is 25% larger (sampling from a larger area helps with edge effects)
        b = src.bounds
        width = (b.right - b.left) * (extent_factor - 1) / 2
        height = (b.top - b.bottom) * (extent_factor - 1) / 2
        larger_extent = box(b.left - width, b.bottom -
                            height, b.right + width, b.top + height)

        # Generate random points within the larger extent
        xs = np.random.uniform(b.left - width, b.right + width, num_points)
        ys = np.random.uniform(b.bottom - height, b.top + height, num_points)

        # Filter points to lie within the original raster extent
        points = gpd.GeoDataFrame(geometry=gpd.points_from_xy(xs, ys))
        original_extent = box(b.left, b.bottom, b.right, b.top)
        points = points[points.geometry.within(original_extent)]

    return points
