import streamlit as st
import pandas as pd
import numpy as np
import io

from utils.generacion import generar_dataframe
from utils.descargas import (
    preparar_csv, preparar_excel, preparar_json, preparar_parquet, preparar_sqlite
)
from config.constantes import IDIOMAS_DISPONIBLES

st.title("Generador de Datos Sintéticos")

with st.sidebar.form("form_datos"):
    num_filas = st.number_input("Número de registros (filas)", min_value=1, value=10)
    semilla = st.number_input("Número de la suerte (semilla)", min_value=0, value=42)
    num_numericas = st.slider("Columnas Numéricas", min_value=0, max_value=5, value=2)
    num_strings = st.slider("Columnas de Texto", min_value=0, max_value=5, value=2)
    num_booleans = st.slider("Columnas Booleanas", min_value=0, max_value=5, value=1)
    num_fechas = st.slider("Columnas de Fecha", min_value=0, max_value=5, value=1)
    porcentaje_nulos = st.slider("% de nulos/vacíos en los datos", min_value=0, max_value=100, value=0)
    idioma_opcion = st.selectbox("Idioma", options=list(IDIOMAS_DISPONIBLES.keys()), index=0)
    generar = st.form_submit_button("Generar")

if generar:
    idioma = IDIOMAS_DISPONIBLES[idioma_opcion]
    df = generar_dataframe(
        num_filas=int(num_filas),
        semilla=int(semilla),
        num_numericas=int(num_numericas),
        num_strings=int(num_strings),
        num_booleans=int(num_booleans),
        num_fechas=int(num_fechas),
        porcentaje_nulos=int(porcentaje_nulos),
        idioma=idioma
    )
    st.session_state.df = df
    st.session_state.df_sample = df.sample(min(10, len(df)), random_state=int(semilla))

if "df" in st.session_state and "df_sample" in st.session_state:
    df = st.session_state.df
    sample_df = st.session_state.df_sample
    st.dataframe(sample_df)
    st.write("Opciones de formato para descargar:")

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        formato_csv = st.checkbox("CSV", value=True, key="csv_checkbox")
        if formato_csv:
            csv = preparar_csv(df)
            st.download_button(
                label="Descargar CSV",
                data=csv,
                file_name="datos_sinteticos.csv",
                mime="text/csv"
            )
    with col2:
        formato_excel = st.checkbox("Excel", value=False, key="excel_checkbox")
        if formato_excel:
            buffer = preparar_excel(df)
            st.download_button(
                label="Descargar Excel",
                data=buffer,
                file_name="datos_sinteticos.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    with col3:
        formato_json = st.checkbox("JSON", value=False, key="json_checkbox")
        if formato_json:
            json = preparar_json(df)
            st.download_button(
                label="Descargar JSON",
                data=json,
                file_name="datos_sinteticos.json",
                mime="application/json"
            )
    with col4:
        formato_parquet = st.checkbox("Parquet", value=False, key="parquet_checkbox")
        if formato_parquet:
            buffer_parquet = preparar_parquet(df)
            st.download_button(
                label="Descargar Parquet",
                data=buffer_parquet,
                file_name="datos_sinteticos.parquet",
                mime="application/octet-stream"
            )
    with col5:
        formato_sqlite = st.checkbox("SQLite", value=False, key="sqlite_checkbox")
        if formato_sqlite:
            buffer_sqlite = preparar_sqlite(df)
            st.download_button(
                label="Descargar SQLite",
                data=buffer_sqlite,
                file_name="datos_sinteticos.db",
                mime="application/x-sqlite3"
            )

