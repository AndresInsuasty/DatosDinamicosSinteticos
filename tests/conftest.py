import pytest
import pandas as pd
import numpy as np
from app.utils.plantillas import PLANTILLAS_DISPONIBLES

@pytest.fixture
def parametros_basicos():
    """Parámetros básicos para las plantillas."""
    return {
        'num_filas': 50,
        'semilla': 42,
        'porcentaje_nulos': 10,
        'idioma': 'es_ES'
    }

@pytest.fixture
def parametros_sin_nulos():
    """Parámetros sin nulos para tests específicos."""
    return {
        'num_filas': 20,
        'semilla': 123,
        'porcentaje_nulos': 0,
        'idioma': 'en_US'
    }

@pytest.fixture
def todas_las_plantillas():
    """Todas las clases de plantillas disponibles."""
    return PLANTILLAS_DISPONIBLES

@pytest.fixture
def plantilla_gastos(parametros_basicos):
    """Instancia de plantilla de gastos personales."""
    return PLANTILLAS_DISPONIBLES["Gastos Personales"](**parametros_basicos)

@pytest.fixture
def plantilla_ventas(parametros_basicos):
    """Instancia de plantilla de ventas supermercado."""
    return PLANTILLAS_DISPONIBLES["Ventas Supermercado"](**parametros_basicos)
