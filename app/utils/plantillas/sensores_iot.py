"""Plantilla para generar datos sintéticos de sensores IoT."""

import pandas as pd
import numpy as np
from faker import Faker

from .base import PlantillaBase


class PlantillaSensoresIoT(PlantillaBase):
    """Plantilla para generar datos de sensores IoT industriales/ambientales."""

    @property
    def nombre(self) -> str:
        return "Sensores IoT"

    @property
    def descripcion(self) -> str:
        return ("Lecturas de sensores IoT industriales y ambientales. "
                "Temperatura, humedad, presión y batería correlacionados entre sí y "
                "con alertas realistas generadas cuando los valores superan umbrales.")

    def generar(self) -> pd.DataFrame:
        fake = Faker(self.idioma)
        fake.seed_instance(self.semilla)
        np.random.seed(self.semilla)

        # Tipo de sensor → parámetros ambientales base
        config_sensor = {
            'Temperatura_Ambiente': {
                'temp_mu': 22, 'temp_sd': 4,
                'hum_mu':  55, 'hum_sd': 10,
                'pres_mu': 1013, 'pres_sd': 8,
            },
            'Temperatura_Industrial': {
                'temp_mu': 65, 'temp_sd': 15,
                'hum_mu':  30, 'hum_sd': 8,
                'pres_mu': 1013, 'pres_sd': 15,
            },
            'Cámara_Fría': {
                'temp_mu': -5, 'temp_sd': 3,
                'hum_mu':  85, 'hum_sd': 5,
                'pres_mu': 1015, 'pres_sd': 5,
            },
            'Exterior_Urbano': {
                'temp_mu': 18, 'temp_sd': 8,
                'hum_mu':  65, 'hum_sd': 15,
                'pres_mu': 1008, 'pres_sd': 12,
            },
            'Sala_Servidores': {
                'temp_mu': 19, 'temp_sd': 2,
                'hum_mu':  45, 'hum_sd': 5,
                'pres_mu': 1013, 'pres_sd': 3,
            },
        }
        umbrales_temp = {
            'Temperatura_Ambiente':   (10, 35),
            'Temperatura_Industrial': (20, 100),
            'Cámara_Fría':            (-15, 5),
            'Exterior_Urbano':        (-5, 45),
            'Sala_Servidores':        (15, 27),
        }
        estados_bateria = ['Crítica', 'Baja', 'Media', 'Alta', 'Cargando']
        ubicaciones = ['Planta-A', 'Planta-B', 'Almacén-1', 'Almacén-2',
                       'Oficina-Principal', 'Exterior-Norte', 'Exterior-Sur', 'CPD']

        tipos = list(config_sensor.keys())
        tipo_arr = np.random.choice(tipos, self.num_filas)

        temperatura = np.array([
            np.random.normal(config_sensor[t]['temp_mu'], config_sensor[t]['temp_sd'])
            for t in tipo_arr
        ]).round(2)
        humedad = np.clip(
            np.array([
                np.random.normal(config_sensor[t]['hum_mu'], config_sensor[t]['hum_sd'])
                for t in tipo_arr
            ]), 0, 100
        ).round(2)
        # Temperatura y humedad tienen correlación inversa leve
        humedad = np.clip(
            humedad - (temperatura - np.array([config_sensor[t]['temp_mu'] for t in tipo_arr])) * 0.3,
            0, 100
        ).round(2)

        presion = np.array([
            np.random.normal(config_sensor[t]['pres_mu'], config_sensor[t]['pres_sd'])
            for t in tipo_arr
        ]).round(1)

        # Nivel de CO2 correlaciona con temperatura en entornos industriales
        co2_ppm = np.clip(
            400 + (temperatura - 15) * 5 + np.random.normal(0, 30, self.num_filas),
            350, 5000
        ).round(0).astype(int)

        # Batería degrada con el tiempo (sensores más viejos tienen menos batería)
        bateria_pct = np.clip(
            np.random.beta(4, 2, self.num_filas) * 100 +
            np.random.normal(0, 5, self.num_filas),
            0, 100
        ).round(1)
        estado_bateria_arr = np.select(
            [bateria_pct < 10, bateria_pct < 25, bateria_pct < 60, bateria_pct < 90],
            ['Crítica', 'Baja', 'Media', 'Alta'],
            default='Cargando'
        )

        # Señal WiFi correlaciona negativamente con distancia (simulada con ruido)
        senal_db = np.clip(
            np.random.normal(-65, 15, self.num_filas), -100, -30
        ).round(0).astype(int)

        # Alertas: generadas cuando temperatura fuera de rango o batería crítica
        temp_min = np.array([umbrales_temp[t][0] for t in tipo_arr])
        temp_max = np.array([umbrales_temp[t][1] for t in tipo_arr])
        alerta_temp = (temperatura < temp_min) | (temperatura > temp_max)
        alerta_bateria = bateria_pct < 15
        alerta_co2 = co2_ppm > 1000
        tiene_alerta = alerta_temp | alerta_bateria | alerta_co2

        tipo_alerta = np.where(
            alerta_temp & alerta_bateria, 'Temperatura+Batería',
            np.where(alerta_temp & alerta_co2, 'Temperatura+CO2',
            np.where(alerta_temp, 'Temperatura',
            np.where(alerta_bateria, 'Batería Crítica',
            np.where(alerta_co2, 'CO2 Elevado', 'Sin Alerta'))))
        )

        data = {
            'timestamp': [
                fake.date_time_between(start_date='-30d', end_date='now')
                for _ in range(self.num_filas)
            ],
            'sensor_id': [f"SNS-{fake.random_number(digits=5):05d}" for _ in range(self.num_filas)],
            'tipo_sensor': tipo_arr,
            'ubicacion': np.random.choice(ubicaciones, self.num_filas),
            'temperatura_c': temperatura,
            'humedad_pct': humedad,
            'presion_hpa': presion,
            'co2_ppm': co2_ppm,
            'bateria_pct': bateria_pct,
            'estado_bateria': estado_bateria_arr,
            'senal_wifi_dbm': senal_db,
            'tiene_alerta': tiene_alerta,
            'tipo_alerta': tipo_alerta,
        }

        dataframe = pd.DataFrame(data)
        dataframe = dataframe.sort_values('timestamp').reset_index(drop=True)
        dataframe = self._aplicar_nulos(
            dataframe, columnas_excluir=['timestamp', 'sensor_id']
        )
        return dataframe
