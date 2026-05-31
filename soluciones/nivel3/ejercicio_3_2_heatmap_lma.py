"""
Ejercicio 3.2 — Heatmap de Expresión Génica en Subtipos de LMA
Nivel 3 | Hematología con Claude Code

Genera datos simulados de expresión de genes relevantes en LMA
y visualiza las diferencias entre 3 subtipos moleculares.

Subtipos simulados:
  1. NPM1 mutado (NPM1m) — firma HOX característica
  2. CBF-LMA t(8;21) — baja expresión HOX, alta de CD34
  3. LMA-TP53 / Cariotipo adverso — expresión desregulada

Genes incluidos: HOX genes, FLT3, DNMT3A, TET2, IDH2, TP53, RUNX1, CD34,
                 GATA2, MPO, HOXA9, HOXB4, EVI1/MECOM, BCL2, MCM2

Ejecutar: python ejercicio_3_2_heatmap_lma.py
Requiere: pip install matplotlib numpy pandas seaborn scipy
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import sys

# Intentar importar seaborn (opcional pero mejora el heatmap)
try:
    import seaborn as sns
    TIENE_SEABORN = True
except ImportError:
    TIENE_SEABORN = False
    print("  Nota: seaborn no instalado. Usando matplotlib puro. "
          "Instala con: pip install seaborn")

rng = np.random.default_rng(seed=7)


# ── Definición de los patrones de expresión por subtipo ──────────────────────

# Valores de log2(TPM+1) normalizados: escala 0-12
# Cada gen tiene (media, desv_std) por subtipo
PATRONES_EXPRESION = {
    # Gen:        NPM1m          CBF/t(8;21)    TP53/Adverso
    "HOXA9":   [(10.5, 0.8),   (3.2, 1.0),    (6.1, 1.5)],
    "HOXA10":  [(9.8,  0.9),   (2.8, 0.9),    (5.4, 1.4)],
    "HOXB3":   [(8.9,  1.0),   (2.5, 1.1),    (4.8, 1.6)],
    "HOXB4":   [(9.2,  0.8),   (3.0, 0.8),    (5.0, 1.3)],
    "HOXB7":   [(8.5,  1.1),   (2.2, 1.0),    (4.5, 1.5)],
    "MEIS1":   [(9.0,  0.9),   (2.9, 0.9),    (5.8, 1.4)],
    "FLT3":    [(7.2,  1.2),   (4.5, 1.0),    (5.5, 1.3)],
    "NPM1":    [(10.0, 0.6),   (7.5, 0.8),    (7.2, 0.9)],
    "DNMT3A":  [(6.5,  1.0),   (5.8, 0.8),    (4.2, 1.2)],
    "IDH2":    [(5.8,  1.1),   (4.2, 0.9),    (3.9, 1.0)],
    "TET2":    [(5.2,  0.9),   (5.5, 0.7),    (3.5, 1.1)],
    "RUNX1":   [(4.5,  0.8),   (2.1, 1.2),    (5.8, 1.0)],
    "TP53":    [(4.2,  0.7),   (4.8, 0.6),    (7.5, 0.8)],
    "ASXL1":   [(3.8,  0.9),   (3.5, 0.8),    (6.2, 1.1)],
    "EVI1":    [(5.0,  1.0),   (3.0, 0.9),    (8.5, 1.2)],
    "CD34":    [(3.5,  1.0),   (8.2, 0.9),    (5.5, 1.3)],
    "MPO":     [(4.8,  1.1),   (7.0, 0.9),    (3.8, 1.2)],
    "GATA2":   [(6.0,  0.9),   (4.5, 0.8),    (4.0, 1.0)],
    "BCL2":    [(7.5,  0.8),   (5.2, 0.9),    (8.0, 1.0)],
    "MCM2":    [(6.2,  0.9),   (7.8, 0.8),    (7.5, 1.0)],
}

SUBTIPOS = ["NPM1m", "CBF-t(8;21)", "TP53/Adverso"]
N_MUESTRAS = 10  # por subtipo


# ── Generar matriz de expresión simulada ─────────────────────────────────────

def generar_matriz_expresion() -> pd.DataFrame:
    """Genera una matriz genes × muestras con variabilidad realista."""
    columnas = []
    for i, subtipo in enumerate(SUBTIPOS):
        for j in range(N_MUESTRAS):
            columnas.append(f"{subtipo}_{j+1:02d}")

    datos = {}
    for gen, patrones in PATRONES_EXPRESION.items():
        expresiones = []
        for i, (media, sd) in enumerate(patrones):
            vals = rng.normal(media, sd, N_MUESTRAS)
            vals = np.clip(vals, 0, 12)  # log2(TPM+1) ∈ [0, 12]
            expresiones.extend(vals.round(2))
        datos[gen] = expresiones

    df = pd.DataFrame(datos, index=columnas).T
    return df


# ── Heatmap principal ────────────────────────────────────────────────────────

def plot_heatmap_expresion(df: pd.DataFrame) -> None:
    # Colormap personalizado: azul (baja expresión) → blanco → rojo (alta)
    cmap_custom = LinearSegmentedColormap.from_list(
        "hema_expr",
        [(0.0, "#2166AC"),   # azul oscuro
         (0.3, "#74ADD1"),   # azul claro
         (0.5, "#F7F7F7"),   # blanco
         (0.7, "#F46D43"),   # naranja
         (1.0, "#A50026")],  # rojo oscuro
    )

    fig, axes = plt.subplots(1, 2, figsize=(20, 10),
                              gridspec_kw={'width_ratios': [3, 1]})
    fig.suptitle("Patrones de Expresión Génica en Subtipos de LMA\n"
                 "Datos simulados — escala log₂(TPM+1)",
                 fontsize=14, fontweight='bold')

    # ── Panel izquierdo: heatmap completo ────────────────────────────────────
    ax1 = axes[0]

    if TIENE_SEABORN:
        # Añadir barra de anotación de subtipos
        col_colors = []
        palette = {"NPM1m": "#E63946", "CBF-t(8;21)": "#457B9D", "TP53/Adverso": "#2A9D8F"}
        for col in df.columns:
            subtipo = col.rsplit('_', 1)[0]
            col_colors.append(palette.get(subtipo, "gray"))

        g = sns.clustermap(
            df,
            col_colors=col_colors,
            cmap=cmap_custom,
            vmin=0, vmax=12,
            figsize=(20, 10),
            dendrogram_ratio=(0.1, 0.05),
            col_cluster=False,     # mantener agrupación por subtipo
            row_cluster=True,      # clustering jerárquico de genes
            xticklabels=True,
            yticklabels=True,
            linewidths=0.1,
            linecolor='white',
            cbar_kws={"label": "log₂(TPM+1)"},
        )
        g.fig.suptitle("Heatmap de Expresión Génica — LMA (3 subtipos moleculares)\n"
                       "Clustering jerárquico de genes | Datos simulados",
                       y=1.02, fontsize=13, fontweight='bold')

        # Leyenda de subtipos
        handles = [plt.Rectangle((0, 0), 1, 1, fc=color, ec='white')
                   for color in palette.values()]
        g.ax_heatmap.legend(handles, palette.keys(), loc='upper right',
                            bbox_to_anchor=(1.15, 1.05), title="Subtipo")

        plt.savefig("heatmap_expresion_lma.pdf", bbox_inches='tight', dpi=200)
        plt.savefig("heatmap_expresion_lma.png", bbox_inches='tight', dpi=150)

    else:
        # Heatmap básico sin seaborn
        im = ax1.imshow(df.values, aspect='auto', cmap=cmap_custom,
                        vmin=0, vmax=12, interpolation='nearest')
        ax1.set_yticks(range(len(df.index)))
        ax1.set_yticklabels(df.index, fontsize=9)
        ax1.set_xticks(range(len(df.columns)))
        ax1.set_xticklabels(df.columns, rotation=90, fontsize=7)

        # Líneas divisorias entre subtipos
        ax1.axvline(x=N_MUESTRAS - 0.5, color='white', linewidth=2)
        ax1.axvline(x=2*N_MUESTRAS - 0.5, color='white', linewidth=2)

        plt.colorbar(im, ax=ax1, label="log₂(TPM+1)", shrink=0.8)
        ax1.set_title("Heatmap de Expresión Génica por Subtipo", fontsize=11)

        # ── Panel derecho: media por gen por subtipo ──────────────────────────
        ax2 = axes[1]
        medias = pd.DataFrame({
            subtipo: df.iloc[:, i*N_MUESTRAS:(i+1)*N_MUESTRAS].mean(axis=1)
            for i, subtipo in enumerate(SUBTIPOS)
        })
        im2 = ax2.imshow(medias.values, aspect='auto', cmap=cmap_custom,
                          vmin=0, vmax=12, interpolation='nearest')
        ax2.set_yticks(range(len(medias.index)))
        ax2.set_yticklabels(medias.index, fontsize=9)
        ax2.set_xticks(range(len(SUBTIPOS)))
        ax2.set_xticklabels(SUBTIPOS, rotation=45, ha='right', fontsize=9)
        ax2.set_title("Media por subtipo", fontsize=10)
        plt.colorbar(im2, ax=ax2, shrink=0.8)

        plt.tight_layout()
        plt.savefig("heatmap_expresion_lma.pdf", bbox_inches='tight', dpi=200)
        plt.savefig("heatmap_expresion_lma.png", bbox_inches='tight', dpi=150)
        plt.show()

    print("  Guardado: heatmap_expresion_lma.pdf / .png")


# ── Análisis de firmas génicas ────────────────────────────────────────────────

def analizar_firmas(df: pd.DataFrame) -> None:
    print("\n  ANÁLISIS DE FIRMAS GÉNICAS")
    print("  " + "─" * 55)

    # Media de los HOX genes por subtipo
    hox_genes = [g for g in df.index if "HOX" in g or g == "MEIS1"]
    otros = [g for g in df.index if g not in hox_genes]

    for i, subtipo in enumerate(SUBTIPOS):
        cols = df.iloc[:, i*N_MUESTRAS:(i+1)*N_MUESTRAS]
        hox_media = cols.loc[hox_genes].mean().mean()
        otros_media = cols.loc[otros].mean().mean()
        hox_ratio = hox_media / max(otros_media, 0.01)

        print(f"\n  {subtipo}:")
        print(f"    Media HOX/MEIS1          : {hox_media:.2f}")
        print(f"    Media otros genes         : {otros_media:.2f}")
        print(f"    Ratio HOX/otros           : {hox_ratio:.2f}x")

        if hox_ratio > 1.5:
            print(f"    → Firma HOX activada (típica de NPM1m / KMT2A-r)")
        elif hox_ratio < 0.7:
            print(f"    → HOX suprimidos (típico de CBF-LMA)")
        else:
            print(f"    → Patrón HOX intermedio")

    # Top genes diferenciales entre NPM1m y CBF
    npm1_cols = df.iloc[:, :N_MUESTRAS].mean(axis=1)
    cbf_cols  = df.iloc[:, N_MUESTRAS:2*N_MUESTRAS].mean(axis=1)
    diff = (npm1_cols - cbf_cols).abs().sort_values(ascending=False)

    print(f"\n  TOP 5 GENES MÁS DIFERENCIALES (NPM1m vs CBF):")
    for gen, delta in diff.head(5).items():
        up_en = "NPM1m" if npm1_cols[gen] > cbf_cols[gen] else "CBF"
        print(f"    {gen:<12}: ΔlogFC = {delta:.2f}  (más alto en {up_en})")


# ── Main ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("\n" + "═" * 60)
    print("  EJERCICIO 3.2 — Heatmap Expresión Génica en LMA")
    print("  Hematología con Claude Code | Nivel 3")
    print("═" * 60)

    df = generar_matriz_expresion()
    print(f"\n  Matriz generada: {len(df.index)} genes × {len(df.columns)} muestras")
    print(f"  Subtipos: {SUBTIPOS}")
    print(f"  Muestras por subtipo: {N_MUESTRAS}")

    analizar_firmas(df)

    print("\n  Generando heatmap...")
    plot_heatmap_expresion(df)

    # Exportar matriz a CSV
    df.to_csv("expresion_lma_simulada.csv")
    print("  Matriz exportada: expresion_lma_simulada.csv")
