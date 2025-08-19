from abc import ABC, abstractmethod
import pandas as pd

class PlantillaBase(ABC):
    """Clase base abstracta para todas las plantillas de datos sintéticos."""
    
    def __init__(self, num_filas: int, semilla: int, porcentaje_nulos: int = 0):
        self.num_filas = num_filas
        self.semilla = semilla
        self.porcentaje_nulos = porcentaje_nulos
    
    @abstractmethod
    def generar(self) -> pd.DataFrame:
        """Genera el DataFrame con los datos sintéticos de la plantilla."""
        pass
    
    @property
    @abstractmethod
    def nombre(self) -> str:
        """Nombre descriptivo de la plantilla."""
        pass
    
    @property
    @abstractmethod
    def descripcion(self) -> str:
        """Descripción de la plantilla."""
        pass
