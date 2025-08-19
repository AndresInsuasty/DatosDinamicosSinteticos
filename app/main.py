import streamlit as st
import pandas as pd
import numpy as np
import io

from utils.generacion import generar_dataframe
from utils.descargas import (
    preparar_csv, preparar_excel, preparar_json, preparar_parquet, preparar_sqlite
)
from config.constantes import IDIOMAS_DISPONIBLES
from utils.plantillas import PLANTILLAS_DISPONIBLES

st.title("Generador de Datos Sintéticos")

with st.sidebar:
    # Selector de modo
    modo = st.radio(
        "Modo de generación:",
        ["Personalizado", "Plantillas"],
        help="Personalizado: configura tus propias columnas. Plantillas: usa estructuras predefinidas."
    )
    
    with st.form("form_datos"):
        if modo == "Plantillas":
            plantilla_seleccionada = st.selectbox(
                "Selecciona una plantilla:",
                options=list(PLANTILLAS_DISPONIBLES.keys()),
                help="Plantillas predefinidas con estructuras de datos específicas"
            )
        
        # Parámetros comunes para ambos modos
        num_filas = st.number_input("Número de registros (filas)", min_value=1, value=10)
        semilla = st.number_input("Número de la suerte (semilla)", min_value=0, value=42)
        porcentaje_nulos = st.slider("% de nulos/vacíos en los datos", min_value=0, max_value=100, value=0)
        idioma_opcion = st.selectbox("Idioma", options=list(IDIOMAS_DISPONIBLES.keys()), index=0)
        
        # Parámetros específicos para modo personalizado
        if modo == "Personalizado":
            num_numericas = st.slider("Columnas Numéricas", min_value=0, max_value=5, value=2)
            num_strings = st.slider("Columnas de Texto", min_value=0, max_value=5, value=2)
            num_booleans = st.slider("Columnas Booleanas", min_value=0, max_value=5, value=1)
            num_fechas = st.slider("Columnas de Fecha", min_value=0, max_value=5, value=1)
        
        generar = st.form_submit_button("Generar")

if generar:
    idioma = IDIOMAS_DISPONIBLES[idioma_opcion]
    
    if modo == "Personalizado":
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
    else:  # Modo plantillas
        plantilla_clase = PLANTILLAS_DISPONIBLES[plantilla_seleccionada]
        plantilla = plantilla_clase(
            num_filas=int(num_filas),
            semilla=int(semilla),
            porcentaje_nulos=int(porcentaje_nulos),
            idioma=idioma
        )
        df = plantilla.generar()
    
    st.session_state.df = df
    st.session_state.df_sample = df.sample(min(10, len(df)), random_state=int(semilla))

if "df" in st.session_state and "df_sample" in st.session_state:
    df = st.session_state.df
    sample_df = st.session_state.df_sample
    st.dataframe(sample_df)
    
    st.write("**Descargar datos en diferentes formatos:**")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        csv = preparar_csv(df)
        st.download_button(
            label="📄 CSV",
            data=csv,
            file_name="datos_sinteticos.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col2:
        buffer = preparar_excel(df)
        st.download_button(
            label="📊 Excel",
            data=buffer,
            file_name="datos_sinteticos.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
    
    with col3:
        json = preparar_json(df)
        st.download_button(
            label="📋 JSON",
            data=json,
            file_name="datos_sinteticos.json",
            mime="application/json",
            use_container_width=True
        )
    
    with col4:
        buffer_parquet = preparar_parquet(df)
        st.download_button(
            label="🗜️ Parquet",
            data=buffer_parquet,
            file_name="datos_sinteticos.parquet",
            mime="application/octet-stream",
            use_container_width=True
        )
    
    with col5:
        buffer_sqlite = preparar_sqlite(df)
        st.download_button(
            label="🗃️ SQLite",
            data=buffer_sqlite,
            file_name="datos_sinteticos.db",
            mime="application/x-sqlite3",
            use_container_width=True
        )

