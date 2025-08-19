from .base import PlantillaBase
from .gastos_personales import PlantillaGastosPersonales
from .ventas_supermercado import PlantillaVentasSupermercado
from .tickets_servicio import PlantillaTicketsServicio
from .ventas_ecommerce import PlantillaVentasEcommerce
from .recursos_humanos import PlantillaRecursosHumanos
from .finanzas_personales import PlantillaFinanzasPersonales
from .marketing_digital import PlantillaMarketingDigital
from .educacion_estudiantes import PlantillaEducacionEstudiantes

# Registro de plantillas disponibles
PLANTILLAS_DISPONIBLES = {
    "Gastos Personales": PlantillaGastosPersonales,
    "Ventas Supermercado": PlantillaVentasSupermercado,
    "Tickets de Servicio": PlantillaTicketsServicio,
    "Ventas E-commerce": PlantillaVentasEcommerce,
    "Recursos Humanos": PlantillaRecursosHumanos,
    "Finanzas Personales": PlantillaFinanzasPersonales,
    "Marketing Digital": PlantillaMarketingDigital,
    "Educación - Estudiantes": PlantillaEducacionEstudiantes
}

__all__ = ['PlantillaBase', 'PLANTILLAS_DISPONIBLES']
