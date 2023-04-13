import pandas as pd
import geopandas as gpd
import numpy as np
import streamlit as st

def detect_anomalies(df, column_name, threshold):
    mean = np.mean(df[column_name])
    std = np.std(df[column_name])

    df['z_score'] = (df[column_name] - mean) / std

    anomalies = df[np.abs(df['z_score']) > threshold]

    return anomalies

st.title("Anomaly Detection - School Safety Zones")

uploaded_file = st.file_uploader("Upload data set", type=["csv", "geojson"])

DEFAULT_THRESHOLD = 2.5
DEFAULT_COLUMN_NAME = "strobe_speed"

threshold = st.sidebar.slider("Threshold", min_value=1.0, max_value=5.0, step=0.1, value=float(DEFAULT_THRESHOLD))

if uploaded_file is not None:
    if uploaded_file.type == 'text/csv':
        df = pd.read_file(uploaded_file)
    elif uploaded_file.type == 'application/geo+json':
        df = gpd.read_file(uploaded_file)
    else:
        st.write("File type not supported. Please upload a CSV or GeoJSON file.")
        st.stop()

    column_name = st.sidebar.selectbox("Column", df.columns, index=df.columns.get_loc(DEFAULT_COLUMN_NAME))

    anomalies = detect_anomalies(df, column_name, threshold)

    st.subheader("Results")
    st.write(f"Threshold: {threshold}")
    st.write(f"Column: {column_name}")
    st.write(f"Number of anomalies: {len(anomalies)}")

    if not anomalies.empty:
        st.write(anomalies)

    else:
        st.write("No anomalies detected.")
else:
    st.write("Please upload a CSV or GeoJSON file!")
