import streamlit as st
import pandas as pd
import numpy as np
from faker import Faker

st.title("Generador de Datos Sintéticos")

with st.sidebar.form("form_datos"):
    num_filas = st.number_input("Número de registros (filas)", min_value=1, value=10)
    semilla = st.number_input("Número de la suerte (semilla)", min_value=0, value=42)
    num_numericas = st.slider("Columnas Numéricas", min_value=0, max_value=5, value=2)
    num_strings = st.slider("Columnas de Texto", min_value=0, max_value=5, value=2)
    num_booleans = st.slider("Columnas Booleanas", min_value=0, max_value=5, value=1)
    num_fechas = st.slider("Columnas de Fecha", min_value=0, max_value=5, value=1)
    porcentaje_nulos = st.slider("% de nulos/vacíos en los datos", min_value=0, max_value=100, value=0)
    idioma_opcion = st.selectbox("Idioma de los strings", options=["Español", "Inglés"], index=0)
    generar = st.form_submit_button("Generar")

df = None

if generar:
    np.random.seed(int(semilla))
    idioma = 'es_ES' if idioma_opcion == "Español" else 'en_US'
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
    st.dataframe(df.sample(10))

if df is not None:
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Descargar CSV",
        data=csv,
        file_name="datos_sinteticos.csv",
        mime="text/csv"
    )

