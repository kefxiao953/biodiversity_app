import folium
from folium import plugins
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from streamlit_folium import folium_static, st_folium
from streamlit_extras.switch_page_button import switch_page

# configure page
st.set_page_config(
    page_title="Biopraedico",
    page_icon=":recycle:",
    layout="wide"
)

st.header("Welcome to Biopraedico :crystal_ball:")
st.divider()
st.subheader("Predict a Sustainable Future")


st.image("images/intro.png", output_format='PNG', width=1000)

st.markdown("""
<h3 style='text-align: left; color: black;'>Biopraedico enables informed decisions around biodiversity impact.
We are empowering everyone from investors
to conservation groups to everyday consumers to make decisions that advance sustainable development
while preserving biodiversity.</h3>""", unsafe_allow_html=True)

st.markdown("<h3 style='text-align: left; color: green;'>Become a leader in advancing ecosystems and economies.</h3>",
            unsafe_allow_html=True)


col1, col2 = st.columns(2)

with col1:
    demo1 = st.button("Request a Consultation", key="demo1")
    if demo1:
        switch_page("request consult")

with col2:
    demo2 = st.button("Explore our Data", key="demo2")
    if demo2:
        switch_page("for consumers")

st.divider()

