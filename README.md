# Aprendizaje

Entorno de aprendizaje autoguiado con Claude Code. Dos rutas disponibles:

---

## Rutas de aprendizaje

### Ruta 1 — Programación general: L99
99 problemas clásicos de programación para aprender a pensar algorítmicamente.

**[L99_Tutorial.md](./L99_Tutorial.md)**

### Ruta 2 — Medicina y Hematología
Tutorial completo de todas las capacidades actuales de Claude Code aplicadas
a la hematología clínica, molecular y de laboratorio.

**[Hematologia_ClaudeCode.md](./Hematologia_ClaudeCode.md)**

Cubre: hemograma, coagulopatías, citometría de flujo, NGS, clasificación OMS 2022,
protocolos de quimioterapia, TPH, bioinformática y ejercicios progresivos.

**[Practica_Guiada.md](./Practica_Guiada.md)** — 9 ejercicios ejecutables en 3 niveles:

| Nivel | Ejercicio | Script |
|-------|-----------|--------|
| 1 — Básico | Clasificador de anemias | `soluciones/nivel1/ejercicio_1_1_clasificador_anemias.py` |
| 1 — Básico | 5 casos interactivos de hemograma | `soluciones/nivel1/ejercicio_1_2_casos_hemograma.py` |
| 1 — Básico | Scatter VCM vs Hb (3 tipos anemia) | `soluciones/nivel1/ejercicio_1_3_scatter_anemias.py` |
| 2 — Intermedio | Calculadora IPSS-R para SMD | `soluciones/nivel2/ejercicio_2_1_ipss_r_smd.py` |
| 2 — Intermedio | Árbol de decisión ELN 2022 LMA | `soluciones/nivel2/ejercicio_2_2_eln_2022_lma.py` |
| 2 — Intermedio | Caso clínico LMC con respuestas | `soluciones/nivel2/ejercicio_2_3_caso_lmc.py` |
| 3 — Avanzado | Parser VCF + informe NGS hematológico | `soluciones/nivel3/ejercicio_3_1_vcf_parser.py` |
| 3 — Avanzado | Heatmap expresión génica LMA | `soluciones/nivel3/ejercicio_3_2_heatmap_lma.py` |
| 3 — Avanzado | Diseño estudio + código R completo | `soluciones/nivel3/ejercicio_3_3_diseno_estudio.md` |

---

## Estructura

```
Aprendizaje/
├── L99_Tutorial.md            ← Ruta 1: 99 problemas de programación
├── Hematologia_ClaudeCode.md  ← Ruta 2: Tutorial Claude Code en Hematología
├── Practica_Guiada.md         ← Ruta 2: Práctica guiada paso a paso
├── soluciones/
│   ├── nivel1/                ← 3 scripts Python (básico)
│   ├── nivel2/                ← 3 scripts Python (intermedio)
│   └── nivel3/                ← 2 scripts Python + 1 protocolo R (avanzado)
└── notas/                     ← Apuntes personales
```

## Inicio rápido

```bash
# Entrar al entorno de Claude Code
cd ~/Aprendizaje
claude
```
