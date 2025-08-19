"""Tests para plantillas específicas."""

import numpy as np
import pandas as pd
import pytest


class TestPlantillasEspecificas:
    """Tests para plantillas específicas del sistema."""

    def test_gastos_personales_estructura(self, plantilla_gastos):
        """Test estructura del DataFrame de gastos personales."""
        dataframe = plantilla_gastos.generar()

        # Verificar columnas esperadas
        columnas_esperadas = [
            'fecha', 'categoria', 'descripcion', 'monto',
            'metodo_pago', 'es_recurrente'
        ]
        for col in columnas_esperadas:
            assert col in dataframe.columns

        # Verificar tipos de datos
        fecha_valida = (pd.api.types.is_datetime64_any_dtype(dataframe['fecha']) or
                       dataframe['fecha'].dtype == 'object')
        assert fecha_valida

        monto_valido = (dataframe['monto'].dtype in ['float64', 'int64'] or
                       dataframe['monto'].dtype == 'object')
        assert monto_valido

        # Para columnas booleanas con nulos, el tipo cambia a object
        # Verificar que los valores no nulos son booleanos
        valores_no_nulos = dataframe['es_recurrente'].dropna()
        if len(valores_no_nulos) > 0:
            assert all(isinstance(val, (bool, np.bool_)) for val in valores_no_nulos)

    def test_ventas_supermercado_estructura(self, plantilla_ventas):
        """Test estructura del DataFrame de ventas supermercado."""
        dataframe = plantilla_ventas.generar()

        # Verificar columnas esperadas incluyendo calculadas
        columnas_esperadas = [
            'fecha_venta', 'ticket_id', 'producto', 'categoria',
            'cantidad', 'precio_unitario', 'descuento_pct',
            'vendedor_id', 'total'
        ]
        for col in columnas_esperadas:
            assert col in dataframe.columns

        # Verificar cálculo de total - solo para filas sin nulos en las columnas necesarias
        mask_completo = (dataframe['cantidad'].notna() &
                        dataframe['precio_unitario'].notna() &
                        dataframe['descuento_pct'].notna() &
                        dataframe['total'].notna())

        if mask_completo.any():
            dataframe_completo = dataframe[mask_completo].copy()
            total_calculado = (dataframe_completo['cantidad'] * dataframe_completo['precio_unitario'] *
                              (1 - dataframe_completo['descuento_pct'] / 100)).round(2)
            pd.testing.assert_series_equal(
                dataframe_completo['total'],
                total_calculado,
                check_names=False
            )

    @pytest.mark.parametrize("nombre_plantilla", [
        "Gastos Personales", "Ventas Supermercado", "Tickets de Servicio",
        "Ventas E-commerce", "Recursos Humanos", "Finanzas Personales",
        "Marketing Digital", "Educación - Estudiantes"
    ])
    def test_todas_plantillas_generan_datos(self, todas_las_plantillas,
                                           nombre_plantilla, parametros_sin_nulos):
        """Test que todas las plantillas generan datos correctamente."""
        if nombre_plantilla in todas_las_plantillas:
            plantilla_clase = todas_las_plantillas[nombre_plantilla]
            plantilla = plantilla_clase(**parametros_sin_nulos)
            dataframe = plantilla.generar()

            # Verificaciones básicas
            assert isinstance(dataframe, pd.DataFrame)
            assert len(dataframe) == parametros_sin_nulos['num_filas']
            assert len(dataframe.columns) > 0

            # Sin nulos cuando porcentaje es 0
            assert dataframe.isnull().sum().sum() == 0

    def test_reproducibilidad_con_semilla(self, todas_las_plantillas):
        """Test que la misma semilla produce los mismos datos."""
        parametros = {'num_filas': 10, 'semilla': 999, 'porcentaje_nulos': 0, 'idioma': 'es_ES'}

        for plantilla_clase in todas_las_plantillas.values():
            plantilla1 = plantilla_clase(**parametros)
            plantilla2 = plantilla_clase(**parametros)

            dataframe1 = plantilla1.generar()
            dataframe2 = plantilla2.generar()

            # Los DataFrames deben ser idénticos
            pd.testing.assert_frame_equal(dataframe1, dataframe2)

    def test_aplicacion_nulos_respeta_porcentaje(self, plantilla_gastos):
        """Test que el porcentaje de nulos se aplica aproximadamente."""
        plantilla_gastos.porcentaje_nulos = 25
        df = plantilla_gastos.generar()

        # Calcular porcentaje real de nulos (excluyendo columnas protegidas)
        columnas_con_nulos = [col for col in df.columns if col != 'fecha']
        if columnas_con_nulos:
            porcentaje_real = (df[columnas_con_nulos].isnull().sum().sum() /
                             (len(df) * len(columnas_con_nulos)) * 100)

            # Permitir un margen de error del 10%
            assert abs(porcentaje_real - 25) < 10
