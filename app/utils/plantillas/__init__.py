"""Módulo de plantillas para generación de datos sintéticos."""

from .base import PlantillaBase
from .educacion_estudiantes import PlantillaEducacionEstudiantes
from .finanzas_personales import PlantillaFinanzasPersonales
from .gastos_personales import PlantillaGastosPersonales
from .historial_clinico import PlantillaHistorialClinico
from .logistica_entregas import PlantillaLogisticaEntregas
from .marketing_digital import PlantillaMarketingDigital
from .recursos_humanos import PlantillaRecursosHumanos
from .sensores_iot import PlantillaSensoresIoT
from .tickets_servicio import PlantillaTicketsServicio
from .ventas_ecommerce import PlantillaVentasEcommerce
from .ventas_supermercado import PlantillaVentasSupermercado

# Registro de plantillas disponibles
PLANTILLAS_DISPONIBLES = {
    "Educación - Estudiantes": PlantillaEducacionEstudiantes,
    "Finanzas Personales":     PlantillaFinanzasPersonales,
    "Gastos Personales":       PlantillaGastosPersonales,
    "Historial Clínico":       PlantillaHistorialClinico,
    "Logística y Entregas":    PlantillaLogisticaEntregas,
    "Marketing Digital":       PlantillaMarketingDigital,
    "Recursos Humanos":        PlantillaRecursosHumanos,
    "Sensores IoT":            PlantillaSensoresIoT,
    "Tickets de Servicio":     PlantillaTicketsServicio,
    "Ventas E-commerce":       PlantillaVentasEcommerce,
    "Ventas Supermercado":     PlantillaVentasSupermercado,
}

__all__ = ['PlantillaBase', 'PLANTILLAS_DISPONIBLES']
