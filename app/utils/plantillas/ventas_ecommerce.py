import pandas as pd
import numpy as np
from faker import Faker
from .base import PlantillaBase

class PlantillaVentasEcommerce(PlantillaBase):
    
    @property
    def nombre(self) -> str:
        return "Ventas E-commerce"
    
    @property
    def descripcion(self) -> str:
        return "Datos de ventas online con métricas de conversión, tráfico y análisis de comportamiento"
    
    def generar(self) -> pd.DataFrame:
        fake = Faker(self.idioma)
        fake.seed_instance(self.semilla)
        np.random.seed(self.semilla)
        
        canales = ['Google Ads', 'Facebook', 'Email', 'Orgánico', 'Directo', 'Referidos']
        dispositivos = ['Desktop', 'Mobile', 'Tablet']
        categorias = ['Electrónicos', 'Ropa', 'Hogar', 'Deportes', 'Libros', 'Belleza']
        
        data = {
            'fecha_pedido': [fake.date_between(start_date='-6m', end_date='today') 
                            for _ in range(self.num_filas)],
            'pedido_id': [f"ORD-{fake.random_number(digits=8)}" for _ in range(self.num_filas)],
            'cliente_id': [f"CLI-{fake.random_number(digits=6)}" for _ in range(self.num_filas)],
            'canal_marketing': np.random.choice(canales, self.num_filas),
            'dispositivo': np.random.choice(dispositivos, self.num_filas, p=[0.4, 0.5, 0.1]),
            'categoria_producto': np.random.choice(categorias, self.num_filas),
            'valor_pedido': np.random.uniform(15, 800, self.num_filas).round(2),
            'costo_adquisicion': np.random.uniform(2, 50, self.num_filas).round(2),
            'tiempo_en_sitio_min': np.random.uniform(1, 45, self.num_filas).round(1),
            'paginas_vistas': np.random.randint(1, 15, self.num_filas),
            'es_cliente_nuevo': np.random.choice([True, False], self.num_filas, p=[0.3, 0.7]),
            'pais': [fake.country() for _ in range(self.num_filas)],
            'descuento_aplicado': np.random.uniform(0, 30, self.num_filas).round(2)
        }
        
        df = pd.DataFrame(data)
        df['roi'] = ((df['valor_pedido'] - df['costo_adquisicion']) / df['costo_adquisicion'] * 100).round(2)
        
        if self.porcentaje_nulos > 0:
            for col in ['descuento_aplicado', 'tiempo_en_sitio_min']:
                mask = np.random.random(self.num_filas) < (self.porcentaje_nulos / 100)
                df.loc[mask, col] = None
        
        return df
