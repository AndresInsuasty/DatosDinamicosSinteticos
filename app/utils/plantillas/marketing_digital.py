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
        return ("Métricas de campañas digitales con CTR, conversiones, "
                "costos y análisis de performance")

    def generar(self) -> pd.DataFrame:
        fake = Faker(self.idioma)
        fake.seed_instance(self.semilla)
        np.random.seed(self.semilla)

        plataformas = ['Google Ads', 'Facebook Ads', 'Instagram Ads',
                      'LinkedIn Ads', 'TikTok Ads', 'Twitter Ads']
        tipos_campana = ['Awareness', 'Conversion', 'Traffic', 'Engagement', 'Lead Generation']
        audiencias = ['18-24', '25-34', '35-44', '45-54', '55+']

        data = {
            'fecha_campana': [fake.date_between(start_date='-1y', end_date='today')
                             for _ in range(self.num_filas)],
            'campana_id': [f"CAMP-{fake.random_number(digits=6)}" for _ in range(self.num_filas)],
            'plataforma': np.random.choice(plataformas, self.num_filas),
            'tipo_campana': np.random.choice(tipos_campana, self.num_filas),
            'audiencia_objetivo': np.random.choice(audiencias, self.num_filas),
            'presupuesto_diario': np.random.uniform(10, 1000, self.num_filas).round(2),
            'impresiones': np.random.randint(1000, 100000, self.num_filas),
            'clicks': np.random.randint(10, 5000, self.num_filas),
            'conversiones': np.random.randint(0, 200, self.num_filas),
            'costo_total': np.random.uniform(50, 2000, self.num_filas).round(2),
            'revenue_generado': np.random.uniform(0, 8000, self.num_filas).round(2),
            'alcance': np.random.randint(500, 80000, self.num_filas),
            'engagement_rate': np.random.uniform(0.5, 15, self.num_filas).round(2),
            'tiempo_conversion_hrs': np.random.uniform(0.1, 168, self.num_filas).round(1)
        }

        dataframe = pd.DataFrame(data)
        dataframe['ctr'] = (dataframe['clicks'] / dataframe['impresiones'] * 100).round(3)
        dataframe['conversion_rate'] = (dataframe['conversiones'] /
                                      dataframe['clicks'] * 100).round(2)
        dataframe['cpc'] = (dataframe['costo_total'] / dataframe['clicks']).round(2)
        dataframe['cpa'] = np.where(dataframe['conversiones'] > 0,
                                  (dataframe['costo_total'] / dataframe['conversiones']).round(2), 0)
        dataframe['roas'] = np.where(dataframe['costo_total'] > 0,
                                   (dataframe['revenue_generado'] / dataframe['costo_total']).round(2), 0)

        # Aplicar nulos si es necesario (excluir IDs y fechas críticas)
        dataframe = self._aplicar_nulos(dataframe, columnas_excluir=['fecha_campana', 'campana_id'])

        return dataframe
