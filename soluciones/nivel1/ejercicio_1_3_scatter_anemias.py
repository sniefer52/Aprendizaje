"""
Ejercicio 1.3 — Gráfico de Dispersión VCM vs Hb
Nivel 1 | Hematología con Claude Code

Genera datos simulados de 50 pacientes con 3 tipos de anemia y visualiza
la distribución morfológica en un scatter plot con regiones diagnósticas.

Tipos simulados:
  • Ferropénica (microcítica hipocrómica)
  • Talasemia minor (microcítica con Hb menos baja)
  • Megaloblástica (macrocítica)

Ejecutar: python ejercicio_1_3_scatter_anemias.py
Requiere: pip install matplotlib numpy pandas
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D

rng = np.random.default_rng(seed=42)


# ── 1. Generar datos simulados ────────────────────────────────────────────────

def generar_datos(n_por_grupo: int = 50) -> pd.DataFrame:
    """Simula hemogramas con variabilidad clínicamente realista."""

    registros = []

    # ── Grupo 1: Ferropenia ───────────────────────────────────────────────────
    # VCM 58-78 fL | Hb 6-10 g/dL | distribución asimétrica hacia valores bajos
    for _ in range(n_por_grupo):
        hb  = rng.normal(8.0, 1.2)
        vcm = rng.normal(68,  6.0)
        hcm = vcm * 0.31 + rng.normal(0, 1.5)   # HCM correlaciona con VCM
        registros.append({
            "diagnostico": "Ferropenia",
            "hb": round(max(5.0, min(11.5, hb)), 1),
            "vcm": round(max(55,  min(82,  vcm)), 1),
            "hcm": round(max(15,  min(28,  hcm)), 1),
        })

    # ── Grupo 2: Talasemia minor ──────────────────────────────────────────────
    # VCM 60-75 fL pero Hb relativamente más conservada (9-12 g/dL)
    # Microcitosis desproporcionada respecto a la anemia (índice de Mentzer <13)
    for _ in range(n_por_grupo):
        hb  = rng.normal(10.5, 1.0)
        vcm = rng.normal(66,   5.0)
        hcm = vcm * 0.32 + rng.normal(0, 1.2)
        registros.append({
            "diagnostico": "Talasemia minor",
            "hb": round(max(8.0, min(13.0, hb)), 1),
            "vcm": round(max(58,  min(78,  vcm)), 1),
            "hcm": round(max(18,  min(28,  hcm)), 1),
        })

    # ── Grupo 3: Megaloblástica ───────────────────────────────────────────────
    # VCM 105-130 fL | Hb variable (6-10 g/dL cuando hay déficit severo)
    for _ in range(n_por_grupo):
        hb  = rng.normal(8.5, 1.5)
        vcm = rng.normal(115, 8.0)
        hcm = vcm * 0.33 + rng.normal(0, 2.0)
        registros.append({
            "diagnostico": "Megaloblástica",
            "hb": round(max(4.5, min(11.5, hb)), 1),
            "vcm": round(max(100, min(135, vcm)), 1),
            "hcm": round(max(28,  min(44,  hcm)), 1),
        })

    df = pd.DataFrame(registros)
    # Calcular índice de Mentzer: VCM / nº eritrocitos ≈ VCM / (Hb/MCH*10)
    # Simplificado: Mentzer = VCM / (Hb / 0.3) — orientativo
    df["mentzer"] = (df["vcm"] / (df["hb"] / 0.30)).round(1)
    return df


# ── 2. Scatter plot principal ─────────────────────────────────────────────────

def plot_scatter_anemias(df: pd.DataFrame) -> None:
    colores = {
        "Ferropenia":       "#E63946",   # rojo
        "Talasemia minor":  "#F4A261",   # naranja
        "Megaloblástica":   "#457B9D",   # azul
    }
    marcadores = {
        "Ferropenia":       "o",
        "Talasemia minor":  "s",
        "Megaloblástica":   "^",
    }

    fig, axes = plt.subplots(1, 2, figsize=(16, 7))
    fig.suptitle("Morfología eritrocitaria en tres tipos de anemia\n"
                 "Datos simulados (n=50 por grupo)",
                 fontsize=14, fontweight='bold', y=1.02)

    # ── Panel izquierdo: VCM vs Hb ────────────────────────────────────────────
    ax1 = axes[0]

    # Zonas diagnósticas de fondo
    ax1.axhspan(0,  80,  alpha=0.07, color="#E63946", label="_micro")
    ax1.axhspan(100, 140, alpha=0.07, color="#457B9D", label="_macro")
    ax1.axhspan(80, 100, alpha=0.04, color="#2A9D8F", label="_normo")

    # Líneas de umbral
    ax1.axhline(y=80,  color='gray', linestyle='--', linewidth=0.8, alpha=0.6)
    ax1.axhline(y=100, color='gray', linestyle='--', linewidth=0.8, alpha=0.6)
    ax1.axvline(x=12.0, color='red', linestyle=':', linewidth=0.9, alpha=0.5,
                label='Umbral Hb (mujer)')
    ax1.axvline(x=13.0, color='darkred', linestyle=':', linewidth=0.9, alpha=0.5,
                label='Umbral Hb (varón)')

    for dx, grupo in df.groupby("diagnostico"):
        ax1.scatter(grupo["hb"], grupo["vcm"],
                    c=colores[dx], marker=marcadores[dx],
                    s=55, alpha=0.75, edgecolors='white', linewidths=0.4,
                    label=dx, zorder=3)

    # Elipses de confianza (centros aproximados)
    centros = {
        "Ferropenia":      (8.0,  68),
        "Talasemia minor": (10.5, 66),
        "Megaloblástica":  (8.5,  115),
    }
    for dx, (cx, cy) in centros.items():
        ax1.annotate(dx, xy=(cx, cy), fontsize=8.5, color=colores[dx],
                     ha='center', va='center',
                     bbox=dict(boxstyle='round,pad=0.3', fc='white',
                               ec=colores[dx], alpha=0.7))

    ax1.set_xlabel("Hemoglobina (g/dL)", fontsize=11)
    ax1.set_ylabel("VCM (fL)", fontsize=11)
    ax1.set_title("VCM vs Hemoglobina", fontsize=12)
    ax1.set_xlim(4, 14)
    ax1.set_ylim(50, 140)
    ax1.legend(loc='upper right', fontsize=9)
    ax1.grid(True, alpha=0.3)

    # Etiquetas de zona
    ax1.text(4.3, 68,  "Microcítica\n(VCM<80)", fontsize=8, color="#E63946",
             alpha=0.7, va='center')
    ax1.text(4.3, 90,  "Normocítica\n(80-100)", fontsize=8, color="#2A9D8F",
             alpha=0.7, va='center')
    ax1.text(4.3, 115, "Macrocítica\n(VCM>100)", fontsize=8, color="#457B9D",
             alpha=0.7, va='center')

    # ── Panel derecho: VCM vs HCM (morfología bidimensional) ─────────────────
    ax2 = axes[1]
    ax2.axvspan(0, 80,   alpha=0.07, color="#E63946")
    ax2.axvspan(100, 140, alpha=0.07, color="#457B9D")
    ax2.axhline(y=27, color='gray', linestyle='--', linewidth=0.8, alpha=0.6)

    for dx, grupo in df.groupby("diagnostico"):
        ax2.scatter(grupo["vcm"], grupo["hcm"],
                    c=colores[dx], marker=marcadores[dx],
                    s=55, alpha=0.75, edgecolors='white', linewidths=0.4,
                    label=dx, zorder=3)

    ax2.set_xlabel("VCM (fL)", fontsize=11)
    ax2.set_ylabel("HCM (pg)", fontsize=11)
    ax2.set_title("VCM vs HCM\n(hipocromía vs normocromía)", fontsize=12)
    ax2.set_xlim(50, 140)
    ax2.set_ylim(12, 46)
    ax2.text(58, 23, "Hipocrómica\n(HCM<27)", fontsize=8, color="#E63946", alpha=0.8)
    ax2.text(58, 32, "Normocrómica\n(HCM≥27)", fontsize=8, color="#2A9D8F", alpha=0.8)
    ax2.legend(loc='upper left', fontsize=9)
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("scatter_anemias.pdf", bbox_inches='tight', dpi=200)
    plt.savefig("scatter_anemias.png", bbox_inches='tight', dpi=150)
    print("  Gráficos guardados: scatter_anemias.pdf / scatter_anemias.png")
    plt.show()


# ── 3. Estadísticos descriptivos ─────────────────────────────────────────────

def resumen_estadistico(df: pd.DataFrame) -> None:
    print("\n  ESTADÍSTICOS POR GRUPO")
    print("  " + "─" * 55)
    resumen = df.groupby("diagnostico")[["hb", "vcm", "hcm"]].agg(
        ["mean", "std", "min", "max"]
    ).round(1)
    print(resumen.to_string())

    print("\n  ÍNDICE DE MENTZER (media ± SD)")
    print("  VCM/RBC — <13 sugiere talasemia, >13 sugiere ferropenia")
    mentzer = df.groupby("diagnostico")["mentzer"].agg(["mean", "std"]).round(1)
    for dx, row in mentzer.iterrows():
        interpretacion = "talasemia" if row["mean"] < 13 else "ferropenia"
        print(f"    {dx:<20}: {row['mean']} ± {row['std']}  ({interpretacion})")


# ── Main ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("\n" + "═" * 60)
    print("  EJERCICIO 1.3 — Scatter VCM vs Hb en 3 Tipos de Anemia")
    print("  Hematología con Claude Code | Nivel 1")
    print("═" * 60)

    df = generar_datos(n_por_grupo=50)
    resumen_estadistico(df)

    print("\n  Generando gráficos...")
    plot_scatter_anemias(df)
