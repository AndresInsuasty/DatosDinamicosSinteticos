import streamlit as st
import pandas as pd
import numpy as np
from faker import Faker
import io

st.title("Generador de Datos Sintéticos")

with st.sidebar.form("form_datos"):
    num_filas = st.number_input("Número de registros (filas)", min_value=1, value=10)
    semilla = st.number_input("Número de la suerte (semilla)", min_value=0, value=42)
    num_numericas = st.slider("Columnas Numéricas", min_value=0, max_value=5, value=2)
    num_strings = st.slider("Columnas de Texto", min_value=0, max_value=5, value=2)
    num_booleans = st.slider("Columnas Booleanas", min_value=0, max_value=5, value=1)
    num_fechas = st.slider("Columnas de Fecha", min_value=0, max_value=5, value=1)
    porcentaje_nulos = st.slider("% de nulos/vacíos en los datos", min_value=0, max_value=100, value=0)
    idiomas_disponibles = {
        "Español": "es_ES",
        "Inglés": "en_US",
        "Francés": "fr_FR",
        "Alemán": "de_DE",
        "Italiano": "it_IT",
        "Portugués": "pt_BR"
    }
    idioma_opcion = st.selectbox("Idioma", options=list(idiomas_disponibles.keys()), index=0)
    generar = st.form_submit_button("Generar")

if generar:
    np.random.seed(int(semilla))
    idioma = idiomas_disponibles[idioma_opcion]
    fake = Faker(idioma)
    Faker.seed(int(semilla))

    data = {}
    n_filas = int(num_filas)
    n_nulos = int(n_filas * porcentaje_nulos / 100)

    # Columnas numéricas
    for i in range(int(num_numericas)):
        col_name = f"num_{i+1}"
        col_data = np.random.randn(n_filas)
        if n_nulos > 0:
            idx = np.random.choice(n_filas, n_nulos, replace=False)
            col_data[idx] = np.nan
        data[col_name] = col_data

    # Columnas string
    for i in range(int(num_strings)):
        col_name = f"str_{i+1}"
        col_data = [fake.word() for _ in range(n_filas)]
        if n_nulos > 0:
            idx = np.random.choice(n_filas, n_nulos, replace=False)
            for j in idx:
                col_data[j] = None
        data[col_name] = col_data

    # Columnas booleanas
    for i in range(int(num_booleans)):
        col_name = f"bool_{i+1}"
        col_data = np.random.choice([True, False], size=n_filas)
        if n_nulos > 0:
            idx = np.random.choice(n_filas, n_nulos, replace=False)
            col_data[idx] = None
        data[col_name] = col_data

    # Columnas de fecha
    for i in range(int(num_fechas)):
        col_name = f"fecha_{i+1}"
        col_data = [fake.date_between(start_date='-5y', end_date='today') for _ in range(n_filas)]
        if n_nulos > 0:
            idx = np.random.choice(n_filas, n_nulos, replace=False)
            for j in idx:
                col_data[j] = None
        data[col_name] = col_data

    df = pd.DataFrame(data)
    st.session_state.df = df  # Guarda el DataFrame en el estado de sesión
    st.session_state.df_sample = df.sample(10, random_state=int(semilla))


# Usa el DataFrame guardado en el estado de sesión para mostrar y descargar
if "df" in st.session_state and "df_sample" in st.session_state:
    df = st.session_state.df
    sample_df = st.session_state.df_sample
    st.dataframe(sample_df)
    st.write("Opciones de formato para descargar:")
    formato_csv = st.checkbox("CSV", value=True)
    formato_excel = st.checkbox("Excel", value=False)
    if formato_csv:
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Descargar CSV",
            data=csv,
            file_name="datos_sinteticos.csv",
            mime="text/csv"
        )
    if formato_excel:
        buffer = io.BytesIO()
        df.to_excel(buffer, index=False, engine='openpyxl')
        buffer.seek(0)
        st.download_button(
            label="Descargar Excel",
            data=buffer,
            file_name="datos_sinteticos.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

# Sí, se requiere openpyxl para exportar a Excel con pandas.

