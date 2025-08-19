"""Módulo base."""

from abc import ABC, abstractmethod
import pandas as pd
import numpy as np

class PlantillaBase(ABC):
    """Clase base abstracta para todas las plantillas de datos sintéticos."""

    def __init__(self, num_filas: int, semilla: int, porcentaje_nulos: int = 0, idioma: str = 'es_ES'):
        self.num_filas = num_filas
        self.semilla = semilla
        self.porcentaje_nulos = porcentaje_nulos
        self.idioma = idioma

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

    def _aplicar_nulos(self, df: pd.DataFrame, columnas_excluir: list = None) -> pd.DataFrame:
        """Aplica nulos aleatoriamente a todas las columnas excepto las excluidas."""
        if self.porcentaje_nulos <= 0:
            return df

        if columnas_excluir is None:
            columnas_excluir = []

        # Aplicar nulos a todas las columnas excepto las excluidas
        for col in df.columns:
            if col not in columnas_excluir:
                mask = np.random.random(self.num_filas) < (self.porcentaje_nulos / 100)
                df.loc[mask, col] = None

        return df
