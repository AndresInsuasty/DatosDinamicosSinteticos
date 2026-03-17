"""Plantilla para generar datos sintéticos de recursos humanos."""

import pandas as pd
import numpy as np
from faker import Faker

from .base import PlantillaBase


class PlantillaRecursosHumanos(PlantillaBase):
    """Plantilla para generar datos de recursos humanos."""

    @property
    def nombre(self) -> str:
        return "Recursos Humanos"

    @property
    def descripcion(self) -> str:
        return ("Datos de empleados con salarios, departamentos y métricas de RRHH. "
                "Salario, edad y tipo de contrato correlacionados con el nivel del empleado.")

    def generar(self) -> pd.DataFrame:
        fake = Faker(self.idioma)
        fake.seed_instance(self.semilla)
        np.random.seed(self.semilla)

        departamentos = ['IT', 'Ventas', 'Marketing', 'RRHH', 'Finanzas', 'Operaciones']

        # Nivel → (rango_salario_anual, rango_edad, prob_contrato_[TC, MT, CTR, PAS])
        config_nivel = {
            'Pasante':     {'salario': (12000,  22000),  'edad': (18, 25), 'contrato': [0.20, 0.30, 0.10, 0.40]},
            'Junior':      {'salario': (22000,  42000),  'edad': (22, 32), 'contrato': [0.70, 0.15, 0.10, 0.05]},
            'Semi-Senior': {'salario': (40000,  65000),  'edad': (26, 38), 'contrato': [0.80, 0.08, 0.10, 0.02]},
            'Senior':      {'salario': (62000,  95000),  'edad': (30, 48), 'contrato': [0.85, 0.05, 0.09, 0.01]},
            'Lead':        {'salario': (88000, 120000),  'edad': (34, 52), 'contrato': [0.90, 0.02, 0.07, 0.01]},
            'Manager':     {'salario': (105000, 155000), 'edad': (38, 58), 'contrato': [0.94, 0.01, 0.05, 0.00]},
            'Director':    {'salario': (140000, 220000), 'edad': (42, 65), 'contrato': [0.96, 0.01, 0.03, 0.00]},
        }
        tipos_contrato = ['Tiempo Completo', 'Medio Tiempo', 'Contratista', 'Pasante']

        niveles = np.random.choice(
            list(config_nivel.keys()),
            self.num_filas,
            p=[0.05, 0.25, 0.22, 0.20, 0.12, 0.10, 0.06]
        )

        salarios = np.array([
            round(np.random.uniform(*config_nivel[n]['salario']), 0)
            for n in niveles
        ])
        edades = np.array([
            np.random.randint(*config_nivel[n]['edad'])
            for n in niveles
        ])
        contratos = np.array([
            np.random.choice(tipos_contrato, p=config_nivel[n]['contrato'])
            for n in niveles
        ])
        # Evaluación: niveles más altos tienden a calificaciones mayores
        nivel_score = {
            'Pasante': 0, 'Junior': 1, 'Semi-Senior': 2,
            'Senior': 3, 'Lead': 4, 'Manager': 5, 'Director': 6
        }
        base_eval = np.array([nivel_score[n] * 0.2 + 2.5 for n in niveles])
        evaluaciones = np.clip(
            base_eval + np.random.normal(0, 0.6, self.num_filas), 1.0, 5.0
        ).round(1)

        # Horas extras: niveles altos trabajan más (pero no tanto como Juniors)
        horas_extras = np.clip(
            np.array([nivel_score[n] * 1.5 + 5 for n in niveles]) +
            np.random.normal(0, 6, self.num_filas),
            0, 60
        ).round(1)

        # Dependientes correlacionan con edad
        prob_dependientes = np.clip((edades - 22) / 80, 0.05, 0.75)
        tiene_dependientes = np.array([
            np.random.random() < p for p in prob_dependientes
        ])

        # Fecha de ingreso coherente con edad mínima laboral y empresa de max 10 años
        fechas_ingreso = []
        for edad in edades:
            max_anos = min(edad - 18, 10)
            if max_anos <= 0:
                max_anos = 1
            anos_atras = np.random.randint(0, max_anos + 1)
            fechas_ingreso.append(fake.date_between(
                start_date=f'-{max(anos_atras, 1)}y', end_date='today'
            ))

        data = {
            'empleado_id': [f"EMP{fake.random_number(digits=4):04d}" for _ in range(self.num_filas)],
            'nombre': [fake.name() for _ in range(self.num_filas)],
            'email': [fake.email() for _ in range(self.num_filas)],
            'departamento': np.random.choice(departamentos, self.num_filas),
            'nivel': niveles,
            'tipo_contrato': contratos,
            'fecha_ingreso': fechas_ingreso,
            'salario_anual': salarios,
            'evaluacion_desempeno': evaluaciones,
            'dias_vacaciones_usados': np.random.randint(0, 31, self.num_filas),
            'horas_extras_mes': horas_extras,
            'edad': edades,
            'genero': np.random.choice(['M', 'F', 'Otro'], self.num_filas, p=[0.48, 0.48, 0.04]),
            'tiene_dependientes': tiene_dependientes,
        }

        dataframe = pd.DataFrame(data)
        dataframe['antiguedad_anos'] = (
            (pd.Timestamp.now() - pd.to_datetime(dataframe['fecha_ingreso'])).dt.days / 365.25
        ).round(1)

        dataframe = self._aplicar_nulos(
            dataframe, columnas_excluir=['empleado_id', 'fecha_ingreso']
        )
        return dataframe
