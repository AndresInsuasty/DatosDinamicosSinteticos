"""Plantilla para generar datos sintéticos de marketing digital."""

import pandas as pd
import numpy as np
from faker import Faker

from .base import PlantillaBase


class PlantillaMarketingDigital(PlantillaBase):
    """Plantilla para generar datos de marketing digital."""

    @property
    def nombre(self) -> str:
        return "Marketing Digital"

    @property
    def descripcion(self) -> str:
        return ("Métricas de campañas digitales con CTR, conversiones y ROAS. "
                "Clicks, conversiones y costos coherentemente derivados de impresiones y presupuesto.")

    def generar(self) -> pd.DataFrame:
        fake = Faker(self.idioma)
        fake.seed_instance(self.semilla)
        np.random.seed(self.semilla)

        # Plataforma → (CTR_medio, conv_rate_medio, cpc_rango)
        config_plataforma = {
            'Google Ads':    {'ctr_mu': 3.5,  'cvr_mu': 4.0,  'cpc': (0.30, 3.50)},
            'Facebook Ads':  {'ctr_mu': 1.2,  'cvr_mu': 2.5,  'cpc': (0.20, 2.00)},
            'Instagram Ads': {'ctr_mu': 0.8,  'cvr_mu': 1.8,  'cpc': (0.25, 2.50)},
            'LinkedIn Ads':  {'ctr_mu': 0.5,  'cvr_mu': 3.5,  'cpc': (3.00, 12.00)},
            'TikTok Ads':    {'ctr_mu': 1.5,  'cvr_mu': 1.5,  'cpc': (0.10, 1.50)},
            'Twitter Ads':   {'ctr_mu': 0.9,  'cvr_mu': 1.2,  'cpc': (0.30, 2.00)},
            'YouTube Ads':   {'ctr_mu': 0.6,  'cvr_mu': 2.0,  'cpc': (0.10, 1.80)},
        }
        tipos_campana = ['Awareness', 'Conversión', 'Tráfico', 'Engagement', 'Lead Generation', 'Remarketing']
        audiencias = ['18-24', '25-34', '35-44', '45-54', '55+']

        plataformas = list(config_plataforma.keys())
        plat_arr = np.random.choice(plataformas, self.num_filas)

        # Presupuesto diario y duración de campaña
        presupuesto_diario = np.random.uniform(10, 1000, self.num_filas).round(2)
        duracion_dias = np.random.randint(1, 91, self.num_filas)
        costo_total = (presupuesto_diario * duracion_dias *
                       np.random.uniform(0.60, 1.0, self.num_filas)).round(2)

        # Impresiones derivadas del costo y CPC estimado
        cpc_est = np.array([
            np.random.uniform(*config_plataforma[p]['cpc']) for p in plat_arr
        ])
        impresiones = np.maximum(
            (costo_total / cpc_est / (
                np.clip(np.array([config_plataforma[p]['ctr_mu'] for p in plat_arr]), 0.3, 10) / 100
            )).astype(int),
            1000
        )

        # Clicks: CTR con varianza alrededor del promedio de la plataforma
        ctr_real = np.clip(
            np.array([config_plataforma[p]['ctr_mu'] for p in plat_arr]) +
            np.random.normal(0, 0.8, self.num_filas),
            0.1, 20
        )
        clicks = np.maximum(
            (impresiones * ctr_real / 100).astype(int), 1
        )

        # Conversiones: tasa de conversión con varianza
        cvr_real = np.clip(
            np.array([config_plataforma[p]['cvr_mu'] for p in plat_arr]) +
            np.random.normal(0, 0.7, self.num_filas),
            0.1, 15
        )
        conversiones = np.maximum(
            (clicks * cvr_real / 100).astype(int), 0
        )

        # Revenue: cada conversión genera entre 5 y 200 USD en promedio por tipo de campaña
        tipo_campana_arr = np.random.choice(tipos_campana, self.num_filas)
        revenue_por_conv = np.where(
            tipo_campana_arr == 'Awareness', np.random.uniform(0, 5, self.num_filas),
            np.where(
                tipo_campana_arr == 'Engagement', np.random.uniform(0, 10, self.num_filas),
                np.random.uniform(15, 250, self.num_filas)
            )
        )
        revenue = np.clip(
            conversiones * revenue_por_conv + np.random.normal(0, 50, self.num_filas), 0, None
        ).round(2)

        alcance = (impresiones * np.random.uniform(0.60, 0.90, self.num_filas)).astype(int)
        engagement_rate = np.clip(
            np.random.normal(3.5, 2.0, self.num_filas), 0.1, 20
        ).round(2)

        data = {
            'fecha_campana': [fake.date_between(start_date='-1y', end_date='today')
                              for _ in range(self.num_filas)],
            'campana_id': [f"CAMP-{fake.random_number(digits=6):06d}" for _ in range(self.num_filas)],
            'plataforma': plat_arr,
            'tipo_campana': tipo_campana_arr,
            'audiencia_objetivo': np.random.choice(audiencias, self.num_filas),
            'duracion_dias': duracion_dias,
            'presupuesto_diario': presupuesto_diario,
            'impresiones': impresiones,
            'clicks': clicks,
            'conversiones': conversiones,
            'costo_total': costo_total,
            'revenue_generado': revenue,
            'alcance': alcance,
            'engagement_rate': engagement_rate,
            'tiempo_conversion_hrs': np.random.exponential(24, self.num_filas).round(1),
        }

        dataframe = pd.DataFrame(data)
        dataframe['ctr'] = (dataframe['clicks'] / dataframe['impresiones'] * 100).round(3)
        dataframe['conversion_rate'] = np.where(
            dataframe['clicks'] > 0,
            (dataframe['conversiones'] / dataframe['clicks'] * 100).round(2), 0
        )
        dataframe['cpc'] = (dataframe['costo_total'] / dataframe['clicks']).round(2)
        dataframe['cpa'] = np.where(
            dataframe['conversiones'] > 0,
            (dataframe['costo_total'] / dataframe['conversiones']).round(2), 0
        )
        dataframe['roas'] = np.where(
            dataframe['costo_total'] > 0,
            (dataframe['revenue_generado'] / dataframe['costo_total']).round(2), 0
        )

        dataframe = self._aplicar_nulos(
            dataframe, columnas_excluir=['fecha_campana', 'campana_id']
        )
        return dataframe
