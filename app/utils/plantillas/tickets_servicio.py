import pandas as pd
import numpy as np
from faker import Faker
from .base import PlantillaBase

class PlantillaTicketsServicio(PlantillaBase):
    
    @property
    def nombre(self) -> str:
        return "Tickets de Servicio"
    
    @property
    def descripcion(self) -> str:
        return "Tickets de soporte técnico con estados, prioridades y asignaciones"
    
    def generar(self) -> pd.DataFrame:
        fake = Faker(self.idioma)
        fake.seed_instance(self.semilla)
        np.random.seed(self.semilla)
        
        data = {
            'ticket_id': [f"TCK-{fake.random_number(digits=5)}" for _ in range(self.num_filas)],
            'fecha_creacion': [fake.date_between(start_date='-3m', end_date='today') 
                              for _ in range(self.num_filas)],
            'cliente': [fake.company() for _ in range(self.num_filas)],
            'asunto': [fake.sentence(nb_words=6) for _ in range(self.num_filas)],
            'categoria': np.random.choice(['Hardware', 'Software', 'Red', 'Email', 
                                         'Acceso'], self.num_filas),
            'prioridad': np.random.choice(['Baja', 'Media', 'Alta', 'Crítica'], 
                                        self.num_filas, p=[0.4, 0.3, 0.2, 0.1]),
            'estado': np.random.choice(['Abierto', 'En Progreso', 'Resuelto', 'Cerrado'], 
                                     self.num_filas, p=[0.2, 0.3, 0.3, 0.2]),
            'asignado_a': [fake.name() for _ in range(self.num_filas)],
            'tiempo_resolucion_hrs': np.random.uniform(0.5, 72, self.num_filas).round(1)
        }
        
        df = pd.DataFrame(data)
        
        # Aplicar nulos si es necesario
        if self.porcentaje_nulos > 0:
            for col in ['asignado_a', 'tiempo_resolucion_hrs']:
                mask = np.random.random(self.num_filas) < (self.porcentaje_nulos / 100)
                df.loc[mask, col] = None
        
        return df
