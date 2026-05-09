# create_streamlit_app.py

import streamlit as st
import pandas as pd


def create_streamlit_app(data_csv):
    df = pd.read_csv(data_csv)
    st.title("Aplicación interactiva de análisis de datos")
    st.dataframe(df)
    st.write(df.describe())


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        create_streamlit_app(sys.argv[1])
    else:
        print("Uso: python create_streamlit_app.py <ruta_archivo_csv>")
