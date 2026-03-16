"""Plantilla para generar datos sintéticos de ventas de e-commerce."""

import pandas as pd
import numpy as np
from faker import Faker

from .base import PlantillaBase


class PlantillaVentasEcommerce(PlantillaBase):
    """Plantilla para generar datos de ventas de e-commerce."""

    @property
    def nombre(self) -> str:
        return "Ventas E-commerce"

    @property
    def descripcion(self) -> str:
        return ("Datos de ventas online con métricas de conversión y comportamiento. "
                "Canal, dispositivo y valor de pedido correlacionados con la categoría.")

    def generar(self) -> pd.DataFrame:
        fake = Faker(self.idioma)
        fake.seed_instance(self.semilla)
        np.random.seed(self.semilla)

        # Categoría → (rango_valor_pedido, rango_costo_adquisicion)
        config_categoria = {
            'Electrónicos': {'valor': (80,  800), 'cac': (8,  50)},
            'Ropa':         {'valor': (20,  200), 'cac': (3,  25)},
            'Hogar':        {'valor': (30,  400), 'cac': (4,  35)},
            'Deportes':     {'valor': (25,  300), 'cac': (4,  30)},
            'Libros':       {'valor': (8,    60), 'cac': (1,  10)},
            'Belleza':      {'valor': (15,  150), 'cac': (3,  20)},
            'Juguetes':     {'valor': (15,  200), 'cac': (3,  22)},
            'Alimentación': {'valor': (20,  120), 'cac': (2,  15)},
        }
        # Canal → distribución de dispositivos (Desktop, Mobile, Tablet)
        canal_dispositivo = {
            'Google Ads':  [0.50, 0.40, 0.10],
            'Facebook':    [0.25, 0.65, 0.10],
            'Instagram':   [0.15, 0.77, 0.08],
            'TikTok':      [0.10, 0.85, 0.05],
            'Email':       [0.60, 0.35, 0.05],
            'Orgánico':    [0.45, 0.45, 0.10],
            'Directo':     [0.55, 0.38, 0.07],
            'Referidos':   [0.40, 0.50, 0.10],
        }
        dispositivos = ['Desktop', 'Mobile', 'Tablet']
        canales = list(canal_dispositivo.keys())
        categorias = list(config_categoria.keys())

        canal_arr = np.random.choice(canales, self.num_filas)
        categoria_arr = np.random.choice(categorias, self.num_filas)

        dispositivo_arr = np.array([
            np.random.choice(dispositivos, p=canal_dispositivo[c]) for c in canal_arr
        ])
        valor_pedido = np.array([
            round(np.random.uniform(*config_categoria[c]['valor']), 2) for c in categoria_arr
        ])
        cac = np.array([
            round(np.random.uniform(*config_categoria[c]['cac']), 2) for c in categoria_arr
        ])
        # Tiempo en sitio y páginas vistas correlacionados entre sí
        paginas_vistas = np.random.randint(1, 16, self.num_filas)
        tiempo_en_sitio = np.clip(
            paginas_vistas * np.random.uniform(1.5, 4.0, self.num_filas) +
            np.random.normal(0, 2, self.num_filas),
            1, 90
        ).round(1)

        # Clientes nuevos tienen menor probabilidad en canales directos/email
        prob_nuevo = np.where(
            np.isin(canal_arr, ['Directo', 'Email']), 0.15, 0.35
        )
        es_nuevo = np.array([np.random.random() < p for p in prob_nuevo])

        # Descuento mayor en canales de paid media para atraer conversiones
        desc_base = np.where(
            np.isin(canal_arr, ['Google Ads', 'Facebook', 'Instagram', 'TikTok']),
            np.random.uniform(5, 30, self.num_filas),
            np.random.uniform(0, 15, self.num_filas)
        )
        descuento = np.clip(desc_base, 0, 40).round(2)

        data = {
            'fecha_pedido': [fake.date_between(start_date='-6m', end_date='today')
                             for _ in range(self.num_filas)],
            'pedido_id': [f"ORD-{fake.random_number(digits=8):08d}" for _ in range(self.num_filas)],
            'cliente_id': [f"CLI-{fake.random_number(digits=6):06d}" for _ in range(self.num_filas)],
            'canal_marketing': canal_arr,
            'dispositivo': dispositivo_arr,
            'categoria_producto': categoria_arr,
            'valor_pedido': valor_pedido,
            'costo_adquisicion': cac,
            'tiempo_en_sitio_min': tiempo_en_sitio,
            'paginas_vistas': paginas_vistas,
            'es_cliente_nuevo': es_nuevo,
            'pais': [fake.country() for _ in range(self.num_filas)],
            'descuento_aplicado': descuento,
        }

        dataframe = pd.DataFrame(data)
        dataframe['roi'] = (
            (dataframe['valor_pedido'] - dataframe['costo_adquisicion']) /
            dataframe['costo_adquisicion'] * 100
        ).round(2)

        dataframe = self._aplicar_nulos(
            dataframe, columnas_excluir=['fecha_pedido', 'pedido_id', 'cliente_id']
        )
        return dataframe
