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
        return ("Datos académicos de estudiantes con calificaciones, "
                "asistencia y métricas educativas")

    def generar(self) -> pd.DataFrame:
        fake = Faker(self.idioma)
        fake.seed_instance(self.semilla)
        np.random.seed(self.semilla)

        materias = ['Matemáticas', 'Ciencias', 'Historia', 'Literatura', 'Arte', 'Educación Física']
        niveles = ['Primaria', 'Secundaria', 'Preparatoria', 'Universidad']
        modalidades = ['Presencial', 'Virtual', 'Híbrida']

        data = {
            'estudiante_id': [f"EST{fake.random_number(digits=6):06d}" for _ in range(self.num_filas)],
            'nombre': [fake.name() for _ in range(self.num_filas)],
            'edad': np.random.randint(6, 25, self.num_filas),
            'nivel_educativo': np.random.choice(niveles, self.num_filas),
            'materia': np.random.choice(materias, self.num_filas),
            'semestre_periodo': [f"{fake.year()}-{np.random.choice(['1', '2'])}"
                               for _ in range(self.num_filas)],
            'calificacion_final': np.random.uniform(0, 100, self.num_filas).round(1),
            'asistencia_pct': np.random.uniform(60, 100, self.num_filas).round(1),
            'participacion_clase': np.random.uniform(1, 10, self.num_filas).round(1),
            'tareas_entregadas': np.random.randint(8, 20, self.num_filas),
            'tareas_totales': np.random.randint(15, 25, self.num_filas),
            'horas_estudio_semana': np.random.uniform(2, 40, self.num_filas).round(1),
            'modalidad': np.random.choice(modalidades, self.num_filas, p=[0.6, 0.3, 0.1]),
            'beca': np.random.choice([True, False], self.num_filas, p=[0.2, 0.8]),
            'nivel_socioeconomico': np.random.choice(['Bajo', 'Medio', 'Alto'],
                                                   self.num_filas, p=[0.3, 0.5, 0.2]),
            'actividades_extracurriculares': np.random.randint(0, 5, self.num_filas)
        }

        dataframe = pd.DataFrame(data)
        dataframe['pct_tareas_entregadas'] = (dataframe['tareas_entregadas'] /
                                            dataframe['tareas_totales'] * 100).round(1)
        dataframe['categoria_rendimiento'] = pd.cut(dataframe['calificacion_final'],
                                                   bins=[0, 60, 70, 80, 90, 100],
                                                   labels=['Insuficiente', 'Regular', 'Bueno',
                                                          'Muy Bueno', 'Excelente'])

        # Aplicar nulos si es necesario (excluir IDs críticos)
        dataframe = self._aplicar_nulos(dataframe, columnas_excluir=['estudiante_id'])

        return dataframe
