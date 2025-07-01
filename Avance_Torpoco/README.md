# Avance Torpoco - Análisis de Fallas en Molinos

Este directorio contiene los archivos de análisis de datos para predicción de fallas en molinos de bolas desarrollados por el equipo.

## 📁 Estructura de Archivos

```
Avance_Torpoco/
├── README.md                           # Este archivo (instrucciones)
├── requirements.txt                    # Dependencias de Python
├── 📊 NOTEBOOKS
│   ├── summary_shift.ipynb            # Procesamiento de datos por turnos/días
│   └── full_mill_analysis_step.ipynb  # Análisis completo paso a paso
├── 🐍 MÓDULOS PYTHON
│   ├── analysis.py                    # Funciones de análisis exploratorio
│   ├── data_loader.py                 # Carga y preprocesamiento de datos
│   ├── model.py                       # Entrenamiento y evaluación de modelos
│   ├── variable_filter.py             # Filtros y grupos de variables
│   ├── visualization.py               # Funciones de visualización
│   └── main_example.py                # Ejemplo de uso desde línea de comandos
```

## 🚀 Configuración Inicial

### 1. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 2. Configurar Jupyter (opcional)

```bash
jupyter notebook
# o
jupyter lab
```

## ⚠️ IMPORTANTE: Configurar Rutas de Archivos

**ANTES de ejecutar cualquier notebook o script, debes cambiar las rutas de archivos para que coincidan con tu sistema.**

### Archivos que requieren configuración de rutas:

#### 📝 `summary_shift.ipynb`
```python
# CAMBIAR estas líneas (al inicio del notebook):
DATA_FILE = "molinos_mineraperu_dataset.csv"   # ← TU archivo CSV
OUT_DIR   = "DataMolinos"                      # ← TU carpeta de salida
```

#### 📝 `full_mill_analysis_step.ipynb`
```python
# CAMBIAR estas líneas (celda de configuración):
DATA_PATH = "molinos_shift_summary_full.csv"    # ← TU archivo CSV
OUTPUT_DIR = "resultados/"                      # ← TU carpeta de resultados
```

#### 🐍 `main_example.py`
```bash
# Usar desde línea de comandos:
python main_example.py "ruta/a/tu/archivo.csv"
```

## 📖 Guía de Uso

### Opción 1: Procesamiento de Datos Crudos → Resumen

Si tienes **datos crudos** de molinos:

1. **Ejecutar `summary_shift.ipynb`**
   - Cambia `DATA_FILE` por la ruta a tu archivo CSV crudo
   - Ejecuta todas las celdas
   - Genera archivos resumen procesados

2. **Ejecutar `full_mill_analysis_step.ipynb`**
   - Cambia `DATA_PATH` al archivo generado en el paso 1
   - Ejecuta el análisis completo

### Opción 2: Datos Ya Procesados → Análisis Directo

Si ya tienes **datos agregados/resumidos**:

1. **Ejecutar directamente `full_mill_analysis_step.ipynb`**
   - Cambia `DATA_PATH` a tu archivo de datos procesados
   - Ejecuta el análisis completo

### Opción 3: Uso Programático

```python
# Usar los módulos directamente
from data_loader import load_and_preprocess_data
from analysis import describe_numeric, correlation_with_target
from model import train_failure_classifier

# Cargar datos
X, y = load_and_preprocess_data("tu_archivo.csv")

# Análisis exploratorio
stats = describe_numeric(X)
correlations = correlation_with_target(pd.concat([X, y], axis=1), 'falla_en_30d')

# Entrenar modelo
model, auc = train_failure_classifier(X, y)
print(f"AUC: {auc:.3f}")
```

## 📊 Notebooks Detallados

### `summary_shift.ipynb`
**Propósito**: Procesar datos crudos de molinos y generar resúmenes estadísticos.

**Input esperado**: 
- CSV con columnas: `timestamp`, `molino_id`, variables de sensores
- Datos a nivel de muestra (granularidad alta)

**Output generado**:
- `molinos_day_summary_full.csv` - Resumen diario
- `molinos_day_summary_full_120.csv` - Resumen con ventana de 120h

**Características creadas**:
- Estadísticos por día: mean, std, min, max, p95
- Z-scores vs histórico del molino
- Tendencias (slopes)
- Flags de falla (7d, 14d, 30d)

### `full_mill_analysis_step.ipynb`
**Propósito**: Análisis completo de ML para predicción de fallas.

**Input esperado**:
- CSV procesado (de `summary_shift.ipynb` o similar)
- Columna target: `falla_en_30d`

**Output generado**:
- Datos preprocesados
- Modelos entrenados (.pkl)
- Visualizaciones (.png)
- Reporte final (.md)
- Métricas de evaluación (.csv)

**Incluye**:
- Análisis exploratorio completo
- Benchmark de múltiples modelos
- Validación cruzada
- Importancia de características
- Visualizaciones automáticas

## 🔧 Solución de Problemas Comunes

### Error: "No se encontró el archivo"
```python
# Verificar ruta absoluta
import os
print(os.path.abspath("tu_archivo.csv"))
```

### Error: "Columna no encontrada"
```python
# Verificar columnas en tu CSV
df = pd.read_csv("tu_archivo.csv")
print(df.columns.tolist())
```

### Error: "Module not found"
```bash
# Reinstalar dependencias
pip install -r requirements.txt
```

## 🎯 Variables Objetivo

El análisis está configurado para predecir:
- `falla_en_30d` - Falla en los próximos 30 días (variable principal)
- `falla_en_14d` - Falla en los próximos 14 días
- `falla_en_7d` - Falla en los próximos 7 días

## 📈 Métricas de Evaluación

- **ROC-AUC**: Métrica principal (separación de clases)
- **Precision/Recall**: Balance entre falsas alarmas y detección
- **F1-Score**: Métrica balanceada
- **Cross-Validation**: Validación robusta (5-fold)

## 🚨 Notas Importantes

1. **Dependencias de Rutas**: Todos los archivos que cargan datos requieren configuración manual de rutas
2. **Formato de Fechas**: El código asume formato DD/MM/YYYY en timestamps
3. **Memoria**: Archivos grandes pueden requerir optimización de memoria
4. **Columnas**: Verificar que las columnas esperadas existan en tus datos
5. **Target**: La columna objetivo debe llamarse exactamente `falla_en_30d`

## 💡 Tips de Uso

- **Empezar pequeño**: Prueba con un subset de datos primero
- **Verificar output**: Revisa los archivos generados antes de continuar
- **Logs**: Los notebooks muestran progreso y estadísticas útiles
- **Backup**: Guarda copias de tus datos originales
- **Documentar**: Anota los cambios que hagas a las rutas y parámetros

---

*Desarrollado por el equipo Torpoco - BREIT MINING G1*