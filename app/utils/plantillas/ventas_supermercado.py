"""Plantilla para generar datos sintéticos de ventas de supermercado."""

import pandas as pd
import numpy as np
from faker import Faker

from .base import PlantillaBase


class PlantillaVentasSupermercado(PlantillaBase):
    """Plantilla para generar datos de ventas de supermercado."""

    @property
    def nombre(self) -> str:
        return "Ventas Supermercado"

    @property
    def descripcion(self) -> str:
        return "Registro de ventas de supermercado con productos, precios y cantidades"

    def generar(self) -> pd.DataFrame:
        fake = Faker(self.idioma)
        fake.seed_instance(self.semilla)
        np.random.seed(self.semilla)

        productos = ['Leche', 'Pan', 'Arroz', 'Pollo', 'Manzanas', 'Yogurt',
                    'Pasta', 'Aceite', 'Huevos', 'Queso', 'Tomates', 'Cereal']

        data = {
            'fecha_venta': [fake.date_between(start_date='-6m', end_date='today')
                           for _ in range(self.num_filas)],
            'ticket_id': [f"TK{fake.random_number(digits=6)}" for _ in range(self.num_filas)],
            'producto': np.random.choice(productos, self.num_filas),
            'categoria': np.random.choice(['Lácteos', 'Panadería', 'Carnes', 'Frutas',
                                         'Cereales'], self.num_filas),
            'cantidad': np.random.randint(1, 10, self.num_filas),
            'precio_unitario': np.random.uniform(0.5, 25, self.num_filas).round(2),
            'descuento_pct': np.random.choice([0, 5, 10, 15, 20], self.num_filas,
                                            p=[0.6, 0.2, 0.1, 0.05, 0.05]),
            'vendedor_id': np.random.randint(1, 20, self.num_filas)
        }

        dataframe = pd.DataFrame(data)
        dataframe['total'] = (dataframe['cantidad'] * dataframe['precio_unitario'] *
                             (1 - dataframe['descuento_pct'] / 100)).round(2)

        # Aplicar nulos si es necesario (excluir IDs y fechas críticas)
        dataframe = self._aplicar_nulos(dataframe, columnas_excluir=['fecha_venta', 'ticket_id'])

        return dataframe
