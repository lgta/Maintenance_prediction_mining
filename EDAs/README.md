# Generación de Datos Sintéticos para Chancadoras Cónicas

Este repositorio contiene un notebook de Python que genera un dataset sintético simulado de sensores y fallas para 3 chancadoras cónicas secundarias, utilizadas en procesos de chancado en minería.

## 📦 Contenido

- `generar_datos_sinteticos_chancadoras_2anios.ipynb`: Notebook con la lógica completa de generación.
- `datos_sinteticos_chancadoras_2anios.csv` (output): Archivo CSV que contiene los datos generados.

## 📅 Detalles del Dataset

- **Periodo:** 2 años (2023–2025)
- **Frecuencia temporal:** Cada 30 minutos
- **Unidades monitoreadas:** 3 chancadoras (C1, C2, C3)
- **Registros:** ~105,000 observaciones
- **Variables:** 24 campos operativos + 6 de fallas

## 🧠 Variables principales

- Condiciones operativas: alimentación (`feed_rate_tph`), corriente, potencia, temperaturas, vibraciones, voltaje, etc.
- Propiedades del mineral: abrasividad, dureza.
- Ciclo de operación: horas acumuladas, ciclos de arranque/parada.
- Lógica de fallas: `falla_en_7d`, `falla_ocurrida`, `tipo_falla`, `modo_falla`, `componente_falla`, `sistema_afectado`.
