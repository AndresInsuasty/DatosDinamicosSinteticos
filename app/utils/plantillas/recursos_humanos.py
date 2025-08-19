import pandas as pd
import numpy as np
from faker import Faker
from .base import PlantillaBase

class PlantillaRecursosHumanos(PlantillaBase):
    
    @property
    def nombre(self) -> str:
        return "Recursos Humanos"
    
    @property
    def descripcion(self) -> str:
        return "Datos de empleados con salarios, departamentos, evaluaciones y métricas de RRHH"
    
    def generar(self) -> pd.DataFrame:
        fake = Faker(self.idioma)
        fake.seed_instance(self.semilla)
        np.random.seed(self.semilla)
        
        departamentos = ['IT', 'Ventas', 'Marketing', 'RRHH', 'Finanzas', 'Operaciones']
        niveles = ['Junior', 'Semi-Senior', 'Senior', 'Lead', 'Manager', 'Director']
        tipos_contrato = ['Tiempo Completo', 'Medio Tiempo', 'Contratista', 'Pasante']
        
        data = {
            'empleado_id': [f"EMP{fake.random_number(digits=4):04d}" for _ in range(self.num_filas)],
            'nombre': [fake.name() for _ in range(self.num_filas)],
            'email': [fake.email() for _ in range(self.num_filas)],
            'departamento': np.random.choice(departamentos, self.num_filas),
            'nivel': np.random.choice(niveles, self.num_filas, p=[0.3, 0.25, 0.2, 0.1, 0.1, 0.05]),
            'tipo_contrato': np.random.choice(tipos_contrato, self.num_filas, p=[0.7, 0.15, 0.1, 0.05]),
            'fecha_ingreso': [fake.date_between(start_date='-5y', end_date='today') 
                             for _ in range(self.num_filas)],
            'salario_anual': np.random.uniform(25000, 150000, self.num_filas).round(0),
            'evaluacion_desempeno': np.random.uniform(1, 5, self.num_filas).round(1),
            'dias_vacaciones_usados': np.random.randint(0, 30, self.num_filas),
            'horas_extras_mes': np.random.uniform(0, 40, self.num_filas).round(1),
            'edad': np.random.randint(22, 65, self.num_filas),
            'genero': np.random.choice(['M', 'F', 'Otro'], self.num_filas, p=[0.48, 0.48, 0.04]),
            'tiene_dependientes': np.random.choice([True, False], self.num_filas, p=[0.4, 0.6])
        }
        
        df = pd.DataFrame(data)
        # Calcular antigüedad en años
        df['antiguedad_anos'] = ((pd.Timestamp.now() - pd.to_datetime(df['fecha_ingreso'])).dt.days / 365.25).round(1)
        
        if self.porcentaje_nulos > 0:
            for col in ['evaluacion_desempeno', 'horas_extras_mes']:
                mask = np.random.random(self.num_filas) < (self.porcentaje_nulos / 100)
                df.loc[mask, col] = None
        
        return df
