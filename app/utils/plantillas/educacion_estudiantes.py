"""Plantilla para generar datos sintéticos de educación de estudiantes."""

import pandas as pd
import numpy as np
from faker import Faker

from .base import PlantillaBase


class PlantillaEducacionEstudiantes(PlantillaBase):
    """Plantilla para generar datos de educación de estudiantes."""

    @property
    def nombre(self) -> str:
        return "Educación - Estudiantes"

    @property
    def descripcion(self) -> str:
        return ("Datos académicos de estudiantes con calificaciones y métricas educativas. "
                "Edad, calificación y asistencia correlacionadas con nivel educativo y horas de estudio.")

    def generar(self) -> pd.DataFrame:
        fake = Faker(self.idioma)
        fake.seed_instance(self.semilla)
        np.random.seed(self.semilla)

        # Nivel → (rango_edad, rango_horas_estudio, media_calificacion)
        config_nivel = {
            'Primaria':     {'edad': (6,  12),  'estudio': (1, 8),   'cal_mu': 75},
            'Secundaria':   {'edad': (12, 16),  'estudio': (3, 15),  'cal_mu': 68},
            'Preparatoria': {'edad': (15, 19),  'estudio': (5, 20),  'cal_mu': 65},
            'Universidad':  {'edad': (18, 26),  'estudio': (8, 40),  'cal_mu': 70},
            'Posgrado':     {'edad': (22, 40),  'estudio': (15, 50), 'cal_mu': 78},
        }
        materias = ['Matemáticas', 'Ciencias', 'Historia', 'Literatura', 'Arte',
                    'Educación Física', 'Inglés', 'Programación', 'Química', 'Biología']
        modalidades = ['Presencial', 'Virtual', 'Híbrida']

        niveles = np.random.choice(
            list(config_nivel.keys()), self.num_filas,
            p=[0.15, 0.20, 0.25, 0.30, 0.10]
        )
        edades = np.array([
            np.random.randint(*config_nivel[n]['edad']) for n in niveles
        ])
        horas_estudio = np.clip(
            np.array([np.random.uniform(*config_nivel[n]['estudio']) for n in niveles]) +
            np.random.normal(0, 2, self.num_filas),
            1, 60
        ).round(1)

        # Calificación correlaciona positivamente con horas de estudio y asistencia
        asistencia_pct = np.clip(
            np.random.normal(82, 12, self.num_filas), 40, 100
        ).round(1)

        cal_base = np.array([config_nivel[n]['cal_mu'] for n in niveles])
        calificacion = np.clip(
            cal_base +
            (horas_estudio - horas_estudio.mean()) * 0.8 +
            (asistencia_pct - 80) * 0.3 +
            np.random.normal(0, 8, self.num_filas),
            0, 100
        ).round(1)

        # Tareas: entregadas siempre <= totales
        tareas_totales = np.random.randint(10, 26, self.num_filas)
        # Proporción de entrega correlaciona con calificación
        prop_entrega = np.clip(
            0.5 + calificacion / 200 + np.random.normal(0, 0.1, self.num_filas),
            0.3, 1.0
        )
        tareas_entregadas = np.clip(
            (tareas_totales * prop_entrega).astype(int), 0, tareas_totales
        )

        # Beca: nivel socioeconómico bajo tiene mayor probabilidad
        nivel_socio = np.random.choice(
            ['Bajo', 'Medio', 'Alto'], self.num_filas, p=[0.30, 0.50, 0.20]
        )
        prob_beca = np.where(
            nivel_socio == 'Bajo', 0.45,
            np.where(nivel_socio == 'Medio', 0.15, 0.04)
        )
        tiene_beca = np.array([np.random.random() < p for p in prob_beca])

        data = {
            'estudiante_id': [f"EST{fake.random_number(digits=6):06d}" for _ in range(self.num_filas)],
            'nombre': [fake.name() for _ in range(self.num_filas)],
            'edad': edades,
            'nivel_educativo': niveles,
            'materia': np.random.choice(materias, self.num_filas),
            'semestre_periodo': [
                f"{np.random.choice(range(2020, 2026))}-{np.random.choice(['1', '2'])}"
                for _ in range(self.num_filas)
            ],
            'calificacion_final': calificacion,
            'asistencia_pct': asistencia_pct,
            'participacion_clase': np.clip(
                calificacion / 12 + np.random.normal(0, 1.5, self.num_filas), 1, 10
            ).round(1),
            'tareas_entregadas': tareas_entregadas,
            'tareas_totales': tareas_totales,
            'horas_estudio_semana': horas_estudio,
            'modalidad': np.random.choice(modalidades, self.num_filas, p=[0.55, 0.30, 0.15]),
            'beca': tiene_beca,
            'nivel_socioeconomico': nivel_socio,
            'actividades_extracurriculares': np.random.randint(0, 6, self.num_filas),
        }

        dataframe = pd.DataFrame(data)
        dataframe['pct_tareas_entregadas'] = (
            dataframe['tareas_entregadas'] / dataframe['tareas_totales'] * 100
        ).round(1)
        dataframe['categoria_rendimiento'] = pd.cut(
            dataframe['calificacion_final'],
            bins=[0, 60, 70, 80, 90, 100],
            labels=['Insuficiente', 'Regular', 'Bueno', 'Muy Bueno', 'Excelente'],
            include_lowest=True
        )

        dataframe = self._aplicar_nulos(dataframe, columnas_excluir=['estudiante_id'])
        return dataframe
