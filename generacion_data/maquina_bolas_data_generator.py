"""
Generador Completo de Datos Sintéticos para Molinos de Bolas - MineraPeru
=========================================================================

Este módulo genera datos sintéticos realistas para 6 molinos de bolas basado en:
- Literatura técnica especializada (Emerson, SPM, etc.)
- Correlaciones físicas fundamentales (Ley de Bond, etc.)
- Patrones de degradación y falla reales de la industria minera
- Variabilidad operacional típica de operaciones mineras

Autor: GRUPO 1 - BREIT
Fecha: 2025
"""

import numpy as np
import pandas as pd
import datetime as dt
from scipy import stats
from scipy.interpolate import interp1d
import warnings
warnings.filterwarnings('ignore')

class MillPhysicsEngine:
    """
    Motor de física que implementa correlaciones fundamentales de molienda
    basadas en literatura técnica y ecuaciones establecidas.
    """
    
    def __init__(self):
        # Constantes físicas fundamentales
        self.BOND_CONSTANT = 10.0  # Constante de Bond
        self.CRITICAL_SPEED_CONSTANT = 42.3  # Para velocidad crítica
        self.MILL_DIAMETER = 5.5  # metros
        self.MILL_LENGTH = 7.0  # metros
        
    def calculate_critical_speed(self, diameter_m=5.5):
        """Calcula velocidad crítica según fórmula estándar"""
        return self.CRITICAL_SPEED_CONSTANT / np.sqrt(diameter_m)
    
    def calculate_bond_energy(self, work_index, f80, p80):
        """
        Calcula energía específica según Ley de Bond
        Args:
            work_index: Índice de trabajo (kWh/t)
            f80: 80% pasante alimentación (μm)  
            p80: 80% pasante producto (μm)
        """
        return self.BOND_CONSTANT * work_index * (1/np.sqrt(p80) - 1/np.sqrt(f80))
    
    def calculate_mill_efficiency(self, liner_wear, ball_charge, speed_pct_critical):
        """
        Calcula eficiencia real del molino basada en condiciones operativas
        """
        # Eficiencia base óptima
        base_efficiency = 0.82
        
        # Factor de desgaste de liners (0-80% desgaste)
        liner_factor = 1.0 - (liner_wear / 100) * 0.18  # Hasta 18% pérdida
        
        # Factor de carga de bolas (óptimo en 32%)
        optimal_ball_charge = 32.0
        ball_factor = 1.0 - 0.5 * ((ball_charge - optimal_ball_charge) / optimal_ball_charge)**2
        
        # Factor de velocidad (óptimo en 76% velocidad crítica)
        optimal_speed_pct = 76.0
        speed_factor = 1.0 - 0.3 * ((speed_pct_critical - optimal_speed_pct) / optimal_speed_pct)**2
        
        return base_efficiency * liner_factor * ball_factor * speed_factor
    
    def calculate_bearing_load_factor(self, power_draw, mill_speed, misalignment=0.0):
        """
        Calcula factor de carga en rodamientos basado en potencia y velocidad
        """
        # Carga base proporcional a potencia
        base_load = power_draw / 2000.0  # Normalizado a factor ~1.0
        
        # Factor de velocidad (cargas dinámicas)
        speed_factor = 1.0 + 0.3 * (mill_speed / 15.0 - 1.0)**2
        
        # Factor de desalineación (incrementa cargas)
        misalignment_factor = 1.0 + misalignment * 2.0
        
        return base_load * speed_factor * misalignment_factor


class DegradationModels:
    """
    Modelos de degradación realistas para diferentes componentes del molino
    basados en patrones observados en la industria minera.
    """
    
    def __init__(self):
        self.degradation_patterns = {
            'bearing_outer_race': {
                'typical_life_hours': 15000,  # ~18 meses operación continua
                'precursor_days': [15, 45],   # Rango de días con señales
                'growth_pattern': 'exponential'
            },
            'bearing_inner_race': {
                'typical_life_hours': 12000,
                'precursor_days': [10, 30],
                'growth_pattern': 'exponential'
            },
            'bearing_feed': {
                'typical_life_hours': 15000,
                'precursor_days': [15, 45],
                'growth_pattern': 'exponential'
            },
            'bearing_discharge': {
                'typical_life_hours': 12000,
                'precursor_days': [12, 35],
                'growth_pattern': 'exponential'
            },
            'liner_wear': {
                'typical_life_hours': 6000,   # ~8 meses
                'precursor_days': [60, 180],  # Degradación muy gradual
                'growth_pattern': 'linear'
            },
            'motor_electrical': {
                'typical_life_hours': 25000,  # ~3 años
                'precursor_days': [7, 21],
                'growth_pattern': 'sudden'
            },
            'lubrication': {
                'typical_life_hours': 8760,   # ~1 año
                'precursor_days': [30, 90],
                'growth_pattern': 'linear'
            }
        }
    
    def generate_bearing_degradation(self, base_vibration, hours_to_failure, failure_type='bearing_outer_race'):
        """
        Genera patrón de degradación realista para rodamientos
        """
        pattern = self.degradation_patterns[failure_type]
        precursor_hours = np.random.uniform(*pattern['precursor_days']) * 24
        
        if hours_to_failure > precursor_hours:
            # Operación normal
            return base_vibration * np.random.normal(1.0, 0.05)
        else:
            # Fase de degradación
            progress = (precursor_hours - hours_to_failure) / precursor_hours
            
            if pattern['growth_pattern'] == 'exponential':
                # Crecimiento exponencial típico de fallas de rodamientos
                multiplier = 1.0 + 4.0 * (np.exp(3 * progress) - 1) / (np.exp(3) - 1)
            else:
                # Crecimiento lineal
                multiplier = 1.0 + 2.0 * progress
                
            return base_vibration * multiplier * np.random.normal(1.0, 0.1)
    
    def generate_liner_wear_effect(self, base_power, wear_percentage):
        """
        Genera efecto del desgaste de liners en consumo energético
        """
        # Los liners desgastados reducen eficiencia de molienda
        wear_factor = 1.0 + (wear_percentage / 100) * 0.15  # Hasta 15% incremento
        return base_power * wear_factor
    
    def generate_lubrication_degradation(self, base_temp, oil_quality, hours_since_change):
        """
        Genera degradación de lubricación que afecta temperatura
        """
        # Degradación gradual del aceite
        oil_degradation = min(hours_since_change / 8760, 1.0)  # Normalizado a 1 año
        quality_factor = (1.0 - oil_quality / 100) * 2.0  # Calidad 0-100%
        
        temp_increase = 5.0 * oil_degradation + 10.0 * quality_factor
        return base_temp + temp_increase


class IndustrialNoiseModels:
    """
    Modelos de ruido realistas para sensores industriales en ambiente minero
    """
    
    def __init__(self):
        # Parámetros de ruido por tipo de sensor (basado en especificaciones técnicas)
        self.noise_params = {
            'vibration': {'base_noise': 0.05, 'seasonal': 0.02, 'random': 0.03},
            'temperature': {'base_noise': 0.02, 'seasonal': 0.01, 'random': 0.015},
            'electrical': {'base_noise': 0.01, 'seasonal': 0.005, 'random': 0.02},
            'process': {'base_noise': 0.03, 'seasonal': 0.01, 'random': 0.025}
        }
    
    def add_sensor_noise(self, signal, sensor_type, timestamp):
        """
        Agrega ruido realista específico del tipo de sensor
        """
        params = self.noise_params.get(sensor_type, self.noise_params['process'])
        
        # Ruido base del sensor
        base_noise = np.random.normal(0, params['base_noise'], len(signal))
        
        # Ruido estacional (variaciones ambientales)
        day_of_year = timestamp.dt.dayofyear
        seasonal_noise = params['seasonal'] * np.sin(2 * np.pi * day_of_year / 365)
        
        # Ruido aleatorio de alta frecuencia
        random_noise = np.random.normal(0, params['random'], len(signal))
        
        # Outliers ocasionales (1% de probabilidad)
        outlier_mask = np.random.random(len(signal)) < 0.01
        outlier_noise = np.where(outlier_mask, 
                                np.random.normal(0, params['base_noise'] * 5), 0)
        
        return signal * (1 + base_noise + seasonal_noise + random_noise + outlier_noise)


class RealisticMillDataGenerator:
    """
    Generador principal que combina física, degradación y ruido para crear
    datos sintéticos realistas de molinos de bolas.
    """
    
    def __init__(self, start_date='2023-01-01', duration_years=2.5):
        self.start_date = pd.to_datetime(start_date)
        self.duration_years = duration_years
        # Convertir años decimales a días para evitar error de pd.DateOffset
        duration_days = int(duration_years * 365.25)
        self.end_date = self.start_date + pd.Timedelta(days=duration_days)
        
        # Inicializar motores de física y degradación
        self.physics = MillPhysicsEngine()
        self.degradation = DegradationModels()
        self.noise = IndustrialNoiseModels()
        
        # Configuración única por molino (heterogeneidad realista)
        self.mill_configs = self._initialize_mill_configs()
        
        # Lista para almacenar eventos de falla programados
        self.scheduled_failures = []
        
    def _initialize_mill_configs(self):
        """
        Inicializa configuraciones únicas para cada molino
        Simula heterogeneidad real de equipos en operación
        """
        configs = {}
        base_config = {
            'motor_power_rating': 2000,  # kW
            'mill_diameter': 5.5,        # m
            'mill_length': 7.0,          # m
            'critical_speed': self.physics.calculate_critical_speed()
        }
        
        # Configuraciones específicas por molino
        mill_variations = {
            'M1': {'age_years': 8, 'condition': 0.85, 'efficiency_factor': 0.98, 
                   'failure_tendency': 'bearings', 'liner_condition': 0.6},
            'M2': {'age_years': 6, 'condition': 0.92, 'efficiency_factor': 1.02, 
                   'failure_tendency': 'normal', 'liner_condition': 0.8},
            'M3': {'age_years': 10, 'condition': 0.78, 'efficiency_factor': 0.94, 
                   'failure_tendency': 'liners', 'liner_condition': 0.4},
            'M4': {'age_years': 5, 'condition': 0.94, 'efficiency_factor': 1.01, 
                   'failure_tendency': 'normal', 'liner_condition': 0.9},
            'M5': {'age_years': 9, 'condition': 0.82, 'efficiency_factor': 0.96, 
                   'failure_tendency': 'lubrication', 'liner_condition': 0.7},
            'M6': {'age_years': 7, 'condition': 0.88, 'efficiency_factor': 0.99, 
                   'failure_tendency': 'normal', 'liner_condition': 0.75}
        }
        
        for mill_id, variations in mill_variations.items():
            configs[mill_id] = {**base_config, **variations}
            
        return configs
    
    def _generate_base_conditions(self):
        """
        Genera condiciones base que afectan a todos los molinos
        (mineral, ambiente, etc.)
        """
        # Crear índice temporal horario
        timestamps = pd.date_range(self.start_date, self.end_date, freq='H')
        n_points = len(timestamps)
        
        # Características del mineral (varían gradualmente por zonas minadas)
        work_index_base = 14.5  # kWh/t promedio
        work_index_variation = np.random.normal(0, 0.5, n_points)
        work_index_seasonal = 1.5 * np.sin(2 * np.pi * np.arange(n_points) / (365*24))
        work_index = work_index_base + work_index_variation + work_index_seasonal
        work_index = np.clip(work_index, 10, 20)  # Rango realista
        
        # Dureza mineral (correlacionada con work index)
        hardness = 3.5 + 0.2 * (work_index - 14.5) + np.random.normal(0, 0.3, n_points)
        hardness = np.clip(hardness, 3.0, 6.5)
        
        # Humedad mineral (estacional, mayor en temporada lluviosa)
        humidity_base = 8.0  # % promedio
        humidity_seasonal = 3.0 * np.sin(2 * np.pi * timestamps.dayofyear / 365 + np.pi)
        humidity_random = np.random.normal(0, 1.0, n_points)
        humidity = humidity_base + humidity_seasonal + humidity_random
        humidity = np.clip(humidity, 4, 12)
        
        # Condiciones ambientales (típicas de sierra peruana)
        ambient_temp = 18 + 8 * np.sin(2 * np.pi * timestamps.dayofyear / 365) + \
                      np.random.normal(0, 2, n_points)
        ambient_humidity = 65 + 15 * np.sin(2 * np.pi * timestamps.dayofyear / 365 + np.pi/2) + \
                          np.random.normal(0, 5, n_points)
        
        # Granulometría de alimentación (salida del SAG)
        f80_base = 12500  # μm promedio
        f80_variation = np.random.normal(0, 1000, n_points)
        f80 = f80_base + f80_variation
        f80 = np.clip(f80, 9000, 15000)
        
        return pd.DataFrame({
            'timestamp': timestamps,
            'work_index_bond': work_index,
            'dureza_mineral': hardness,
            'humedad_mineral': humidity,
            'temperatura_ambiente': ambient_temp,
            'humedad_relativa': ambient_humidity,
            'granulometria_feed_p80': f80,
            'densidad_mineral': np.random.normal(3.2, 0.2, n_points),
            'contenido_arcillas': np.random.uniform(0, 12, n_points),
            'abrasividad_ai': np.random.uniform(0.15, 0.65, n_points)
        })
    
    def _schedule_failures(self, mill_id, mill_config, timestamps):
        """
        Programa eventos de falla realistas durante el período de simulación
        """
        failures = []
        current_time = timestamps.iloc[0]  # Usar .iloc para acceder al primer elemento
        end_time = timestamps.iloc[-1]    # Usar .iloc para acceder al último elemento
        
        # Probabilidades de falla por tipo basadas en literatura
        failure_types = {
            'bearing_feed': 0.35,      # 35% de fallas
            'bearing_discharge': 0.35, # 35% de fallas  
            'liner_wear': 0.20,       # 20% de fallas
            'motor_electrical': 0.05,  # 5% de fallas
            'lubrication': 0.05       # 5% de fallas
        }
        
        # Ajustar probabilidades según tendencia del molino
        if mill_config['failure_tendency'] == 'bearings':
            failure_types['bearing_feed'] *= 1.5
            failure_types['bearing_discharge'] *= 1.5
        elif mill_config['failure_tendency'] == 'liners':
            failure_types['liner_wear'] *= 2.0
        elif mill_config['failure_tendency'] == 'lubrication':
            failure_types['lubrication'] *= 3.0
        
        # Normalizar probabilidades
        total_prob = sum(failure_types.values())
        failure_types = {k: v/total_prob for k, v in failure_types.items()}
        
        # Programar fallas (frecuencia basada en condición del molino)
        base_mtbf = 4380  # Horas promedio entre fallas (6 meses)
        mtbf = base_mtbf * mill_config['condition']  # Ajustar por condición
        
        while current_time < end_time:
            # Tiempo hasta próxima falla (distribución Weibull)
            time_to_failure = np.random.weibull(2) * mtbf
            failure_time = current_time + pd.Timedelta(hours=time_to_failure)
            
            if failure_time < end_time:
                # Seleccionar tipo de falla
                failure_type = np.random.choice(
                    list(failure_types.keys()),
                    p=list(failure_types.values())
                )
                
                # Severidad de la falla (1=menor, 2=moderada, 3=crítica)
                if failure_type in ['bearing_feed', 'bearing_discharge']:
                    severity = np.random.choice([1, 2, 3], p=[0.1, 0.6, 0.3])
                elif failure_type == 'liner_wear':
                    severity = np.random.choice([1, 2, 3], p=[0.3, 0.6, 0.1])
                else:
                    severity = np.random.choice([1, 2, 3], p=[0.5, 0.4, 0.1])
                
                failures.append({
                    'mill_id': mill_id,
                    'failure_time': failure_time,
                    'failure_type': failure_type,
                    'severity': severity
                })
                
                current_time = failure_time + pd.Timedelta(days=np.random.uniform(7, 30))
            else:
                break
                
        return failures
    
    def _generate_mill_operation(self, mill_id, base_conditions, mill_config):
        """
        Genera operación completa de un molino individual
        """
        timestamps = base_conditions['timestamp']
        n_points = len(timestamps)
        
        # Programar fallas para este molino
        mill_failures = self._schedule_failures(mill_id, mill_config, timestamps)
        self.scheduled_failures.extend(mill_failures)
        
        # Variables operacionales controlables
        # Feed rate: varía por turno y demanda operacional
        feed_rate_base = 280  # t/h promedio
        feed_rate_variation = np.random.normal(0, 20, n_points)
        
        # Variación por turnos (operadores diferentes)
        hour_of_day = timestamps.dt.hour
        turno_effect = np.where(hour_of_day < 8, -10,     # Turno A: más conservador
                               np.where(hour_of_day < 16, 5,  # Turno B: más agresivo
                                       0))                     # Turno C: normal
        
        feed_rate = feed_rate_base + feed_rate_variation + turno_effect
        feed_rate = np.clip(feed_rate, 180, 350)
        
        # Velocidad de rotación (% de velocidad crítica)
        speed_pct_critical = np.random.normal(76, 2, n_points)  # Óptimo ~76%
        speed_pct_critical = np.clip(speed_pct_critical, 70, 85)
        speed_rpm = speed_pct_critical * mill_config['critical_speed'] / 100
        
        # Nivel de carga de bolas
        ball_charge = np.random.normal(32, 1.5, n_points)  # Óptimo ~32%
        ball_charge = np.clip(ball_charge, 28, 36)
        
        # Densidad de pulpa
        pulp_density = np.random.normal(72, 3, n_points)  # % sólidos
        pulp_density = np.clip(pulp_density, 68, 78)
        
        # Calcular variables derivadas usando física
        # Energía específica según Bond
        p80_target = 125  # μm target
        bond_energy = self.physics.calculate_bond_energy(
            base_conditions['work_index_bond'],
            base_conditions['granulometria_feed_p80'],
            p80_target
        )
        
        # Eficiencia real del molino
        liner_wear = np.random.uniform(0, 80, n_points)  # % desgaste liners
        mill_efficiency = self.physics.calculate_mill_efficiency(
            liner_wear, ball_charge, speed_pct_critical
        )
        mill_efficiency *= mill_config['efficiency_factor']
        
        # Consumo energético real
        energy_specific = bond_energy / mill_efficiency
        power_draw = energy_specific * feed_rate
        
        # Variables condition monitoring
        # Carga en rodamientos
        bearing_load = self.physics.calculate_bearing_load_factor(
            power_draw, speed_rpm, misalignment=0.02  # 2% misalignment típico
        )
        
        # Generar señales de vibración base
        vibration_base_feed = 3.5 * bearing_load * mill_config['condition']
        vibration_base_discharge = 4.0 * bearing_load * mill_config['condition']
        vibration_shell = 5.0 * np.sqrt(power_draw / 2000) * mill_config['condition']
        
        # Temperaturas base
        temp_bearing_feed = 45 + 15 * (bearing_load - 1) + base_conditions['temperatura_ambiente'] * 0.3
        temp_bearing_discharge = 48 + 18 * (bearing_load - 1) + base_conditions['temperatura_ambiente'] * 0.3
        temp_motor = 60 + 20 * (power_draw / mill_config['motor_power_rating'] - 1)
        
        # Sistema de lubricación
        oil_pressure = np.random.normal(2.5, 0.3, n_points)
        oil_flow = np.random.normal(120, 15, n_points)
        oil_quality = 100 - np.random.exponential(2, n_points)  # Degrada con el tiempo
        oil_quality = np.clip(oil_quality, 70, 100)
        
        # Variables eléctricas
        motor_current = power_draw / (mill_config['motor_power_rating'] * 0.9) * 800
        motor_voltage = np.random.normal(4160, 20, n_points)
        power_factor = np.random.normal(0.90, 0.02, n_points)
        
        # Aplicar efectos de degradación y fallas
        vibration_feed_h, vibration_feed_v = self._apply_degradation_effects(
            timestamps, mill_failures, vibration_base_feed, 'vibration'
        )
        vibration_discharge_h, vibration_discharge_v = self._apply_degradation_effects(
            timestamps, mill_failures, vibration_base_discharge, 'vibration'
        )
        
        temp_bearing_feed = self._apply_degradation_effects(
            timestamps, mill_failures, temp_bearing_feed, 'temperature'
        )[0]
        
        # Crear DataFrame con todas las variables
        mill_data = pd.DataFrame({
            # Identificadores
            'timestamp': timestamps,
            'molino_id': mill_id,
            'turno': pd.cut(timestamps.dt.hour, bins=[0, 8, 16, 24], 
                           labels=['A', 'B', 'C'], include_lowest=True),
            
            # Variables de proceso
            'feed_rate': feed_rate,
            'velocidad_rotacion': speed_rpm,
            'velocidad_porcentaje_critica': speed_pct_critical,
            'nivel_carga_bolas': ball_charge,
            'densidad_pulpa': pulp_density,
            'agua_adicionada': feed_rate * (100/pulp_density - 1) * 0.8,  # m³/h estimado
            'presion_ciclones': np.random.normal(95, 15, n_points),
            
            # Condition monitoring - vibración
            'vibracion_cojinete_feed_h': vibration_feed_h,
            'vibracion_cojinete_feed_v': vibration_feed_v,
            'vibracion_cojinete_discharge_h': vibration_discharge_h,
            'vibracion_cojinete_discharge_v': vibration_discharge_v,
            'vibracion_shell_h': vibration_shell * np.random.normal(1, 0.05, n_points),
            'vibracion_shell_v': vibration_shell * np.random.normal(1, 0.05, n_points),
            'vibracion_pinion': vibration_shell * 1.2 * np.random.normal(1, 0.08, n_points),
            'vibracion_gearbox': vibration_shell * 0.8 * np.random.normal(1, 0.06, n_points),
            
            # Condition monitoring - temperatura
            'temp_cojinete_feed': temp_bearing_feed,
            'temp_cojinete_discharge': temp_bearing_discharge,
            'temp_aceite_lubricacion': np.random.normal(55, 5, n_points),
            'temp_motor_principal': temp_motor,
            'temp_gearbox': np.random.normal(58, 6, n_points),
            
            # Variables eléctricas
            'corriente_motor': motor_current,
            'potencia_activa': power_draw,
            'voltaje_motor': motor_voltage,
            'factor_potencia': power_factor,
            
            # Sistema lubricación
            'presion_aceite_principal': oil_pressure,
            'flujo_aceite': oil_flow,
            'nivel_tanque_aceite': np.random.uniform(40, 90, n_points),
            'calidad_aceite_ppm': (100 - oil_quality) / 5,  # Convert to ppm
            
            # Performance variables
            'consumo_energetico_especifico': energy_specific,
            'throughput_real': feed_rate * np.random.normal(0.95, 0.02, n_points),
            'eficiencia_molienda': mill_efficiency * 100,
            'granulometria_producto_p80': p80_target * np.random.normal(1, 0.08, n_points),
            
            # Estado equipos
            'nivel_desgaste_liners': liner_wear,
            'horas_operacion_acumuladas': np.arange(n_points),
            'ciclos_arranque_parada': np.random.poisson(1, n_points),
            
            # Contexto operacional
            'carga_circulante': np.random.normal(250, 50, n_points),
            'eficiencia_clasificacion': np.random.normal(60, 8, n_points)
        })
        
        # Agregar características del mineral
        for col in ['work_index_bond', 'dureza_mineral', 'humedad_mineral', 
                   'granulometria_feed_p80', 'densidad_mineral', 'contenido_arcillas', 
                   'abrasividad_ai', 'temperatura_ambiente', 'humedad_relativa']:
            mill_data[col] = base_conditions[col]
        
        # Generar targets para predicción de fallas
        mill_data = self._generate_failure_targets(mill_data, mill_failures)
        
        # Aplicar ruido realista de sensores
        mill_data = self._apply_sensor_noise(mill_data)
        
        return mill_data
    
    def _apply_degradation_effects(self, timestamps, failures, base_signal, signal_type):
        """
        Aplica efectos de degradación realistas basados en fallas programadas
        """
        signal_degraded = base_signal.copy()
        signal_degraded_v = base_signal.copy() * np.random.normal(0.95, 0.05, len(base_signal))
        
        for failure in failures:
            failure_time = failure['failure_time']
            failure_type = failure['failure_type']
            
            # Encontrar índices en ventana de degradación
            time_diff = (failure_time - timestamps).dt.total_seconds() / 3600  # horas
            degradation_mask = (time_diff > 0) & (time_diff < 720)  # 30 días antes
            
            if degradation_mask.any():
                indices = np.where(degradation_mask)[0]
                hours_to_failure = time_diff[indices]
                
                if 'bearing' in failure_type and signal_type == 'vibration':
                    # Aplicar degradación de rodamiento
                    for i, idx in enumerate(indices):
                        degraded_value = self.degradation.generate_bearing_degradation(
                            base_signal.iloc[idx], hours_to_failure.iloc[i], failure_type
                        )
                        signal_degraded.iloc[idx] = degraded_value
                        signal_degraded_v.iloc[idx] = degraded_value * np.random.normal(0.98, 0.03)
                
                elif signal_type == 'temperature':
                    # Incremento gradual de temperatura
                    temp_increase = 2.0 * (1 - hours_to_failure / 720)  # Hasta +2°C
                    signal_degraded.iloc[indices] += temp_increase
        
        return signal_degraded, signal_degraded_v
    
    def _generate_failure_targets(self, mill_data, failures):
        """
        Genera variables target para predicción de fallas
        """
        timestamps = mill_data['timestamp']
        n_points = len(timestamps)
        
        # Inicializar targets
        mill_data['falla_en_7d'] = False
        mill_data['falla_en_14d'] = False
        mill_data['falla_en_30d'] = False
        mill_data['tipo_falla'] = 'normal'
        mill_data['severidad_falla'] = 0
        mill_data['dias_hasta_falla'] = 365.0
        
        for failure in failures:
            failure_time = failure['failure_time']
            failure_type = failure['failure_type']
            severity = failure['severity']
            
            # Calcular días hasta falla para cada timestamp
            days_to_failure = (failure_time - timestamps).dt.total_seconds() / 86400
            
            # Marcar targets en ventanas apropiadas
            mask_7d = (days_to_failure > 0) & (days_to_failure <= 7)
            mask_14d = (days_to_failure > 0) & (days_to_failure <= 14)
            mask_30d = (days_to_failure > 0) & (days_to_failure <= 30)
            
            mill_data.loc[mask_7d, 'falla_en_7d'] = True
            mill_data.loc[mask_14d, 'falla_en_14d'] = True
            mill_data.loc[mask_30d, 'falla_en_30d'] = True
            mill_data.loc[mask_30d, 'tipo_falla'] = failure_type
            mill_data.loc[mask_30d, 'severidad_falla'] = severity
            
            # Actualizar días hasta falla (tomar el mínimo si hay múltiples fallas)
            mill_data.loc[mask_30d, 'dias_hasta_falla'] = np.minimum(
                mill_data.loc[mask_30d, 'dias_hasta_falla'],
                days_to_failure[mask_30d]
            )
        
        return mill_data
    
    def _apply_sensor_noise(self, mill_data):
        """
        Aplica ruido realista de sensores industriales
        """
        # Mapeo de columnas a tipos de sensor
        sensor_mapping = {
            'vibration': [col for col in mill_data.columns if 'vibracion' in col],
            'temperature': [col for col in mill_data.columns if 'temp' in col],
            'electrical': ['corriente_motor', 'potencia_activa', 'voltaje_motor', 'factor_potencia'],
            'process': ['feed_rate', 'densidad_pulpa', 'presion_ciclones', 'agua_adicionada']
        }
        
        for sensor_type, columns in sensor_mapping.items():
            for col in columns:
                if col in mill_data.columns:
                    mill_data[col] = self.noise.add_sensor_noise(
                        mill_data[col], sensor_type, mill_data['timestamp']
                    )
        
        return mill_data
    
    def generate_complete_dataset(self):
        """
        Genera el dataset completo para todos los molinos
        """
        print("🔄 Iniciando generación de dataset sintético...")
        print(f"📅 Período: {self.start_date.date()} a {self.end_date.date()}")
        print(f"⚙️  Molinos: 6 unidades (M1-M6)")
        
        # Generar condiciones base comunes
        print("🌍 Generando condiciones base (mineral, ambiente)...")
        base_conditions = self._generate_base_conditions()
        
        # Lista para almacenar datos de todos los molinos
        all_mill_data = []
        
        # Generar datos para cada molino
        for mill_id in ['M1', 'M2', 'M3', 'M4', 'M5', 'M6']:
            print(f"⚙️  Generando datos para {mill_id}...")
            mill_config = self.mill_configs[mill_id]
            
            # Generar operación del molino
            mill_data = self._generate_mill_operation(mill_id, base_conditions, mill_config)
            all_mill_data.append(mill_data)
        
        # Combinar todos los datos
        print("🔗 Combinando datos de todos los molinos...")
        complete_dataset = pd.concat(all_mill_data, ignore_index=True)
        
        # Ordenar por timestamp y molino
        complete_dataset = complete_dataset.sort_values(['timestamp', 'molino_id']).reset_index(drop=True)
        
        # Agregar variables derivadas finales
        complete_dataset = self._add_derived_features(complete_dataset)
        
        # Resumen estadístico
        self._print_dataset_summary(complete_dataset)
        
        return complete_dataset
    
    def _add_derived_features(self, dataset):
        """
        Agrega variables derivadas y features engineered
        """
        print("🧮 Calculando variables derivadas...")
        
        # Features de tendencia (rolling windows)
        for mill_id in dataset['molino_id'].unique():
            mill_mask = dataset['molino_id'] == mill_id
            mill_data = dataset[mill_mask].copy()
            
            # Tendencias de vibración (7 días)
            dataset.loc[mill_mask, 'vibracion_trend_7d'] = (
                mill_data['vibracion_cojinete_feed_h'].rolling(window=168, min_periods=24).mean()
            )
            
            # Tendencias de temperatura (7 días)
            dataset.loc[mill_mask, 'temperatura_trend_7d'] = (
                mill_data['temp_cojinete_feed'].rolling(window=168, min_periods=24).mean()
            )
            
            # Tendencias de energía (24 horas)
            dataset.loc[mill_mask, 'energia_trend_24h'] = (
                mill_data['consumo_energetico_especifico'].rolling(window=24, min_periods=12).mean()
            )
            
            # Tendencias de throughput (24 horas)
            dataset.loc[mill_mask, 'throughput_trend_24h'] = (
                mill_data['throughput_real'].rolling(window=24, min_periods=12).mean()
            )
        
        # Ratios y métricas compuestas
        dataset['ratio_p80_feed_producto'] = (
            dataset['granulometria_feed_p80'] / dataset['granulometria_producto_p80']
        )
        
        dataset['potencia_especifica_neta'] = (
            dataset['potencia_activa'] / dataset['throughput_real']
        )
        
        # Eficiencia energética teórica vs real
        theoretical_energy = self.physics.calculate_bond_energy(
            dataset['work_index_bond'],
            dataset['granulometria_feed_p80'],
            dataset['granulometria_producto_p80']
        )
        dataset['eficiencia_energetica_teorica'] = theoretical_energy / dataset['consumo_energetico_especifico']
        
        # Anomaly scores básicos (Z-scores)
        for mill_id in dataset['molino_id'].unique():
            mill_mask = dataset['molino_id'] == mill_id
            mill_data = dataset[mill_mask]
            
            # Score de anomalía en vibración
            vibration_composite = (
                mill_data['vibracion_cojinete_feed_h'] + 
                mill_data['vibracion_cojinete_discharge_h']
            ) / 2
            dataset.loc[mill_mask, 'anomaly_score_vibration'] = np.abs(
                stats.zscore(vibration_composite, nan_policy='omit')
            )
            
            # Score de anomalía eléctrica
            electrical_composite = mill_data['corriente_motor'] / mill_data['corriente_motor'].mean()
            dataset.loc[mill_mask, 'anomaly_score_electrical'] = np.abs(
                stats.zscore(electrical_composite, nan_policy='omit')
            )
        
        return dataset
    
    def _print_dataset_summary(self, dataset):
        """
        Imprime resumen estadístico del dataset generado
        """
        print("\n" + "="*60)
        print("📊 RESUMEN DEL DATASET GENERADO")
        print("="*60)
        
        print(f"📏 Dimensiones: {dataset.shape[0]:,} filas × {dataset.shape[1]} columnas")
        print(f"💾 Tamaño estimado: {dataset.memory_usage(deep=True).sum() / 1024**2:.1f} MB")
        print(f"📅 Período: {dataset['timestamp'].min()} a {dataset['timestamp'].max()}")
        
        print(f"\n⚙️  MOLINOS:")
        for mill_id in sorted(dataset['molino_id'].unique()):
            mill_data = dataset[dataset['molino_id'] == mill_id]
            print(f"   {mill_id}: {len(mill_data):,} registros")
        
        print(f"\n🚨 EVENTOS DE FALLA:")
        failure_summary = dataset[dataset['falla_en_30d'] == True].groupby(['molino_id', 'tipo_falla']).size().unstack(fill_value=0)
        if not failure_summary.empty:
            print(failure_summary)
        
        total_failures = len(dataset[dataset['falla_en_7d'] == True])
        print(f"   Total eventos en ventana 7d: {total_failures}")
        
        print(f"\n📈 ESTADÍSTICAS CLAVE:")
        key_vars = ['consumo_energetico_especifico', 'throughput_real', 'vibracion_cojinete_feed_h', 'temp_cojinete_feed']
        for var in key_vars:
            if var in dataset.columns:
                print(f"   {var}: {dataset[var].mean():.2f} ± {dataset[var].std():.2f}")
        
        print(f"\n✅ Dataset generado exitosamente!")
        print("="*60)
    
    def save_dataset(self, dataset, filepath='molinos_dataset.csv', format='csv'):
        """
        Guarda el dataset en formato CSV o Parquet
        """
        print(f"💾 Guardando dataset en: {filepath}")
        
        # Optimizar tipos de datos
        for col in dataset.columns:
            if dataset[col].dtype == 'object' and col not in ['timestamp', 'molino_id', 'turno', 'tipo_falla']:
                dataset[col] = pd.to_numeric(dataset[col], errors='ignore')
        
        # Guardar según formato especificado
        if format.lower() == 'csv' or filepath.endswith('.csv'):
            dataset.to_csv(filepath, index=False, sep=',')
        else:
            dataset.to_parquet(filepath, compression='snappy', index=False)
        
        print(f"✅ Dataset guardado: {filepath}")
        return filepath
    
    def create_specialized_views(self, dataset):
        """
        Crea vistas especializadas del dataset
        """
        print("📋 Creando vistas especializadas...")
        
        # Vista Condition Monitoring (para predicción de fallas)
        cm_columns = [
            'timestamp', 'molino_id', 'turno',
            # Sensores críticos
            'vibracion_cojinete_feed_h', 'vibracion_cojinete_feed_v',
            'vibracion_cojinete_discharge_h', 'vibracion_cojinete_discharge_v',
            'vibracion_shell_h', 'vibracion_shell_v', 'vibracion_pinion', 'vibracion_gearbox',
            'temp_cojinete_feed', 'temp_cojinete_discharge', 'temp_aceite_lubricacion',
            'temp_motor_principal', 'temp_gearbox',
            'corriente_motor', 'potencia_activa', 'voltaje_motor',
            'presion_aceite_principal', 'flujo_aceite', 'calidad_aceite_ppm',
            'horas_operacion_acumuladas', 'velocidad_rotacion',
            # Targets de falla
            'falla_en_7d', 'falla_en_14d', 'falla_en_30d', 'tipo_falla', 'severidad_falla', 'dias_hasta_falla',
            # Features derivadas
            'vibracion_trend_7d', 'temperatura_trend_7d', 'anomaly_score_vibration', 'anomaly_score_electrical'
        ]
        
        condition_monitoring_view = dataset[cm_columns].copy()
        
        # Vista Process Optimization (agregada por turno para optimización energética)
        process_columns = [
            'timestamp', 'molino_id', 'turno',
            # Variables controlables
            'feed_rate', 'velocidad_rotacion', 'velocidad_porcentaje_critica',
            'nivel_carga_bolas', 'densidad_pulpa', 'agua_adicionada', 'presion_ciclones',
            # Características mineral
            'work_index_bond', 'dureza_mineral', 'humedad_mineral', 'granulometria_feed_p80',
            'densidad_mineral', 'contenido_arcillas', 'abrasividad_ai',
            # Performance
            'consumo_energetico_especifico', 'throughput_real', 'eficiencia_molienda',
            'granulometria_producto_p80', 'potencia_activa',
            # Estado equipos
            'nivel_desgaste_liners', 'carga_circulante', 'eficiencia_clasificacion',
            # Features derivadas
            'energia_trend_24h', 'throughput_trend_24h', 'ratio_p80_feed_producto',
            'potencia_especifica_neta', 'eficiencia_energetica_teorica'
        ]
        
        # Agregar por turno (cada 8 horas)
        process_optimization_view = dataset[process_columns].copy()
        process_optimization_view['turno_timestamp'] = (
            process_optimization_view['timestamp'].dt.floor('8H')
        )
        
        # Agrupar por turno y tomar promedios
        aggregation_dict = {col: 'mean' for col in process_columns if col not in ['timestamp', 'molino_id', 'turno']}
        aggregation_dict.update({
            'timestamp': 'first',
            'turno': 'first'
        })
        
        process_optimization_view = (
            process_optimization_view.groupby(['molino_id', 'turno_timestamp'])
            .agg(aggregation_dict)
            .reset_index()
            .drop('turno_timestamp', axis=1)
        )
        
        return condition_monitoring_view, process_optimization_view


def main():
    """
    Función principal para generar el dataset completo
    """
    print("🏭 GENERADOR DE DATOS SINTÉTICOS - MOLINOS DE BOLAS MINERAPERU")
    print("=" * 70)
    
    # Inicializar generador
    generator = RealisticMillDataGenerator(
        start_date='2023-01-01',
        duration_years=2.5
    )
    
    # Generar dataset completo
    dataset = generator.generate_complete_dataset()
    
    # Guardar dataset principal
    filepath = generator.save_dataset(dataset, 'molinos_mineraperu_dataset.csv')
    
    # Crear vistas especializadas
    cm_view, opt_view = generator.create_specialized_views(dataset)
    
    # Guardar vistas en CSV
    generator.save_dataset(cm_view, 'condition_monitoring_view.csv')
    generator.save_dataset(opt_view, 'process_optimization_view.csv')
    
    print("\n🎯 ARCHIVOS GENERADOS:")
    print("   📄 molinos_mineraperu_dataset.csv (Dataset principal)")
    print("   📄 condition_monitoring_view.csv (Vista predicción fallas)")
    print("   📄 process_optimization_view.csv (Vista optimización energética)")
    
    return dataset, cm_view, opt_view


# Función de utilidad para cargar y explorar el dataset
def load_and_explore_dataset(filepath='molinos_mineraperu_dataset.csv'):
    """
    Carga y proporciona exploración básica del dataset
    """
    print(f"📂 Cargando dataset: {filepath}")
    
    # Detectar formato automáticamente
    if filepath.endswith('.csv'):
        dataset = pd.read_csv(filepath, parse_dates=['timestamp'])
    else:
        dataset = pd.read_parquet(filepath)
    
    print(f"✅ Dataset cargado: {dataset.shape[0]:,} registros")
    
    # Exploración básica
    print("\n📊 INFORMACIÓN BÁSICA:")
    print(f"   Período: {dataset['timestamp'].min()} a {dataset['timestamp'].max()}")
    print(f"   Molinos: {sorted(dataset['molino_id'].unique())}")
    print(f"   Variables: {len(dataset.columns)} columnas")
    
    # Estadísticas de fallas
    print("\n🚨 ESTADÍSTICAS DE FALLAS:")
    for period in ['falla_en_7d', 'falla_en_14d', 'falla_en_30d']:
        if period in dataset.columns:
            count = dataset[period].sum()
            percentage = (count / len(dataset)) * 100
            print(f"   {period}: {count:,} eventos ({percentage:.2f}%)")
    
    return dataset


if __name__ == "__main__":
    # Ejecutar generación completa
    dataset, cm_view, opt_view = main()