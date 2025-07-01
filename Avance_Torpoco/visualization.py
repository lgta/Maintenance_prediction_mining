"""Plotly‑based visual helpers (no Streamlit dependency)."""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt 
import math     

# -------------------------------------------------------------------------
def plot_histogram(df: pd.DataFrame, column: str, nbins: int = 40):
    fig = px.histogram(df, x=column, nbins=nbins, title=f'Distribution of {column}')
    fig.show()

# -------------------------------------------------------------------------
def plot_corr_heatmap(df: pd.DataFrame):
    corr = df.corr(numeric_only=True)
    fig = px.imshow(corr, text_auto='.2f', aspect='auto',
                    title='Correlation Matrix')
    fig.show()

# -------------------------------------------------------------------------
def plot_time_series(df: pd.DataFrame, time_col: str, y_col: str):
    fig = px.line(df, x=time_col, y=y_col, title=f'{y_col} over {time_col}')
    fig.show()



def plot_binning_grid(df: pd.DataFrame, features: list, target: str,
                      q: int = 10, n_cols: int = 3, figsize: tuple = (14, 4)):
    """Genera una parrilla de gráficas Failure‑rate vs deciles."""
    n = len(features)
    n_rows = math.ceil(n / n_cols)
    fig, axes = plt.subplots(n_rows, n_cols,
                             figsize=(figsize[0], figsize[1] * n_rows),
                             squeeze=False)

    for i, feat in enumerate(features):
        r, c = divmod(i, n_cols)
        ax = axes[r][c]
        tmp = pd.DataFrame({feat: df[feat], target: df[target]}).dropna()
        tmp["bin"] = pd.qcut(tmp[feat], q=q, duplicates="drop")
        grouped = tmp.groupby("bin", observed=True)[target].mean()
        ax.plot(grouped.values, marker="o")
        ax.set_title(feat, fontsize=9)
        ax.set_xlabel("Decil")
        ax.set_ylabel("Failure rate")

    # Oculta ejes vacíos
    for j in range(i + 1, n_rows * n_cols):
        r, c = divmod(j, n_cols)
        axes[r][c].axis("off")

    plt.tight_layout(); plt.show()