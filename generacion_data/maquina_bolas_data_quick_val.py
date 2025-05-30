import pandas as pd
dataset = pd.read_csv('molinos_mineraperu_dataset.csv')

print(f"Período: {dataset['timestamp'].min()} a {dataset['timestamp'].max()}")
print(f"Molinos: {sorted(dataset['molino_id'].unique())}")
print(f"Frecuencia promedio entre registros:")
print(f"Total días: {(dataset['timestamp'].max() - dataset['timestamp'].min()).days}")

# Ver distribución por molino
print(dataset['molino_id'].value_counts().sort_index())