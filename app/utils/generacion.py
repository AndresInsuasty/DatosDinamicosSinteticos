import numpy as np
import pandas as pd
from faker import Faker

def asignar_nulos(col_data, n_nulos):
    idx = np.random.choice(len(col_data), n_nulos, replace=False)
    if isinstance(col_data, np.ndarray):
        col_data[idx] = np.nan
    else:
        for j in idx:
            col_data[j] = None
    return col_data

def generar_columna_numerica(n_filas, n_nulos):
    col_data = np.random.randn(n_filas)
    if n_nulos > 0:
        col_data = asignar_nulos(col_data, n_nulos)
    return col_data

def generar_columna_string(n_filas, n_nulos, fake):
    col_data = [fake.word() for _ in range(n_filas)]
    if n_nulos > 0:
        col_data = asignar_nulos(col_data, n_nulos)
    return col_data

def generar_columna_booleana(n_filas, n_nulos):
    col_data = np.random.choice([True, False], size=n_filas)
    if n_nulos > 0:
        col_data = asignar_nulos(col_data, n_nulos)
    return col_data

def generar_columna_fecha(n_filas, n_nulos, fake):
    col_data = [fake.date_between(start_date='-5y', end_date='today') for _ in range(n_filas)]
    if n_nulos > 0:
        col_data = asignar_nulos(col_data, n_nulos)
    return col_data

def generar_dataframe(
    num_filas,
    semilla,
    num_numericas,
    num_strings,
    num_booleans,
    num_fechas,
    porcentaje_nulos,
    idioma
):
    np.random.seed(semilla)
    fake = Faker(idioma)
    Faker.seed(semilla)
    n_nulos = int(num_filas * porcentaje_nulos / 100)
    data = {}

    for i in range(num_numericas):
        data[f"num_{i+1}"] = generar_columna_numerica(num_filas, n_nulos)
    for i in range(num_strings):
        data[f"str_{i+1}"] = generar_columna_string(num_filas, n_nulos, fake)
    for i in range(num_booleans):
        data[f"bool_{i+1}"] = generar_columna_booleana(num_filas, n_nulos)
    for i in range(num_fechas):
        data[f"fecha_{i+1}"] = generar_columna_fecha(num_filas, n_nulos, fake)

    return pd.DataFrame(data)
