"""Tests para integración del sistema."""

import io
import os
import sys

import pandas as pd
import pytest

# Agregar el directorio de la app al path para imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from app.config.constantes import IDIOMAS_DISPONIBLES
from app.utils.descargas import (
    preparar_csv, preparar_excel, preparar_json,
    preparar_parquet, preparar_sqlite
)
from app.utils.generacion import generar_dataframe


class TestIntegracion:
    """Tests de integración del sistema."""

    def test_generacion_personalizada_completa(self):
        """Test generación de datos personalizados con todos los tipos."""
        dataframe = generar_dataframe(
            num_filas=25,
            semilla=42,
            num_numericas=2,
            num_strings=2,
            num_booleans=1,
            num_fechas=1,
            porcentaje_nulos=0,
            idioma='es_ES'
        )

        assert isinstance(dataframe, pd.DataFrame)
        assert len(dataframe) == 25
        assert len(dataframe.columns) == 6  # 2+2+1+1

    def test_todos_los_idiomas_disponibles(self):
        """Test que todos los idiomas configurados funcionan."""
        for idioma_codigo in IDIOMAS_DISPONIBLES.values():
            dataframe = generar_dataframe(
                num_filas=5,
                semilla=123,
                num_numericas=1,
                num_strings=1,
                num_booleans=0,
                num_fechas=0,
                porcentaje_nulos=0,
                idioma=idioma_codigo
            )

            assert isinstance(dataframe, pd.DataFrame)
            assert len(dataframe) == 5

    @pytest.mark.parametrize("formato,funcion", [
        ("csv", preparar_csv),
        ("excel", preparar_excel),
        ("json", preparar_json),
        ("parquet", preparar_parquet),
        ("sqlite", preparar_sqlite)
    ])
    def test_exportacion_formatos(self, funcion):
        """Test exportación a diferentes formatos."""
        dataframe = generar_dataframe(
            num_filas=10,
            semilla=42,
            num_numericas=1,
            num_strings=1,
            num_booleans=1,
            num_fechas=1,
            porcentaje_nulos=0,
            idioma='es_ES'
        )

        # La función debe ejecutarse sin errores
        resultado = funcion(dataframe)
        assert resultado is not None

        # Verificar según el tipo de resultado
        if isinstance(resultado, str):
            # Para CSV y JSON que retornan strings
            assert len(resultado) > 0
        elif isinstance(resultado, (bytes, io.BytesIO)):
            # Para Excel, Parquet y SQLite que retornan bytes o BytesIO
            if hasattr(resultado, 'getvalue'):
                # Es un BytesIO
                assert len(resultado.getvalue()) > 0
            else:
                # Es bytes directamente
                assert len(resultado) > 0
        else:
            # Fallback: verificar que no sea None
            assert resultado is not None

    def test_flujo_plantilla_completo(self, todas_las_plantillas):
        """Test flujo completo con plantillas y exportación."""
        plantilla_clase = todas_las_plantillas["Gastos Personales"]
        plantilla = plantilla_clase(
            num_filas=15,
            semilla=42,
            porcentaje_nulos=5,
            idioma='es_ES'
        )

        dataframe = plantilla.generar()
        assert isinstance(dataframe, pd.DataFrame)
        assert len(dataframe) == 15

        # Test exportación
        csv_data = preparar_csv(dataframe)
        assert isinstance(csv_data, str)
        assert len(csv_data) > 0

        json_data = preparar_json(dataframe)
        assert len(json_data) > 0
