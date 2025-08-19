import pytest
import pandas as pd
import numpy as np

class TestPlantillasEspecificas:
    
    def test_gastos_personales_estructura(self, plantilla_gastos):
        """Test estructura del DataFrame de gastos personales."""
        df = plantilla_gastos.generar()
        
        # Verificar columnas esperadas
        columnas_esperadas = [
            'fecha', 'categoria', 'descripcion', 'monto', 
            'metodo_pago', 'es_recurrente'
        ]
        for col in columnas_esperadas:
            assert col in df.columns
        
        # Verificar tipos de datos
        assert pd.api.types.is_datetime64_any_dtype(df['fecha']) or df['fecha'].dtype == 'object'
        assert df['monto'].dtype in ['float64', 'int64'] or df['monto'].dtype == 'object'
        
        # Para columnas booleanas con nulos, el tipo cambia a object
        # Verificar que los valores no nulos son booleanos
        valores_no_nulos = df['es_recurrente'].dropna()
        if len(valores_no_nulos) > 0:
            assert all(isinstance(val, (bool, np.bool_)) for val in valores_no_nulos)

    def test_ventas_supermercado_estructura(self, plantilla_ventas):
        """Test estructura del DataFrame de ventas supermercado."""
        df = plantilla_ventas.generar()
        
        # Verificar columnas esperadas incluyendo calculadas
        columnas_esperadas = [
            'fecha_venta', 'ticket_id', 'producto', 'categoria',
            'cantidad', 'precio_unitario', 'descuento_pct', 
            'vendedor_id', 'total'
        ]
        for col in columnas_esperadas:
            assert col in df.columns
        
        # Verificar cálculo de total - solo para filas sin nulos en las columnas necesarias
        mask_completo = (df['cantidad'].notna() & 
                        df['precio_unitario'].notna() & 
                        df['descuento_pct'].notna() & 
                        df['total'].notna())
        
        if mask_completo.any():
            df_completo = df[mask_completo].copy()
            total_calculado = (df_completo['cantidad'] * df_completo['precio_unitario'] * 
                              (1 - df_completo['descuento_pct'] / 100)).round(2)
            pd.testing.assert_series_equal(
                df_completo['total'], 
                total_calculado, 
                check_names=False
            )
    
    @pytest.mark.parametrize("nombre_plantilla", [
        "Gastos Personales", "Ventas Supermercado", "Tickets de Servicio",
        "Ventas E-commerce", "Recursos Humanos", "Finanzas Personales",
        "Marketing Digital", "Educación - Estudiantes"
    ])
    def test_todas_plantillas_generan_datos(self, todas_las_plantillas, nombre_plantilla, parametros_sin_nulos):
        """Test que todas las plantillas generan datos correctamente."""
        if nombre_plantilla in todas_las_plantillas:
            plantilla_clase = todas_las_plantillas[nombre_plantilla]
            plantilla = plantilla_clase(**parametros_sin_nulos)
            df = plantilla.generar()
            
            # Verificaciones básicas
            assert isinstance(df, pd.DataFrame)
            assert len(df) == parametros_sin_nulos['num_filas']
            assert len(df.columns) > 0
            
            # Sin nulos cuando porcentaje es 0
            assert df.isnull().sum().sum() == 0
    
    def test_reproducibilidad_con_semilla(self, todas_las_plantillas):
        """Test que la misma semilla produce los mismos datos."""
        parametros = {'num_filas': 10, 'semilla': 999, 'porcentaje_nulos': 0, 'idioma': 'es_ES'}
        
        for nombre_plantilla, plantilla_clase in todas_las_plantillas.items():
            plantilla1 = plantilla_clase(**parametros)
            plantilla2 = plantilla_clase(**parametros)
            
            df1 = plantilla1.generar()
            df2 = plantilla2.generar()
            
            # Los DataFrames deben ser idénticos
            pd.testing.assert_frame_equal(df1, df2)
    
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
