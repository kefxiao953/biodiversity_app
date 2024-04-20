# Biodiversity Conservation Analysis Repository

## Purpose
This repository supports a major biodiversity conservation project, employing a combination of geospatial analysis, machine learning, and interactive visualizations to assess the impacts of climate change on species distribution. By integrating diverse datasets and employing advanced modeling techniques, our work aims to predict vulnerable regions, aiding stakeholders in making informed conservation decisions.

## Project Structure
/data/: Houses initial datasets used in analyses, including environmental variables and species observations. As part of our project's scaling strategy, this folder will transition to cloud storage for enhanced accessibility and performance.
/inputs/: Contains configuration and input files for the models. These files guide the processing and are integral to the reproducibility of our analyses. This directory will also move to Google Cloud for better management.
/outputs/: Stores outputs from the models and scripts, such as processed data and visual results. The outputs are crucial for stakeholder presentations and further analysis. Migration to cloud storage is planned for this directory as well.
presence_absence.ipynb: Jupyter Notebook for initial data processing, analysis setup, and exploratory data visualization.
doc_presence_absence.ipynb: Enhanced documentation notebook that provides a detailed walkthrough of the data processing and analysis pipeline, intended for educational purposes and new project members.
main.py: The main script for the Streamlit application, facilitating interactive data exploration and visualization. It integrates functionalities defined in functions.py to provide a dynamic web interface.
functions.py: Contains all the reusable code functions used across different parts of the project, such as data loading, raster processing, and visualization. This module supports the modularity and maintainability of the codebase.

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
