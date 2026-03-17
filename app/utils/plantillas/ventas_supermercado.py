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
        return ("Registro de ventas de supermercado con productos, precios y cantidades. "
                "Categoría, precio unitario y cantidad típica correlacionados por producto.")

    def generar(self) -> pd.DataFrame:
        fake = Faker(self.idioma)
        fake.seed_instance(self.semilla)
        np.random.seed(self.semilla)

        # Producto → (categoría, rango_precio, rango_cantidad)
        catalogo = {
            'Leche':        ('Lácteos',    (0.80, 2.50),  (1, 6)),
            'Yogurt':       ('Lácteos',    (0.60, 2.00),  (1, 4)),
            'Queso':        ('Lácteos',    (2.50, 9.00),  (1, 3)),
            'Pan':          ('Panadería',  (0.50, 3.00),  (1, 5)),
            'Croissant':    ('Panadería',  (0.80, 2.50),  (1, 6)),
            'Pollo':        ('Carnes',     (5.00, 18.00), (1, 3)),
            'Carne molida': ('Carnes',     (6.00, 20.00), (1, 2)),
            'Salmón':       ('Pescados',   (8.00, 25.00), (1, 2)),
            'Manzanas':     ('Frutas',     (0.50, 2.00),  (2, 8)),
            'Plátanos':     ('Frutas',     (0.30, 1.20),  (3, 10)),
            'Tomates':      ('Verduras',   (0.40, 2.00),  (2, 8)),
            'Lechuga':      ('Verduras',   (0.60, 2.50),  (1, 3)),
            'Arroz':        ('Cereales',   (1.00, 4.00),  (1, 4)),
            'Pasta':        ('Cereales',   (0.80, 3.50),  (1, 5)),
            'Cereal':       ('Cereales',   (2.50, 7.00),  (1, 3)),
            'Aceite':       ('Despensa',   (3.00, 9.00),  (1, 2)),
            'Huevos':       ('Despensa',   (1.50, 4.50),  (1, 3)),
            'Jugo naranja': ('Bebidas',    (1.50, 4.00),  (1, 4)),
            'Agua mineral': ('Bebidas',    (0.50, 1.80),  (2, 12)),
        }

        productos = list(catalogo.keys())
        prod_array = np.random.choice(productos, self.num_filas)

        categorias_arr = np.array([catalogo[p][0] for p in prod_array])
        precios_arr = np.array([
            round(np.random.uniform(*catalogo[p][1]), 2) for p in prod_array
        ])
        cantidades_arr = np.array([
            np.random.randint(*catalogo[p][2]) for p in prod_array
        ])
        descuentos_arr = np.random.choice(
            [0, 5, 10, 15, 20, 25],
            self.num_filas,
            p=[0.55, 0.20, 0.12, 0.07, 0.04, 0.02]
        )

        data = {
            'fecha_venta': [fake.date_between(start_date='-6m', end_date='today')
                            for _ in range(self.num_filas)],
            'ticket_id': [f"TK{fake.random_number(digits=6):06d}" for _ in range(self.num_filas)],
            'producto': prod_array,
            'categoria': categorias_arr,
            'cantidad': cantidades_arr,
            'precio_unitario': precios_arr,
            'descuento_pct': descuentos_arr,
            'vendedor_id': np.random.randint(1, 21, self.num_filas),
        }

        dataframe = pd.DataFrame(data)
        dataframe['total'] = (
            dataframe['cantidad'] * dataframe['precio_unitario'] *
            (1 - dataframe['descuento_pct'] / 100)
        ).round(2)

        dataframe = self._aplicar_nulos(dataframe, columnas_excluir=['fecha_venta', 'ticket_id'])
        return dataframe
