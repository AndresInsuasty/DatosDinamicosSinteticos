"""Plantilla para generar datos sintéticos de finanzas personales."""

import pandas as pd
import numpy as np
from faker import Faker

from .base import PlantillaBase


class PlantillaFinanzasPersonales(PlantillaBase):
    """Plantilla para generar datos de finanzas personales."""

    @property
    def nombre(self) -> str:
        return "Finanzas Personales"

    @property
    def descripcion(self) -> str:
        return ("Datos financieros personales con ingresos, gastos e inversiones. "
                "Gastos, ahorros y deudas correlacionados con nivel educativo e ingresos.")

    def generar(self) -> pd.DataFrame:
        fake = Faker(self.idioma)
        fake.seed_instance(self.semilla)
        np.random.seed(self.semilla)

        # Nivel educativo → rango de ingresos mensuales
        config_educacion = {
            'Secundaria':    (800,   3000),
            'Técnico':       (1200,  5000),
            'Universitario': (2500,  9000),
            'Posgrado':      (5000, 18000),
        }
        tipos_inversion = ['Acciones', 'Bonos', 'Fondos', 'Criptomonedas', 'Bienes Raíces', 'Efectivo']
        tipos_vivienda = ['Propia', 'Alquilada', 'Familiar']

        nivel_edu = np.random.choice(
            list(config_educacion.keys()), self.num_filas, p=[0.20, 0.30, 0.40, 0.10]
        )
        edades = np.random.randint(22, 70, self.num_filas)

        ingresos = np.array([
            round(np.random.uniform(*config_educacion[e]) * (1 + (a - 22) * 0.008), 2)
            for e, a in zip(nivel_edu, edades)
        ])

        # Gastos fijos: 35-55% de ingresos
        ratio_fijos = np.random.uniform(0.35, 0.55, self.num_filas)
        gastos_fijos = (ingresos * ratio_fijos).round(2)

        # Gastos variables: 15-30% de ingresos
        ratio_variables = np.random.uniform(0.15, 0.30, self.num_filas)
        gastos_variables = (ingresos * ratio_variables).round(2)

        # Ahorros: lo que queda después de gastos, con algo de ruido (puede ser negativo)
        ahorro_base = ingresos - gastos_fijos - gastos_variables
        ruido_ahorro = np.random.normal(0, ingresos * 0.05, self.num_filas)
        ahorros = np.clip(ahorro_base + ruido_ahorro, 0, ingresos * 0.50).round(2)

        # Deudas: correlacionan inversamente con ingresos y ahorros
        max_deuda = np.clip(ingresos * 24 * (1 - ahorros / ingresos * 2), 0, ingresos * 36)
        deudas = np.array([
            round(np.random.uniform(0, max(md, 1)), 2) for md in max_deuda
        ])

        # Score crediticio: alto ingreso + bajas deudas → mejor score
        ratio_deuda_ing = np.where(ingresos > 0, deudas / (ingresos * 12), 1.0)
        score_base = 750 - ratio_deuda_ing * 250 + (ahorros / ingresos) * 80
        score_crediticio = np.clip(
            score_base + np.random.normal(0, 30, self.num_filas), 300, 850
        ).round(0).astype(int)

        # Patrimonio neto: más alto para personas con ingresos altos y pocos gastos
        patrimonio = np.clip(
            ahorros * 12 * np.random.uniform(1, 5, self.num_filas) - deudas +
            np.random.normal(0, 5000, self.num_filas),
            -20000, 500000
        ).round(2)

        # Inversión: personas de mayor nivel educativo / ingresos prefieren activos
        inv_pesos = {
            'Secundaria':    [0.05, 0.10, 0.15, 0.10, 0.10, 0.50],
            'Técnico':       [0.10, 0.15, 0.20, 0.15, 0.15, 0.25],
            'Universitario': [0.20, 0.15, 0.25, 0.15, 0.15, 0.10],
            'Posgrado':      [0.30, 0.20, 0.20, 0.10, 0.15, 0.05],
        }
        inversion_principal = np.array([
            np.random.choice(tipos_inversion, p=inv_pesos[e]) for e in nivel_edu
        ])

        # Fondo de emergencia: más meses para quienes tienen mayor ratio de ahorro
        ratio_ahorro_norm = np.clip(ahorros / ingresos, 0, 0.5)
        emergency_fund = np.clip(
            ratio_ahorro_norm * 24 + np.random.normal(0, 1.5, self.num_filas), 0, 18
        ).round(1)

        data = {
            'fecha': [fake.date_between(start_date='-2y', end_date='today')
                      for _ in range(self.num_filas)],
            'usuario_id': [f"USR{fake.random_number(digits=5):05d}" for _ in range(self.num_filas)],
            'edad': edades,
            'nivel_educacion': nivel_edu,
            'ingresos_mensuales': ingresos,
            'gastos_fijos': gastos_fijos,
            'gastos_variables': gastos_variables,
            'ahorros_mes': ahorros,
            'deudas_total': deudas,
            'score_crediticio': score_crediticio,
            'patrimonio_neto': patrimonio,
            'tipo_vivienda': np.random.choice(tipos_vivienda, self.num_filas, p=[0.40, 0.50, 0.10]),
            'inversion_principal': inversion_principal,
            'emergency_fund_meses': emergency_fund,
        }

        dataframe = pd.DataFrame(data)
        dataframe['ratio_ahorro'] = (dataframe['ahorros_mes'] /
                                     dataframe['ingresos_mensuales'] * 100).round(2)
        dataframe['ratio_deuda_ingreso'] = (dataframe['deudas_total'] /
                                            (dataframe['ingresos_mensuales'] * 12) * 100).round(2)

        dataframe = self._aplicar_nulos(dataframe, columnas_excluir=['fecha', 'usuario_id'])
        return dataframe
