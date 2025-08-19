"""Tests para rendimiento del sistema."""

import os
import time

import pandas as pd
import pytest


class TestPerformance:
    """Tests de rendimiento del sistema."""

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
            dataframe = plantilla.generar()

            end_time = time.time()
            tiempo_ejecucion = end_time - start_time

            # Verificaciones
            assert isinstance(dataframe, pd.DataFrame)
            assert len(dataframe) == 10000

            # El tiempo no debe exceder 10 segundos para 10k registros
            max_tiempo = 10
            assert tiempo_ejecucion < max_tiempo, (
                f"Plantilla {nombre_plantilla} tardó {tiempo_ejecucion:.2f}s"
            )

    def test_memoria_eficiente(self, plantilla_gastos):
        """Test que la generación no consume memoria excesiva."""
        import psutil

        proceso = psutil.Process(os.getpid())
        memoria_inicial = proceso.memory_info().rss / 1024 / 1024  # MB

        # Generar múltiples DataFrames
        for _ in range(10):
            dataframe = plantilla_gastos.generar()
            del dataframe

        memoria_final = proceso.memory_info().rss / 1024 / 1024  # MB
        incremento_memoria = memoria_final - memoria_inicial

        # El incremento no debe ser excesivo (menos de 100MB)
        max_incremento = 100
        assert incremento_memoria < max_incremento, (
            f"Incremento de memoria: {incremento_memoria:.2f}MB"
        )
