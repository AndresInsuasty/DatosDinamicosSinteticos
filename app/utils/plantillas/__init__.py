from .base import PlantillaBase
from .gastos_personales import PlantillaGastosPersonales
from .ventas_supermercado import PlantillaVentasSupermercado
from .tickets_servicio import PlantillaTicketsServicio

# Registro de plantillas disponibles
PLANTILLAS_DISPONIBLES = {
    "Gastos Personales": PlantillaGastosPersonales,
    "Ventas Supermercado": PlantillaVentasSupermercado,
    "Tickets de Servicio": PlantillaTicketsServicio
}

__all__ = ['PlantillaBase', 'PLANTILLAS_DISPONIBLES']
