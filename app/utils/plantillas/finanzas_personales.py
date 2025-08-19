import pandas as pd
import numpy as np
from faker import Faker
from .base import PlantillaBase

class PlantillaFinanzasPersonales(PlantillaBase):
    
    @property
    def nombre(self) -> str:
        return "Finanzas Personales"
    
    @property
    def descripcion(self) -> str:
        return "Datos financieros personales con ingresos, gastos, inversiones y análisis patrimonial"
    
    def generar(self) -> pd.DataFrame:
        fake = Faker(self.idioma)
        fake.seed_instance(self.semilla)
        np.random.seed(self.semilla)
        
        tipos_ingreso = ['Salario', 'Freelance', 'Inversiones', 'Negocio', 'Renta', 'Otros']
        tipos_gasto = ['Vivienda', 'Alimentación', 'Transporte', 'Salud', 'Educación', 'Entretenimiento']
        tipos_inversion = ['Acciones', 'Bonos', 'Fondos', 'Criptomonedas', 'Bienes Raíces', 'Efectivo']
        
        data = {
            'fecha': [fake.date_between(start_date='-2y', end_date='today') 
                     for _ in range(self.num_filas)],
            'usuario_id': [f"USR{fake.random_number(digits=5):05d}" for _ in range(self.num_filas)],
            'edad': np.random.randint(18, 70, self.num_filas),
            'ingresos_mensuales': np.random.uniform(1500, 15000, self.num_filas).round(2),
            'gastos_fijos': np.random.uniform(800, 8000, self.num_filas).round(2),
            'gastos_variables': np.random.uniform(200, 3000, self.num_filas).round(2),
            'ahorros_mes': np.random.uniform(0, 4000, self.num_filas).round(2),
            'deudas_total': np.random.uniform(0, 50000, self.num_filas).round(2),
            'score_crediticio': np.random.randint(300, 850, self.num_filas),
            'patrimonio_neto': np.random.uniform(-10000, 200000, self.num_filas).round(2),
            'tipo_vivienda': np.random.choice(['Propia', 'Alquilada', 'Familiar'], self.num_filas, p=[0.4, 0.5, 0.1]),
            'nivel_educacion': np.random.choice(['Secundaria', 'Técnico', 'Universitario', 'Posgrado'], 
                                              self.num_filas, p=[0.2, 0.3, 0.4, 0.1]),
            'inversion_principal': np.random.choice(tipos_inversion, self.num_filas),
            'emergency_fund_meses': np.random.uniform(0, 12, self.num_filas).round(1)
        }
        
        df = pd.DataFrame(data)
        df['ratio_ahorro'] = (df['ahorros_mes'] / df['ingresos_mensuales'] * 100).round(2)
        df['ratio_deuda_ingreso'] = (df['deudas_total'] / (df['ingresos_mensuales'] * 12) * 100).round(2)
        
        if self.porcentaje_nulos > 0:
            for col in ['deudas_total', 'emergency_fund_meses', 'patrimonio_neto']:
                mask = np.random.random(self.num_filas) < (self.porcentaje_nulos / 100)
                df.loc[mask, col] = None
        
        return df
