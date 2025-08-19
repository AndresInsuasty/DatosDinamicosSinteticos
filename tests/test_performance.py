import pytest
import time
import pandas as pd

class TestPerformance:
    
    @pytest.mark.slow
    def test_generacion_grandes_volumenes(self, todas_las_plantillas):
        """Test rendimiento con volúmenes grandes de datos."""
        parametros = {
            'num_filas': 10000,
            'semilla': 42,
            'porcentaje_nulos': 5,
            'idioma': 'es_ES'
        }
        
        for nombre_plantilla, plantilla_clase in todas_las_plantillas.items():
            start_time = time.time()
            
            plantilla = plantilla_clase(**parametros)
            df = plantilla.generar()
            
            end_time = time.time()
            tiempo_ejecucion = end_time - start_time
            
            # Verificaciones
            assert isinstance(df, pd.DataFrame)
            assert len(df) == 10000
            
            # El tiempo no debe exceder 10 segundos para 10k registros
            assert tiempo_ejecucion < 10, f"Plantilla {nombre_plantilla} tardó {tiempo_ejecucion:.2f}s"
    
    def test_memoria_eficiente(self, plantilla_gastos):
        """Test que la generación no consume memoria excesiva."""
        import psutil
        import os
        
        proceso = psutil.Process(os.getpid())
        memoria_inicial = proceso.memory_info().rss / 1024 / 1024  # MB
        
        # Generar múltiples DataFrames
        for _ in range(10):
            df = plantilla_gastos.generar()
            del df
        
        memoria_final = proceso.memory_info().rss / 1024 / 1024  # MB
        incremento_memoria = memoria_final - memoria_inicial
        
        # El incremento no debe ser excesivo (menos de 100MB)
        assert incremento_memoria < 100, f"Incremento de memoria: {incremento_memoria:.2f}MB"
