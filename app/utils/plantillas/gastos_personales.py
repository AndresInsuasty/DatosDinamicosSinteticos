import pandas as pd
import numpy as np
from faker import Faker
from .base import PlantillaBase

class PlantillaGastosPersonales(PlantillaBase):
    
    @property
    def nombre(self) -> str:
        return "Gastos Personales"
    
    @property
    def descripcion(self) -> str:
        return "Registro de gastos personales con categorías, montos y fechas"
    
    def generar(self) -> pd.DataFrame:
        fake = Faker(self.idioma)
        fake.seed_instance(self.semilla)
        np.random.seed(self.semilla)
        
        categorias = ['Alimentación', 'Transporte', 'Entretenimiento', 'Salud', 
                     'Educación', 'Ropa', 'Servicios', 'Otros']
        
        data = {
            'fecha': [fake.date_between(start_date='-1y', end_date='today') 
                     for _ in range(self.num_filas)],
            'categoria': np.random.choice(categorias, self.num_filas),
            'descripcion': [fake.sentence(nb_words=4) for _ in range(self.num_filas)],
            'monto': np.random.uniform(5, 500, self.num_filas).round(2),
            'metodo_pago': np.random.choice(['Efectivo', 'Tarjeta', 'Transferencia'], 
                                          self.num_filas),
            'es_recurrente': np.random.choice([True, False], self.num_filas, p=[0.3, 0.7])
        }
        
        df = pd.DataFrame(data)
        
        # Aplicar nulos si es necesario
        if self.porcentaje_nulos > 0:
            for col in ['descripcion']:  # Solo algunas columnas pueden tener nulos
                mask = np.random.random(self.num_filas) < (self.porcentaje_nulos / 100)
                df.loc[mask, col] = None
        
        return df
