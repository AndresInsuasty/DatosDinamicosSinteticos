import pandas as pd
import numpy as np
from faker import Faker
from .base import PlantillaBase

class PlantillaMarketingDigital(PlantillaBase):
    
    @property
    def nombre(self) -> str:
        return "Marketing Digital"
    
    @property
    def descripcion(self) -> str:
        return "Métricas de campañas digitales con CTR, conversiones, costos y análisis de performance"
    
    def generar(self) -> pd.DataFrame:
        fake = Faker(self.idioma)
        fake.seed_instance(self.semilla)
        np.random.seed(self.semilla)
        
        plataformas = ['Google Ads', 'Facebook Ads', 'Instagram Ads', 'LinkedIn Ads', 'TikTok Ads', 'Twitter Ads']
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
        
        df = pd.DataFrame(data)
        df['ctr'] = (df['clicks'] / df['impresiones'] * 100).round(3)
        df['conversion_rate'] = (df['conversiones'] / df['clicks'] * 100).round(2)
        df['cpc'] = (df['costo_total'] / df['clicks']).round(2)
        df['cpa'] = np.where(df['conversiones'] > 0, (df['costo_total'] / df['conversiones']).round(2), 0)
        df['roas'] = np.where(df['costo_total'] > 0, (df['revenue_generado'] / df['costo_total']).round(2), 0)
        
        # Aplicar nulos si es necesario (excluir IDs y fechas críticas)
        df = self._aplicar_nulos(df, columnas_excluir=['fecha_campana', 'campana_id'])
        
        return df
        
        return df
