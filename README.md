# Proyecto BREIT - MINERIA G1

Un proyecto de análisis de datos y machine learning usando Python y Quarto para documentación reproducible.

## 🛠️ Tecnologías Utilizadas

- **Python** - Lenguaje principal
- **Quarto** - Documentación y reportes reproducibles
- **UV** - Gestor de dependencias moderno y rápido
- **Virtual Environment** - Aislamiento de dependencias

## 📋 Requisitos Previos

### 1. Python
Asegúrate de tener Python 3.8+ instalado:
```bash
python --version
```

### 2. UV (Recomendado)
Instala UV como gestor de dependencias:
```bash
# En macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# En Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# O usando pip
pip install uv
```

### 3. Quarto
Instala Quarto desde su [página oficial](https://quarto.org/docs/get-started/):

**macOS:**
```bash
brew install quarto
```

**Windows:**
Descarga el instalador desde [quarto.org](https://quarto.org/docs/get-started/)

**Linux:**
```bash
# Ubuntu/Debian
sudo curl -LO https://quarto.org/download/latest/quarto-linux-amd64.deb
sudo gdebi quarto-linux-amd64.deb
```

Verifica la instalación:
```bash
quarto --version
```
**INSTALAR EXTENSION DE QUARTO EN VSCODE**

## 🚀 Configuración del Proyecto

### 1. Clonar el Repositorio
```bash
git clone https://github.com/tu-usuario/tu-repositorio.git
cd tu-repositorio
```

### 2. Crear Entorno Virtual con UV
```bash
# Crear entorno virtual usando UV
uv venv

# Activar entorno virtual
# En Windows
.venv\Scripts\activate

# En macOS/Linux
source .venv/bin/activate
```

### 3. Instalar Dependencias con UV
```bash
# Instalar todas las dependencias desde pyproject.toml
uv sync

# O alternativamente
uv pip install -e .
```

## 📁 Estructura del Proyecto

```
BREIT MINING CASE/
├── .venv/                              # Entorno virtual (creado con uv)
├── data/                               # Datos del proyecto
│   ├── assets/                         # Recursos adicionales
│   ├── RUTAS.md                        # Documentación de fuentes
│   ├── diccionario_X_detalle.qmd      # Diccionario de datos
├── generacion_data/                   # Scripts de generación
├── EDAs/                              # Scripts de análisis exploratorio
│   ├── EDA_*.qmd                      # Análisis exploratorio de datos
├── pyproject.toml                     # Configuración y dependencias
├── uv.lock                            # Lock file de UV (si existe)
└── README.md                          # Este archivo
```

## 🔧 Uso del Proyecto

### Ejecutar Scripts Python
```bash
# Activar entorno virtual primero
source .venv/bin/activate  # Linux/macOS
# o
.venv\Scripts\activate     # Windows

# Ejecutar scripts específicos
python maquina_bolas_data_generator.py
```

### Renderizar Documentos Quarto
```bash
# Renderizar un documento específico
quarto render EDA_maquina_bolas.qmd

# Renderizar todos los documentos .qmd
quarto render

# Previsualizar en tiempo real
quarto preview EDA_maquina_bolas.qmd
```

### Trabajar con pyproject.toml y UV
```bash
# Sincronizar todas las dependencias del proyecto - equivalente a `pip install -r requirements.txt`
uv sync

# Agregar nueva dependencia
uv add nombre-paquete

# Agregar dependencia de desarrollo
uv add --dev nombre-paquete-dev

# Actualizar dependencias
uv lock --upgrade

# Instalar proyecto en modo desarrollo
uv pip install -e .

# Generar requirements.txt si es necesario
uv pip freeze > requirements.txt
```

## 📊 Flujo de Trabajo Típico

1. **Activar el entorno virtual:**
   ```bash
   source .venv/bin/activate  # Linux/macOS
   # o
   .venv\Scripts\activate     # Windows
   ```
2. **Sincronizar dependencias:**
   ```bash
   uv sync
   ```
3. **Generar o actualizar datos:**
   ```bash
   python generacion_data/maquina_bolas_data_generator.py
   ```

## 🔍 Análisis Disponibles

- **EDA_maquina_bolas.qmd** - Análisis exploratorio de datos

## 🤝 Contribución

1. Fork el proyecto
2. Crea tu rama de feature (`git checkout -b feature/NuevaCaracteristica`)
3. Commit tus cambios (`git commit -m 'Agregar nueva característica'`)
4. Push a la rama (`git push origin feature/NuevaCaracteristica`)
5. Abre un Pull Request

## ⚠️ Solución de Problemas

### Error de Quarto no encontrado
```bash
# Verificar instalación
quarto --version

# Reinstalar si es necesario
# Seguir instrucciones de instalación arriba
```

### Problemas con UV
```bash
# Verificar instalación
uv --version

# Reinstalar
pip install --upgrade uv
```

### Entorno virtual no se activa
```bash
# Recrear entorno virtual con UV
rm -rf .venv
uv venv
source .venv/bin/activate  # Linux/macOS
```

## 📄 Licencia

MIT LIcense

## 👨‍💻 Autores

1. Angel Ch
2. Jherson
3. Alan
4. Edson

---

**Nota:** Recuerda siempre activar tu entorno virtual antes de trabajar en el proyecto y mantener tus dependencias actualizadas.