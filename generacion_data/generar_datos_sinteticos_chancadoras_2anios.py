
import pandas as pd
import numpy as np

# Parámetros
num_chancadoras = 3
start_date = "2023-01-01"
end_date = "2025-01-01"
freq = "30min"

# Crear timestamps cada 30 minutos por 2 años
timestamps = pd.date_range(start=start_date, end=end_date, freq=freq, inclusive="left")

# Inicializar lista para guardar los DataFrames
data = []

for cid in range(1, num_chancadoras + 1):
    n = len(timestamps)
    turno = np.where((timestamps.hour >= 6) & (timestamps.hour < 18), "Día", "Noche")
    df = pd.DataFrame({
        "timestamp": timestamps,
        "chancadora_id": cid,
        "turno": turno,
        "feed_rate_tph": np.clip(np.random.normal(700, 50, size=n), 400, 1000),
        "corriente_motor": np.clip(np.random.normal(220, 10, size=n), 180, 260),
        "potencia_motor_kw": np.clip(np.random.normal(280, 20, size=n), 180, 350),
        "temp_aceite": np.clip(np.random.normal(55, 5, size=n), 40, 70),
        "temp_motor": np.clip(np.random.normal(60, 7, size=n), 40, 80),
        "temp_eje_principal": np.clip(np.random.normal(60, 6, size=n), 45, 75),
        "temp_bocina_conica": np.clip(np.random.normal(58, 6, size=n), 40, 75),
        "vibracion_bowl": np.clip(np.random.normal(1.8, 0.4, size=n), 0.5, 4.5),
        "vibracion_eje_principal": np.clip(np.random.normal(2.0, 0.5, size=n), 0.5, 5.0),
        "vibracion_manto": np.clip(np.random.normal(2.2, 0.6, size=n), 0.5, 5.5),
        "vibracion_pinion": np.clip(np.random.normal(1.7, 0.3, size=n), 0.5, 4.0),
        "voltaje_motor": np.clip(np.random.normal(420, 10, size=n), 380, 460),
        "factor_potencia": np.round(np.random.uniform(0.85, 1.0, size=n), 3),
        "abrasividad_ai": np.round(np.random.uniform(0.1, 0.6, size=n), 2),
        "dureza_mineral": np.random.randint(1, 6, size=n),
        "horas_operacion_acumuladas": np.mod(np.arange(n) / 2, 720),
        "ciclos_arranque_parada": np.random.poisson(lam=0.005, size=n).cumsum(),
        "falla_en_7d": np.random.choice([0, 1], size=n, p=[0.965, 0.035])
    })

    # Inicializar columnas de falla
    df["tipo_falla"] = None
    df["modo_falla"] = None
    df["componente_falla"] = None
    df["severidad_falla"] = None
    df["falla_ocurrida"] = 0
    df["componente_falla_confirmado"] = None
    df["sistema_afectado"] = None

    # Aplicar lógica de fallas condicional
    tipo_falla_choices = ["Mecánica", "Lubricación", "Eléctrica"]
    modo_falla_choices = ["Desgaste", "Sobrecalentamiento", "Vibración"]
    componente_falla_choices = ["Forros", "Bocina", "Cojinete", "Piñón", "Tanque de aceite"]
    severidad_falla_choices = [1, 2, 3]

    idxs_alerta = df[df["falla_en_7d"] == 1].index
    for idx in idxs_alerta:
        tipo = np.random.choice(tipo_falla_choices)
        modo = np.random.choice(modo_falla_choices)
        componente = np.random.choice(componente_falla_choices)
        severidad = np.random.choice(severidad_falla_choices)

        df.at[idx, "tipo_falla"] = tipo
        df.at[idx, "modo_falla"] = modo
        df.at[idx, "componente_falla"] = componente
        df.at[idx, "severidad_falla"] = severidad

        # Simular ocurrencia real de la falla
        idx_ocurrencia = min(idx + np.random.randint(12, 96), n - 1)
        df.at[idx_ocurrencia, "falla_ocurrida"] = 1
        df.at[idx_ocurrencia, "componente_falla_confirmado"] = componente

        if tipo == "Mecánica":
            sistema = "Sistema mecánico"
        elif tipo == "Lubricación":
            sistema = "Sistema de lubricación"
        elif tipo == "Eléctrica":
            sistema = "Sistema eléctrico"
        else:
            sistema = None
        df.at[idx_ocurrencia, "sistema_afectado"] = sistema

    data.append(df)

# Concatenar todos los datos
df_final = pd.concat(data, ignore_index=True)

# Guardar a CSV
df_final.to_csv("datos_sinteticos_chancadoras_2anios.csv", index=False)
