"""Plantilla para generar datos sintéticos de historial clínico."""

import pandas as pd
import numpy as np
from faker import Faker

from .base import PlantillaBase


class PlantillaHistorialClinico(PlantillaBase):
    """Plantilla para generar datos de historial clínico de pacientes."""

    @property
    def nombre(self) -> str:
        return "Historial Clínico"

    @property
    def descripcion(self) -> str:
        return ("Registros médicos de pacientes con diagnósticos y métricas de salud. "
                "IMC, presión arterial y glucosa correlacionados con edad, peso y diagnósticos.")

    def generar(self) -> pd.DataFrame:
        fake = Faker(self.idioma)
        fake.seed_instance(self.semilla)
        np.random.seed(self.semilla)

        grupos_sanguineos = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
        especialidades = [
            'Medicina General', 'Cardiología', 'Endocrinología', 'Traumatología',
            'Pediatría', 'Ginecología', 'Neurología', 'Dermatología',
        ]
        diagnosticos_principales = [
            'Hipertensión arterial', 'Diabetes tipo 2', 'Obesidad',
            'Lumbalgia', 'Gastritis', 'Ansiedad', 'Hipotiroidismo',
            'Artrosis', 'Asma', 'Sin diagnóstico relevante',
        ]
        estados_civiles = ['Soltero/a', 'Casado/a', 'Divorciado/a', 'Viudo/a', 'Unión libre']

        genero = np.random.choice(['M', 'F'], self.num_filas, p=[0.49, 0.51])
        # Edad con distribución realista (más adultos que niños)
        edad = np.clip(
            np.random.choice(
                range(1, 91),
                self.num_filas,
                p=self._distribucion_edad()
            ), 1, 90
        )

        # Talla (cm): correlaciona con género y edad
        talla_base = np.where(genero == 'M', 175, 162)
        talla = np.clip(
            talla_base + np.random.normal(0, 8, self.num_filas), 50, 210
        ).round(1)

        # Peso (kg): correlaciona con talla, edad y género
        peso_ideal = (talla - 100) * np.where(genero == 'M', 0.9, 0.85)
        peso = np.clip(
            peso_ideal * np.random.uniform(0.75, 1.45, self.num_filas) +
            (edad - 30) * 0.15 +
            np.random.normal(0, 5, self.num_filas),
            10, 200
        ).round(1)

        # IMC derivado
        imc = (peso / (talla / 100) ** 2).round(2)

        # Presión arterial sistólica: correlaciona con edad, IMC y peso
        pas_base = 100 + edad * 0.5 + (imc - 22) * 1.2
        pas = np.clip(
            pas_base + np.random.normal(0, 12, self.num_filas), 80, 220
        ).round(0).astype(int)
        # Diastólica: ~60-65% de la sistólica con ruido
        pad = np.clip(
            pas * np.random.uniform(0.55, 0.68, self.num_filas) +
            np.random.normal(0, 5, self.num_filas),
            50, 130
        ).round(0).astype(int)

        # Glucosa en ayunas (mg/dL): correlaciona con IMC y edad
        glucosa = np.clip(
            80 + (imc - 22) * 2.5 + (edad - 30) * 0.4 +
            np.random.normal(0, 15, self.num_filas),
            60, 400
        ).round(0).astype(int)

        # Colesterol total (mg/dL): correlaciona con edad e IMC
        colesterol = np.clip(
            150 + (imc - 22) * 3 + edad * 0.8 +
            np.random.normal(0, 25, self.num_filas),
            100, 380
        ).round(0).astype(int)

        # Frecuencia cardíaca (lpm)
        frec_cardiaca = np.clip(
            75 - edad * 0.1 + np.random.normal(0, 10, self.num_filas), 45, 130
        ).round(0).astype(int)

        # Diagnóstico correlaciona con métricas
        diagnostico = np.where(
            pas > 140, 'Hipertensión arterial',
            np.where(glucosa > 126, 'Diabetes tipo 2',
            np.where(imc > 30, 'Obesidad',
            np.random.choice(diagnosticos_principales, self.num_filas)))
        )

        # Días de estancia: correlaciona con diagnóstico y gravedad
        dias_estancia = np.where(
            np.isin(diagnostico, ['Diabetes tipo 2', 'Hipertensión arterial']),
            np.random.randint(1, 6, self.num_filas),
            np.where(
                diagnostico == 'Obesidad',
                np.random.randint(0, 4, self.num_filas),
                np.random.randint(0, 3, self.num_filas)
            )
        )

        data = {
            'paciente_id': [f"PAC-{fake.random_number(digits=7):07d}" for _ in range(self.num_filas)],
            'fecha_consulta': [
                fake.date_between(start_date='-2y', end_date='today')
                for _ in range(self.num_filas)
            ],
            'nombre': [fake.name() for _ in range(self.num_filas)],
            'edad': edad,
            'genero': genero,
            'estado_civil': np.random.choice(
                estados_civiles, self.num_filas, p=[0.35, 0.40, 0.10, 0.07, 0.08]
            ),
            'grupo_sanguineo': np.random.choice(
                grupos_sanguineos, self.num_filas, p=[0.36, 0.06, 0.08, 0.02, 0.03, 0.01, 0.38, 0.06]
            ),
            'especialidad': np.random.choice(especialidades, self.num_filas),
            'peso_kg': peso,
            'talla_cm': talla,
            'imc': imc,
            'presion_sistolica': pas,
            'presion_diastolica': pad,
            'glucosa_mg_dl': glucosa,
            'colesterol_total': colesterol,
            'frecuencia_cardiaca': frec_cardiaca,
            'diagnostico_principal': diagnostico,
            'dias_estancia': dias_estancia,
            'fumador': np.random.choice([True, False], self.num_filas, p=[0.22, 0.78]),
            'actividad_fisica': np.random.choice(
                ['Sedentario', 'Leve', 'Moderada', 'Intensa'],
                self.num_filas, p=[0.30, 0.35, 0.25, 0.10]
            ),
        }

        dataframe = pd.DataFrame(data)
        dataframe['categoria_imc'] = pd.cut(
            dataframe['imc'],
            bins=[0, 18.5, 25, 30, 35, 100],
            labels=['Bajo peso', 'Normal', 'Sobrepeso', 'Obesidad I', 'Obesidad II+'],
            include_lowest=True
        )
        dataframe['hipertension'] = dataframe['presion_sistolica'] >= 140

        dataframe = self._aplicar_nulos(
            dataframe, columnas_excluir=['paciente_id', 'fecha_consulta']
        )
        return dataframe

    @staticmethod
    def _distribucion_edad():
        """Genera una distribución de probabilidades por edad (1-90)."""
        edades = np.arange(1, 91)
        # Pico en adultos 30-60, menos niños y ancianos
        pesos = np.exp(-((edades - 42) ** 2) / (2 * 20 ** 2))
        pesos += 0.003  # base mínima para todas las edades
        return (pesos / pesos.sum()).tolist()
