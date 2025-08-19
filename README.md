# Generador de Datos Sintéticos

Una aplicación web desarrollada con Streamlit que permite generar datasets sintéticos para análisis de datos, machine learning y testing. Ofrece tanto generación personalizada como plantillas predefinidas para casos de uso específicos.

## 🚀 Características

- **Generación Personalizada**: Crea datasets con columnas numéricas, de texto, booleanas y de fechas
- **Plantillas Predefinidas**: 8 plantillas listas para usar en diferentes dominios
- **Múltiples Idiomas**: Soporte para diferentes locales (español, inglés, francés, etc.)
- **Exportación Múltiple**: CSV, Excel, JSON, Parquet y SQLite
- **Control de Calidad**: Configuración de porcentaje de valores nulos
- **Reproducibilidad**: Uso de semillas para resultados consistentes

## 📋 Plantillas Disponibles

1. **Educación - Estudiantes**: Datos académicos con calificaciones y métricas educativas
2. **Finanzas Personales**: Análisis financiero personal con ingresos, gastos e inversiones
3. **Gastos Personales**: Registro de gastos categorizados con métodos de pago
4. **Marketing Digital**: Métricas de campañas con CTR, conversiones y ROI
5. **Recursos Humanos**: Datos de empleados con salarios y evaluaciones
6. **Tickets de Servicio**: Sistema de soporte técnico con estados y prioridades
7. **Ventas E-commerce**: Métricas de ventas online con análisis de comportamiento
8. **Ventas Supermercado**: Registro de ventas retail con productos y categorías

## 🛠️ Instalación

### Requisitos Previos
- Python 3.11+
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone <repository-url>
cd DatosDinamicosSinteticos
```

2. **Crear entorno virtual (recomendado)**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Instalar dependencias de testing (opcional)**
```bash
pip install -r requirements-test.txt
```

## 🏃‍♂️ Uso

### Ejecutar la Aplicación

```bash
cd app
streamlit run main.py
```

La aplicación se abrirá en tu navegador en `http://localhost:8501`

### Modo Personalizado

1. Selecciona "Personalizado" en el menú lateral
2. Configura el número de registros y semilla
3. Ajusta las columnas deseadas usando los sliders
4. Selecciona el idioma para la generación de datos
5. Haz clic en "Generar"

### Modo Plantillas

1. Selecciona "Plantillas" en el menú lateral
2. Elige una plantilla del menú desplegable
3. Configura parámetros básicos (registros, semilla, % nulos, idioma)
4. Haz clic en "Generar"

### Exportación de Datos

Una vez generados los datos, puedes descargarlos en diferentes formatos:
- **📄 CSV**: Formato estándar para análisis
- **📊 Excel**: Para uso en hojas de cálculo
- **📋 JSON**: Para aplicaciones web y APIs
- **🗜️ Parquet**: Formato optimizado para big data
- **🗃️ SQLite**: Base de datos portátil

## 🧪 Testing

El proyecto incluye una suite completa de pruebas unitarias y de integración usando pytest.

### Ejecutar Todas las Pruebas

```bash
# Desde el directorio raíz del proyecto
pytest
```

### Ejecutar Pruebas con Cobertura

```bash
pytest --cov=app --cov-report=html
```

### Ejecutar Pruebas Específicas

```bash
# Pruebas de plantillas
pytest tests/test_plantillas_especificas.py

# Pruebas de integración
pytest tests/test_integracion.py

# Pruebas de rendimiento (pueden tardar más)
pytest tests/test_performance.py -m slow
```

### Estructura de Tests

```
tests/
├── __init__.py
├── conftest.py                 # Fixtures compartidas
├── test_plantillas_base.py     # Tests de funcionalidad base
├── test_plantillas_especificas.py  # Tests de plantillas individuales
├── test_integracion.py         # Tests de flujo completo
└── test_performance.py         # Tests de rendimiento
```

### Fixtures Disponibles

- `parametros_basicos`: Configuración estándar para tests
- `parametros_sin_nulos`: Configuración sin valores nulos
- `todas_las_plantillas`: Todas las clases de plantillas
- `plantilla_gastos`: Instancia de plantilla de gastos
- `plantilla_ventas`: Instancia de plantilla de ventas

### Markers de Pytest

- `@pytest.mark.slow`: Tests que pueden tardar más tiempo
- `@pytest.mark.integration`: Tests de integración

## 🏗️ Arquitectura del Proyecto

```
DatosDinamicosSinteticos/
├── app/
│   ├── main.py                 # Aplicación principal Streamlit
│   ├── config/
│   │   └── constantes.py       # Configuraciones globales
│   └── utils/
│       ├── generacion.py       # Generación personalizada
│       ├── descargas.py        # Funciones de exportación
│       └── plantillas/         # Sistema de plantillas
│           ├── __init__.py
│           ├── base.py         # Clase base abstracta
│           ├── gastos_personales.py
│           ├── ventas_supermercado.py
│           ├── tickets_servicio.py
│           ├── ventas_ecommerce.py
│           ├── recursos_humanos.py
│           ├── finanzas_personales.py
│           ├── marketing_digital.py
│           └── educacion_estudiantes.py
├── tests/                      # Suite de pruebas
├── requirements.txt            # Dependencias principales
├── requirements-test.txt       # Dependencias de testing
├── pytest.ini                 # Configuración de pytest
└── README.md                   # Documentación
```

## 🔧 Desarrollo

### Agregar Nueva Plantilla

1. Crear nueva clase que herede de `PlantillaBase`
2. Implementar métodos abstractos (`nombre`, `descripcion`, `generar`)
3. Registrar en `__init__.py` del módulo plantillas
4. Agregar tests correspondientes

Ejemplo:
```python
class MiNuevaPlantilla(PlantillaBase):
    @property
    def nombre(self) -> str:
        return "Mi Nueva Plantilla"
    
    @property
    def descripcion(self) -> str:
        return "Descripción de la plantilla"
    
    def generar(self) -> pd.DataFrame:
        # Implementación de generación
        pass
```

### Patrón Strategy

El proyecto utiliza el patrón Strategy para las plantillas, permitiendo:
- Fácil extensión con nuevas plantillas
- Interfaz consistente para todas las implementaciones
- Mantenimiento modular del código

## 📊 Ejemplos de Uso

### Análisis Financiero Personal
```python
from utils.plantillas import PLANTILLAS_DISPONIBLES

plantilla = PLANTILLAS_DISPONIBLES["Finanzas Personales"](
    num_filas=1000,
    semilla=42,
    porcentaje_nulos=5,
    idioma='es_ES'
)
df = plantilla.generar()
```

### Marketing Analytics
```python
plantilla_marketing = PLANTILLAS_DISPONIBLES["Marketing Digital"](
    num_filas=500,
    semilla=123,
    porcentaje_nulos=10,
    idioma='en_US'
)
df_marketing = plantilla_marketing.generar()
```

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la licencia MIT. Ver el archivo LICENSE para más detalles.

## 🐛 Reportar Problemas

Si encuentras algún bug o tienes sugerencias, por favor abre un issue en el repositorio.

## 📈 Roadmap

- [ ] Más plantillas de datos (IoT, Redes Sociales, etc.)
- [ ] Integración con bases de datos externas
- [ ] API REST para generación programática
- [ ] Validación avanzada de datos generados
- [ ] Métricas de calidad de datos sintéticos
