"""Plantilla para generar datos sintéticos de logística y entregas."""

import pandas as pd
import numpy as np
from faker import Faker

from .base import PlantillaBase


class PlantillaLogisticaEntregas(PlantillaBase):
    """Plantilla para generar datos de logística y entregas."""

    @property
    def nombre(self) -> str:
        return "Logística y Entregas"

    @property
    def descripcion(self) -> str:
        return ("Seguimiento de pedidos y rutas de entrega. "
                "Tiempo de entrega, distancia y costo correlacionados con tipo de envío, "
                "destino y estado del pedido.")

    def generar(self) -> pd.DataFrame:
        fake = Faker(self.idioma)
        fake.seed_instance(self.semilla)
        np.random.seed(self.semilla)

        # Tipo de envío → (rango_distancia_km, plazo_dias, costo_base)
        config_envio = {
            'Express':       {'dist': (5,   200),  'plazo': (1, 3),   'costo': (12, 35)},
            'Estándar':      {'dist': (20,  800),  'plazo': (3, 8),   'costo': (5,  18)},
            'Económico':     {'dist': (50, 1500),  'plazo': (7, 21),  'costo': (2,  10)},
            'Internacional': {'dist': (500, 8000), 'plazo': (10, 41), 'costo': (25, 120)},
            'Mismo día':     {'dist': (1,    50),  'plazo': (1, 2),   'costo': (18, 50)},
        }
        estados = ['En preparación', 'Recogido', 'En tránsito', 'En reparto', 'Entregado',
                   'Intento fallido', 'Devuelto']
        vehiculos = ['Furgoneta', 'Camión pequeño', 'Moto', 'Camión grande', 'Avión cargo']
        categorias_producto = [
            'Electrónica', 'Ropa', 'Alimentación', 'Muebles', 'Documentos',
            'Farmacia', 'Deportes', 'Juguetes', 'Joyería', 'Industrial'
        ]

        tipos_envio = np.random.choice(
            list(config_envio.keys()), self.num_filas,
            p=[0.20, 0.45, 0.20, 0.08, 0.07]
        )

        distancia_km = np.array([
            round(np.random.uniform(*config_envio[t]['dist']), 1) for t in tipos_envio
        ])
        # Plazo prometido basado en tipo
        plazo_prometido = np.array([
            np.random.randint(*config_envio[t]['plazo']) for t in tipos_envio
        ])
        # Tiempo real: puede ser mayor o menor al prometido
        retraso = np.clip(
            np.random.normal(0, 1.5, self.num_filas), -1, 10
        ).round(0).astype(int)
        tiempo_entrega_dias = np.maximum(plazo_prometido + retraso, 1)

        # Costo de envío correlaciona con distancia y tipo
        costo_base = np.array([
            np.random.uniform(*config_envio[t]['costo']) for t in tipos_envio
        ])
        costo_envio = np.clip(
            costo_base + distancia_km * 0.012 +
            np.random.normal(0, 1.5, self.num_filas),
            1, 200
        ).round(2)

        # Peso del paquete (kg)
        peso_paquete = np.clip(
            np.random.exponential(5, self.num_filas), 0.1, 500
        ).round(2)

        # Estado del pedido correlaciona con días transcurridos desde creación
        fecha_pedido = [
            fake.date_between(start_date='-3m', end_date='today')
            for _ in range(self.num_filas)
        ]
        dias_desde_pedido = np.array([
            (pd.Timestamp.now().date() - f).days for f in fecha_pedido
        ])
        estado_arr = np.where(
            dias_desde_pedido == 0, 'En preparación',
            np.where(
                dias_desde_pedido <= 1, np.random.choice(
                    ['En preparación', 'Recogido', 'En tránsito'], self.num_filas
                ),
                np.where(
                    dias_desde_pedido >= tiempo_entrega_dias + 2,
                    np.random.choice(
                        ['Entregado', 'Devuelto', 'Intento fallido'],
                        self.num_filas, p=[0.85, 0.08, 0.07]
                    ),
                    np.random.choice(
                        ['En tránsito', 'En reparto', 'Entregado'],
                        self.num_filas, p=[0.50, 0.30, 0.20]
                    )
                )
            )
        )

        # Satisfacción del cliente: mayor si entrega en plazo o antes
        entrega_a_tiempo = tiempo_entrega_dias <= plazo_prometido
        satisfaccion = np.where(
            np.isin(estado_arr, ['Entregado']),
            np.where(
                entrega_a_tiempo,
                np.clip(np.random.normal(4.5, 0.5, self.num_filas), 1, 5).round(1),
                np.clip(np.random.normal(3.0, 0.8, self.num_filas), 1, 5).round(1)
            ),
            None
        )

        # Vehículo correlaciona con distancia y tipo de envío
        vehiculo_arr = np.where(
            tipos_envio == 'Internacional', 'Avión cargo',
            np.where(
                distancia_km > 500, 'Camión grande',
                np.where(
                    tipos_envio == 'Mismo día', 'Moto',
                    np.where(
                        peso_paquete > 50, 'Camión grande',
                        np.random.choice(['Furgoneta', 'Moto', 'Camión pequeño'],
                                         self.num_filas, p=[0.55, 0.25, 0.20])
                    )
                )
            )
        )

        data = {
            'envio_id': [f"ENV-{fake.random_number(digits=8):08d}" for _ in range(self.num_filas)],
            'fecha_pedido': fecha_pedido,
            'cliente_id': [f"CLI-{fake.random_number(digits=6):06d}" for _ in range(self.num_filas)],
            'tipo_envio': tipos_envio,
            'categoria_producto': np.random.choice(categorias_producto, self.num_filas),
            'peso_kg': peso_paquete,
            'distancia_km': distancia_km,
            'ciudad_origen': [fake.city() for _ in range(self.num_filas)],
            'ciudad_destino': [fake.city() for _ in range(self.num_filas)],
            'transportista': [f"TRANS-{np.random.randint(1, 21):02d}" for _ in range(self.num_filas)],
            'vehiculo': vehiculo_arr,
            'plazo_prometido_dias': plazo_prometido,
            'tiempo_real_dias': tiempo_entrega_dias,
            'costo_envio': costo_envio,
            'estado': estado_arr,
            'entrega_a_tiempo': entrega_a_tiempo,
            'satisfaccion_cliente': satisfaccion,
        }

        dataframe = pd.DataFrame(data)
        dataframe['retraso_dias'] = (
            dataframe['tiempo_real_dias'] - dataframe['plazo_prometido_dias']
        )

        dataframe = self._aplicar_nulos(
            dataframe, columnas_excluir=['envio_id', 'fecha_pedido', 'cliente_id']
        )
        return dataframe
