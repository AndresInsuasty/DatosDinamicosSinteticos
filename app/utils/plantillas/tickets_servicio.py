"""Plantilla para generar datos sintéticos de tickets de servicio."""

import pandas as pd
import numpy as np
from faker import Faker

from .base import PlantillaBase


class PlantillaTicketsServicio(PlantillaBase):
    """Plantilla para generar datos de tickets de servicio."""

    @property
    def nombre(self) -> str:
        return "Tickets de Servicio"

    @property
    def descripcion(self) -> str:
        return ("Tickets de soporte técnico con estados, prioridades y asignaciones. "
                "Tiempo de resolución y estado correlacionados con la prioridad del ticket.")

    def generar(self) -> pd.DataFrame:
        fake = Faker(self.idioma)
        fake.seed_instance(self.semilla)
        np.random.seed(self.semilla)

        # Prioridad → (rango_horas_resolución, distribución_estado)
        config_prioridad = {
            'Crítica': {
                'horas': (0.5, 4.0),
                'estado_p': [0.10, 0.30, 0.40, 0.20],   # Abierto, En Progreso, Resuelto, Cerrado
            },
            'Alta': {
                'horas': (2.0, 24.0),
                'estado_p': [0.15, 0.35, 0.30, 0.20],
            },
            'Media': {
                'horas': (8.0, 72.0),
                'estado_p': [0.25, 0.30, 0.25, 0.20],
            },
            'Baja': {
                'horas': (24.0, 168.0),
                'estado_p': [0.35, 0.25, 0.20, 0.20],
            },
        }
        estados = ['Abierto', 'En Progreso', 'Resuelto', 'Cerrado']

        prioridades = np.random.choice(
            ['Baja', 'Media', 'Alta', 'Crítica'],
            self.num_filas,
            p=[0.40, 0.30, 0.20, 0.10]
        )
        horas_resolucion = np.array([
            round(np.random.uniform(*config_prioridad[p]['horas']), 1)
            for p in prioridades
        ])
        estado_arr = np.array([
            np.random.choice(estados, p=config_prioridad[p]['estado_p'])
            for p in prioridades
        ])
        # Tickets resueltos/cerrados tienen fecha de cierre coherente
        fecha_creacion = [
            fake.date_between(start_date='-3m', end_date='today')
            for _ in range(self.num_filas)
        ]

        data = {
            'ticket_id': [f"TCK-{fake.random_number(digits=5):05d}" for _ in range(self.num_filas)],
            'fecha_creacion': fecha_creacion,
            'cliente': [fake.company() for _ in range(self.num_filas)],
            'asunto': [fake.sentence(nb_words=6) for _ in range(self.num_filas)],
            'categoria': np.random.choice(
                ['Hardware', 'Software', 'Red', 'Email', 'Acceso', 'Base de Datos'],
                self.num_filas,
                p=[0.20, 0.30, 0.20, 0.10, 0.10, 0.10]
            ),
            'prioridad': prioridades,
            'estado': estado_arr,
            'asignado_a': [fake.name() for _ in range(self.num_filas)],
            'tiempo_resolucion_hrs': horas_resolucion,
            'satisfaccion_cliente': np.where(
                np.isin(estado_arr, ['Resuelto', 'Cerrado']),
                np.random.randint(1, 6, self.num_filas),   # 1-5 solo si resuelto
                None
            ),
        }

        dataframe = pd.DataFrame(data)
        dataframe = self._aplicar_nulos(
            dataframe, columnas_excluir=['ticket_id', 'fecha_creacion']
        )
        return dataframe
