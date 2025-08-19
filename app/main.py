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
    generar = st.form_submit_button("Generar")

df = None

if generar:
    np.random.seed(int(semilla))
    fake = Faker()
    Faker.seed(int(semilla))

    data = {}

    # Columnas numéricas
    for i in range(int(num_numericas)):
        col_name = f"num_{i+1}"
        data[col_name] = np.random.randn(int(num_filas))

    # Columnas string
    for i in range(int(num_strings)):
        col_name = f"str_{i+1}"
        data[col_name] = [fake.word() for _ in range(int(num_filas))]

    # Columnas booleanas
    for i in range(int(num_booleans)):
        col_name = f"bool_{i+1}"
        data[col_name] = np.random.choice([True, False], size=int(num_filas))

    # Columnas de fecha
    for i in range(int(num_fechas)):
        col_name = f"fecha_{i+1}"
        data[col_name] = [fake.date_between(start_date='-5y', end_date='today') for _ in range(int(num_filas))]

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
   
