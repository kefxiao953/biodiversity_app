# Biopraedico: Predicting a sustainable future through biodiversity forecasting  
Visit our app [here!](https://github.com/myabarca/biopraedico](http://biopraedico.streamlit.app)

## Purpose
This repository supports a biodiversity forecasting project, employing a combination of geospatial analysis, machine learning, and interactive visualizations to predict species distributions. We integrate datasets on species presence and bioclimatic features and employ ensembled modeling techniques, with the goal of aiding a variety of stakeholders in making informed decisions around sustainable development, conservation, and consumption.

## Project Structure
### data: 
Houses initial datasets used in analyses, including environmental variables from WorldClim and species observations from the Global Biodiversity Information Facility (GBIF). As part of our project's scaling strategy, this folder will transition to cloud storage for enhanced accessibility and performance.

### inputs: 
Contains configuration and input files for the models. These files guide the processing and are integral to the reproducibility of our analyses. This directory will also move to Google Cloud for better management.

### outputs: 
Stores outputs from the models and scripts, such as processed data and visual results. These outputs fuel our web app visualizations. Migration to cloud storage is planned for this directory as well.

### presence_absence.ipynb: 
Jupyter Notebook for initial data processing, analysis setup, and exploratory data visualization.

### annotated_presence_absence.ipynb: 
Enhanced documentation notebook that provides a detailed walkthrough of the data processing and analysis pipeline, intended for educational purposes and new project members.

### homepage.py: 
The main script for the Streamlit application, facilitating interactive data exploration and visualization. It integrates functionalities defined in functions.py to provide a dynamic web interface.

### functions.py: 
Contains all the reusable code functions used across different parts of the project, such as data loading, raster processing, and visualization. This module supports the modularity and maintainability of the codebase.

## Key Functionalities
### Interactive Data Visualization: 
Leveraging Streamlit, the project offers a web-based interface for interactive visualization of species distribution models.
### Advanced Geospatial Analysis: 
Utilizes raster data processing for detailed environmental analysis, crucial for understanding species habitats.
### Machine Learning Integration: 
Implements species distribution modeling using advanced machine learning techniques to predict species responses to environmental changes.

Moving forward, we will also implement cloud sotrage integration: Transitioning to Google Cloud for data and application hosting, ensuring scalability and robust data management.


## Authors
Maricela Abarca
Daniel Gonzalez
Solomon Asiedu-Ofei
Mark Lam
Kefeng Xiao
