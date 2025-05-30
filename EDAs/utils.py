from pathlib import Path
import pandas as pd

def get_project_root():
    """Obtiene la ruta raíz del proyecto"""
    current = Path(__file__).parent
    while current != current.parent:
        if (current / 'pyproject.toml').exists():
            return current
        current = current.parent
    raise FileNotFoundError("No se encontró la raíz del proyecto")

def load_data(filename):
    """Carga datos desde la carpeta data/"""
    project_root = get_project_root()
    data_path = project_root / 'data' / filename
    return pd.read_csv(data_path)

# Función específica para tus datos
def molinos_data():
    """Carga el dataset principal de molinos"""
    return load_data('molinos_mineraperu_dataset.csv')
