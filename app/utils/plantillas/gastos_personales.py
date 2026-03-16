"""Plantilla para generar datos sintéticos de gastos personales."""

import pandas as pd
import numpy as np
from faker import Faker

from .base import PlantillaBase


class PlantillaGastosPersonales(PlantillaBase):
    """Plantilla para generar datos de gastos personales."""

    @property
    def nombre(self) -> str:
        return "Gastos Personales"

    @property
    def descripcion(self) -> str:
        return ("Registro de gastos personales con categorías, montos y fechas. "
                "Montos y métodos de pago correlacionados con la categoría del gasto.")

    def generar(self) -> pd.DataFrame:
        fake = Faker(self.idioma)
        fake.seed_instance(self.semilla)
        np.random.seed(self.semilla)

        # Rangos de monto y probabilidad de recurrencia por categoría
        config_categoria = {
            'Alimentación':     {'rango': (5, 120),   'recurrente': 0.50, 'pago': [0.50, 0.35, 0.15]},
            'Transporte':       {'rango': (10, 200),  'recurrente': 0.60, 'pago': [0.35, 0.40, 0.25]},
            'Entretenimiento':  {'rango': (10, 150),  'recurrente': 0.15, 'pago': [0.30, 0.55, 0.15]},
            'Salud':            {'rango': (15, 300),  'recurrente': 0.40, 'pago': [0.25, 0.50, 0.25]},
            'Educación':        {'rango': (30, 500),  'recurrente': 0.70, 'pago': [0.10, 0.45, 0.45]},
            'Ropa':             {'rango': (20, 350),  'recurrente': 0.05, 'pago': [0.15, 0.70, 0.15]},
            'Servicios':        {'rango': (40, 400),  'recurrente': 0.90, 'pago': [0.05, 0.35, 0.60]},
            'Otros':            {'rango': (5, 200),   'recurrente': 0.20, 'pago': [0.40, 0.40, 0.20]},
        }
        metodos_pago = ['Efectivo', 'Tarjeta', 'Transferencia']
        categorias = list(config_categoria.keys())

        cat_array = np.random.choice(categorias, self.num_filas)

        montos = np.array([
            round(np.random.uniform(*config_categoria[c]['rango']), 2)
            for c in cat_array
        ])
        recurrente = np.array([
            np.random.random() < config_categoria[c]['recurrente']
            for c in cat_array
        ])
        metodo = np.array([
            np.random.choice(metodos_pago, p=config_categoria[c]['pago'])
            for c in cat_array
        ])

        data = {
            'fecha': [fake.date_between(start_date='-1y', end_date='today')
                      for _ in range(self.num_filas)],
            'categoria': cat_array,
            'descripcion': [fake.sentence(nb_words=4) for _ in range(self.num_filas)],
            'monto': montos,
            'metodo_pago': metodo,
            'es_recurrente': recurrente,
        }

        dataframe = pd.DataFrame(data)
        dataframe = self._aplicar_nulos(dataframe, columnas_excluir=['fecha'])
        return dataframe
