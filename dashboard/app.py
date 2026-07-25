import pandas as pd
import numpy as np
import streamlit as st
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "processed" / "crop_yield_cleaned.csv"


data = pd.read_csv(DATA_PATH)

def add_sidebar():
    #Sidebar
    st.sidebar.header("Crop Yield Prediction Variables")
    
    slider_label = [
        ("Rain Fall (mm)", "rainfall"),
        ("Fertilizer", "fertilizer"),
        ("Temperature", "temperature"),
        ("Nitrogen (N)", "nitrogen"),
        ("Phosphorus (P)", "phosphorus"),
        ("Potassium (K)", "potassium"),
        ("Yield (Q/acre)", "yield"),
    ]
    
    input_values = {}
    for label, key in slider_label:
        input_values[key] = st.sidebar.slider(
            label,
            min_value = 0,
            max_value = int(data[key].max()),
            value = int(data[key].mean()),
        )
    return input_values

def main():
    st.set_page_config(
        page_title="Dashboard Crop Yield Prediction",
        page_icon=":bar_chart:",
        layout="wide",
        initial_sidebar_state="expanded"
        )
    with st.container():
        st.title("Dashboard")
        st.write("This project is a dashboard presenting our models and findings. It is built using Streamlit, a Python library for creating interactive web applications.")
        
    input_values = add_sidebar()
    st.write(input_values)
    #Prediction Section
    col1, col2 = st.columns([4,1])

    with col1:
        st.header("Crop Yield Prediction")
        
    with col2:
        st.write("Prediction")
        
if __name__ == "__main__":
    main()