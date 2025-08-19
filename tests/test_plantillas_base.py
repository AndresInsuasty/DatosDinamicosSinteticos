import pytest
import pandas as pd
import numpy as np
from app.utils.plantillas.base import PlantillaBase

class PlantillaMock(PlantillaBase):
    """Plantilla mock para testing."""
    
    @property
    def nombre(self) -> str:
        return "Test Mock"
    
    @property
    def descripcion(self) -> str:
        return "Plantilla de prueba"
    
    def generar(self) -> pd.DataFrame:
        return pd.DataFrame({
            'id': range(self.num_filas),
            'valor': np.random.uniform(0, 100, self.num_filas),
            'texto': [f"item_{i}" for i in range(self.num_filas)]
        })

class TestPlantillaBase:
    
    def test_inicializacion_basica(self):
        """Test inicialización con parámetros básicos."""
        plantilla = PlantillaMock(10, 42, 5, 'es_ES')
        assert plantilla.num_filas == 10
        assert plantilla.semilla == 42
        assert plantilla.porcentaje_nulos == 5
        assert plantilla.idioma == 'es_ES'
    
    def test_inicializacion_por_defecto(self):
        """Test inicialización con valores por defecto."""
        plantilla = PlantillaMock(5, 123)
        assert plantilla.num_filas == 5
        assert plantilla.semilla == 123
        assert plantilla.porcentaje_nulos == 0
        assert plantilla.idioma == 'es_ES'
    
    def test_aplicar_nulos_sin_exclusiones(self):
        """Test aplicación de nulos sin columnas excluidas."""
        plantilla = PlantillaMock(100, 42, 20, 'es_ES')
        df = plantilla.generar()
        df_con_nulos = plantilla._aplicar_nulos(df)
        
        # Verificar que hay nulos en todas las columnas
        for col in df_con_nulos.columns:
            assert df_con_nulos[col].isnull().sum() > 0
    
    def test_aplicar_nulos_con_exclusiones(self):
        """Test aplicación de nulos con columnas excluidas."""
        plantilla = PlantillaMock(100, 42, 30, 'es_ES')
        df = plantilla.generar()
        df_con_nulos = plantilla._aplicar_nulos(df, columnas_excluir=['id'])
        
        # Verificar que la columna excluida no tiene nulos
        assert df_con_nulos['id'].isnull().sum() == 0
        # Verificar que las otras columnas sí tienen nulos
        assert df_con_nulos['valor'].isnull().sum() > 0
        assert df_con_nulos['texto'].isnull().sum() > 0
    
    def test_sin_nulos_cuando_porcentaje_cero(self):
        """Test que no se aplican nulos cuando porcentaje es 0."""
        plantilla = PlantillaMock(50, 42, 0, 'es_ES')
        df = plantilla.generar()
        df_resultado = plantilla._aplicar_nulos(df)
        
        # No debe haber nulos en ninguna columna
        assert df_resultado.isnull().sum().sum() == 0
