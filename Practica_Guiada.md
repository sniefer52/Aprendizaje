# Práctica Guiada — Hematología con Claude Code
## Desarrollo Completo de los 9 Ejercicios (3 Niveles)

> Lee este documento después de `Hematologia_ClaudeCode.md`.
> Aquí encontrarás los scripts listos para ejecutar, las instrucciones paso a paso y los criterios de autoevaluación para cada ejercicio.

---

## Estructura de archivos

```
soluciones/
├── nivel1/
│   ├── ejercicio_1_1_clasificador_anemias.py   ← Clasificador morfológico completo
│   ├── ejercicio_1_2_casos_hemograma.py         ← 5 casos interactivos con feedback
│   └── ejercicio_1_3_scatter_anemias.py         ← Visualización diagnóstica
├── nivel2/
│   ├── ejercicio_2_1_ipss_r_smd.py             ← Calculadora IPSS-R para SMD
│   ├── ejercicio_2_2_eln_2022_lma.py           ← Árbol ELN 2022 para LMA
│   └── ejercicio_2_3_caso_lmc.py               ← Caso clínico LMC con respuestas
└── nivel3/
    ├── ejercicio_3_1_vcf_parser.py             ← Parser VCF + informe NGS
    ├── ejercicio_3_2_heatmap_lma.py            ← Heatmap expresión génica
    └── ejercicio_3_3_diseno_estudio.md         ← Protocolo + código R completo
```

---

## Instalación de dependencias

```bash
# Dependencias comunes para todos los ejercicios
pip install pandas matplotlib numpy seaborn scipy

# Para ejercicios nivel 3
pip install biopython

# Para ejercicios de R (nivel 3.3)
# En R/RStudio:
# install.packages(c("survival","survminer","tableone","ggplot2","dplyr"))
```

---

## NIVEL 1 — Básico: Hemograma e Interpretación

### Ejercicio 1.1 — Clasificador de Anemias

**Archivo:** `soluciones/nivel1/ejercicio_1_1_clasificador_anemias.py`

**Qué hace:**
- Clasifica anemias por morfología (microcítica/normocítica/macrocítica) y colorimetría
- Calcula el índice reticulocitario corregido y determina si es regenerativa o arregenerativa
- Devuelve diagnóstico diferencial ordenado por probabilidad clínica
- Genera lista de pruebas recomendadas según el patrón

**Ejecución:**
```bash
python soluciones/nivel1/ejercicio_1_1_clasificador_anemias.py
```

**Qué verás:**
```
────────────────────────────────────────────────────────────
  INFORME DE CLASIFICACIÓN DE ANEMIA
  Paciente: F/28 años  |  Hb: 8.9 g/dL  VCM: 72 fL  HCM: 23 pg
────────────────────────────────────────────────────────────
  Gravedad    : MODERADA
  Morfología  : microcítica hipocrómica
  Mecanismo   : arregenerativa (IR corregido = 0.6)
  ...
  DIAGNÓSTICO DIFERENCIAL:
    1. Ferropénica (causa más frecuente de anemia microcítica)
    2. Anemia de proceso crónico...
  PRUEBAS RECOMENDADAS:
    • Hierro sérico, ferritina, IST...
```

**Ejercicio para ti (antes de ejecutar):**
1. Con lápiz y papel, clasifica este hemograma:
   - Hb 7.4 g/dL, VCM 118 fL, reticulocitos 0.8%, leucocitos 3.100/µL, varón 68 años
   - ¿Cuál es la morfología? ¿El mecanismo? ¿Tu diagnóstico más probable?
2. Ejecuta el script y compara con tu respuesta
3. Modifica un caso en el código para simular el tuyo y vuelve a correr

**Criterios de éxito:**
- [ ] Clasificas correctamente los 5 casos antes de ejecutar ≥3/5
- [ ] Puedes explicar por qué la IR corregida usa un "factor de maduración"
- [ ] Añades un 6º caso propio al script y funciona correctamente

---

### Ejercicio 1.2 — Banco de Casos Interactivo

**Archivo:** `soluciones/nivel1/ejercicio_1_2_casos_hemograma.py`

**Qué hace:**
- Presenta hemogramas anónimos con contexto clínico (modo examen)
- Solicita tu diagnóstico antes de revelar la respuesta
- Explica la clave diagnóstica y la "trampa" de cada caso
- Calcula tu puntuación por sesión

**Ejecución:**
```bash
# 3 casos aleatorios (por defecto)
python soluciones/nivel1/ejercicio_1_2_casos_hemograma.py

# 5 casos
python soluciones/nivel1/ejercicio_1_2_casos_hemograma.py 5
```

**Los 5 casos incluidos:**
| Caso | Diagnóstico | Trampa principal |
|------|-------------|-----------------|
| 1 | Anemia megaloblástica por déficit B12 | Pancitopenia puede simular aplasia o SMD |
| 2 | Ferropenia con trombocitosis reactiva | La trombocitosis asusta → ¡es reactiva! |
| 3 | AHAI con VCM falsamente elevado | Reticulocitos elevan el VCM medio |
| 4 | LAL pediátrica | Sin bastones de Auer (eso sería LMA) |
| 5 | SMD — sospecha anemia refractaria | No confundir con déficit B12 |

**Ejercicio para ti:**
1. Haz 3 sesiones (lunes / miércoles / viernes de la misma semana)
2. Anota tu puntuación en cada sesión
3. ¿Mejoras? ¿Cuáles casos te siguen costando?
4. Para los casos fallados, pide a Claude Code que te genere 2 casos similares para practicar

**Criterios de éxito:**
- [ ] ≥3/5 en la primera sesión
- [ ] ≥4/5 en la tercera sesión
- [ ] Puedes explicar la trampa de cada caso fallado

---

### Ejercicio 1.3 — Scatter Plot VCM vs Hb

**Archivo:** `soluciones/nivel1/ejercicio_1_3_scatter_anemias.py`

**Qué hace:**
- Genera 150 pacientes simulados (50 por subtipo)
- Crea scatter plot VCM vs Hb con regiones diagnósticas de fondo
- Crea segundo panel VCM vs HCM para ver la hipocromía
- Calcula y muestra el índice de Mentzer por grupo

**Ejecución:**
```bash
python soluciones/nivel1/ejercicio_1_3_scatter_anemias.py
```

**Salida esperada:**
```
  ESTADÍSTICOS POR GRUPO
  ...
  Ferropenia       : Hb 8.0±1.2  VCM 68±6  HCM 22±2
  Talasemia minor  : Hb 10.5±1.0 VCM 66±5  HCM 22±2
  Megaloblástica   : Hb 8.5±1.5  VCM 115±8 HCM 38±3

  ÍNDICE DE MENTZER (media ± SD)
  Ferropenia:       15.2 ± 2.1  (ferropenia)
  Talasemia minor:  11.4 ± 1.8  (talasemia)
  Megaloblástica:   48.6 ± 8.2  (ferropenia — no aplica, VCM muy alto)
```

**Ejercicio para ti:**
1. Mira el gráfico: ¿solapan los grupos ferropenia y talasemia minor en VCM vs Hb?
2. ¿En qué panel (VCM/Hb vs VCM/HCM) se separan mejor?
3. Modifica el script para añadir anemia de proceso crónico como 4º grupo:
   - VCM 78-88, Hb 8-10, HCM 26-30, Mentzer >13
4. ¿Qué pasaría si hubiese un mix 50/50 de ferropenia + talasemia minor?

**Criterios de éxito:**
- [ ] Ejecutas el script sin errores
- [ ] Interpretas correctamente los 2 paneles del gráfico
- [ ] Añades el 4º grupo (APC) y el gráfico lo representa correctamente

---

## NIVEL 2 — Intermedio: Neoplasias Hematológicas

### Ejercicio 2.1 — Calculadora IPSS-R para SMD

**Archivo:** `soluciones/nivel2/ejercicio_2_1_ipss_r_smd.py`

**Qué hace:**
- Implementa el sistema de puntuación IPSS-R completo con las 5 variables
- Aplica el ajuste por edad (IPSS-R ajustado por edad)
- Clasifica en 5 categorías de riesgo (Muy bajo / Bajo / Intermedio / Alto / Muy alto)
- Devuelve pronóstico (SG mediana) y recomendaciones terapéuticas

**Ejecución:**
```bash
# Casos de demostración
python soluciones/nivel2/ejercicio_2_1_ipss_r_smd.py

# Modo interactivo (introduce tus propios datos)
python soluciones/nivel2/ejercicio_2_1_ipss_r_smd.py --interactivo
```

**Los 4 casos incluidos:**
| Caso | Riesgo esperado | Recomendación |
|------|----------------|--------------|
| del(5q) aislada | Bajo | Lenalidomida / observación |
| Citogenética intermedia | Intermedio | Azacitidina / evaluar TPH |
| Monosomía 7 | Alto | Azacitidina urgente / aloTPH |
| Cariotipo complejo >3 | Muy alto | aloTPH prioritario |

**Antes de ejecutar, calcula a mano este caso:**
```
Paciente: varón 58 años
Blastos MO: 8%
Citogenética: -7 (monosomía 7)
Hb: 7.5 g/dL
Plaquetas: 45.000/µL
Neutrófilos: 650/µL

¿Cuánto suman los puntos? ¿Qué categoría de riesgo es?
¿Está indicado el aloTPH?
```

**Criterios de éxito:**
- [ ] Calculas el IPSS-R del caso manual correctamente (±0.5 puntos)
- [ ] Sabes qué variables tienen más peso en la puntuación
- [ ] Usas el modo interactivo con 3 pacientes de tu práctica clínica (anonimizados)
- [ ] Puedes explicar por qué se ajusta por edad y en qué sentido cambia el riesgo

---

### Ejercicio 2.2 — Clasificador ELN 2022 para LMA

**Archivo:** `soluciones/nivel2/ejercicio_2_2_eln_2022_lma.py`

**Qué hace:**
- Implementa el árbol de decisión ELN 2022 completo para LMA
- Integra citogenética + molecular para la clasificación de riesgo
- Identifica dianas terapéuticas (FLT3 → midostaurina, IDH → inhibidores)
- Indica si hay indicación de aloTPH en CR1
- Sugiere marcadores de ERM específicos

**Ejecución:**
```bash
python soluciones/nivel2/ejercicio_2_2_eln_2022_lma.py
```

**Los 5 casos incluidos:**
| Caso | Perfil | Riesgo ELN 2022 | Clave |
|------|--------|----------------|-------|
| 1 | t(8;21) sola | Favorable | CBF — consolidación con HDAC |
| 2 | NPM1m + FLT3-ITD ratio bajo | Favorable | Ratio <0.5 importa |
| 3 | FLT3-ITD alto + NPM1wt | Adverso | Sin NPM1, FLT3 es adverso |
| 4 | TP53 + cariotipo complejo | Adverso (muy alto) | aloTPH urgente |
| 5 | t(15;17) | LPA — circuito propio | ATRA urgente |

**El dilema más importante del ELN 2022:**

> NPM1mut + FLT3-ITD: ¿Favorable o Intermedio?

Depende del **ratio FLT3-ITD/WT**:
- Ratio < 0.5: **FAVORABLE** (NPM1 domina el pronóstico)
- Ratio ≥ 0.5: **INTERMEDIO** (FLT3 alto atenúa el beneficio de NPM1)
- Ratio desconocido: **INTERMEDIO** (se aplica el principio de cautela)

**Ejercicio práctico:**
Modifica el Caso 2 para poner `flt3_itd_ratio=0.8` y vuelve a ejecutar.
¿Cambia la categoría de riesgo? ¿Cambia la indicación de TPH?

**Criterios de éxito:**
- [ ] Clasificas correctamente los 5 casos antes de ejecutar ≥4/5
- [ ] Sabes qué anomalías adversas "rompen" una clasificación favorable
- [ ] Entiendes por qué LPA tiene su propio circuito diagnóstico-terapéutico
- [ ] Puedes explicar el impacto del ratio FLT3-ITD en la clasificación

---

### Ejercicio 2.3 — Caso Clínico: LMC

**Archivo:** `soluciones/nivel2/ejercicio_2_3_caso_lmc.py`

**Qué hace:**
- Presenta un caso clínico completo de LMC (datos reales de presentación)
- Formula 6 preguntas progresivas de dificultad creciente
- Revela respuestas detalladas con razonamiento clínico completo
- Incluye la "trampa" diagnóstica de cada pregunta

**Ejecución:**
```bash
# Solo el caso y las preguntas (modo examen)
python soluciones/nivel2/ejercicio_2_3_caso_lmc.py

# Con respuestas completas
python soluciones/nivel2/ejercicio_2_3_caso_lmc.py --respuestas
```

**Las 6 preguntas:**
1. Diagnóstico y razonamiento (¿por qué no es una reacción leucemoide?)
2. Prueba confirmatoria (¿qué técnica y por qué importa el transcrito p210/p190?)
3. Determinación de la fase (criterios OMS: crónica / acelerada / crisis)
4. Tratamiento de primera línea (ITK 1G vs 2G — ¿cuándo elegir cada uno?)
5. Monitorización de respuesta (escala IS, hitos a 3/6/12 meses)
6. Indicaciones actuales de aloTPH en LMC (¿cuándo ya es obligatorio?)

**Autoevaluación recomendada:**
- Responde por escrito antes de ver las respuestas
- Puntúate 1 punto por pregunta
- Si ≤3/6: revisa secciones 14 y 15 del tutorial principal
- Si ≥5/6: prueba a buscar el **score de Sokal** y recalcular para el caso dado

**Criterios de éxito:**
- [ ] ≥4/6 preguntas correctas antes de ver respuestas
- [ ] Conoces los hitos de respuesta molecular y qué hacer si no se alcanzan
- [ ] Sabes cuándo el TPH ya no es opcional en LMC

---

## NIVEL 3 — Avanzado: Bioinformática y Genómica

### Ejercicio 3.1 — Parser VCF para Panel Hematológico

**Archivo:** `soluciones/nivel3/ejercicio_3_1_vcf_parser.py`

**Qué hace:**
- Lee archivos VCF (formato estándar de variantes genómicas)
- Extrae VAF y profundidad de cobertura de los campos FORMAT/SAMPLE
- Anota cada variante contra paneles de genes de LMA, linfoma y mieloma
- Filtra por calidad (VAF mínimo, profundidad mínima, filtro PASS)
- Genera informe clínico estructurado + CSV exportable

**Ejecución:**
```bash
# Con VCF simulado (demostración, sin datos reales)
python soluciones/nivel3/ejercicio_3_1_vcf_parser.py

# Con tu propio VCF real (anonimizado)
python soluciones/nivel3/ejercicio_3_1_vcf_parser.py --vcf mi_paciente.vcf

# Cambiar panel
python soluciones/nivel3/ejercicio_3_1_vcf_parser.py --panel LINFOMA
python soluciones/nivel3/ejercicio_3_1_vcf_parser.py --panel MIELOMA
```

**VCF simulado incluido contiene:**

| Gen | VAF | Relevancia | Diana |
|-----|-----|-----------|-------|
| NPM1 | 48.3% | Muy alta | menin inhibidores en recaída |
| FLT3-ITD | 48.0% | Muy alta | midostaurina |
| DNMT3A R882 | 48.1% | Alta | — |
| IDH2 R140Q | 46.4% | Alta | enasidenib |
| TP53 R273H | 18.2% | Muy alta | adverso |
| ASXL1 fs | 7.1% | Alta | adverso |
| DESCONOCIDO | 2.5% | Desconocida | — (subumbral, filtrado) |

**Ejercicio de análisis:**
1. Ejecuta con el VCF demo y lee el informe
2. ¿Qué categoría de riesgo ELN 2022 asignarías a este perfil?
3. ¿Hay algún conflicto entre marcadores favorables y adversos?
4. TP53 está a VAF 18%: ¿qué significa en términos de clonalidad?
5. Modifica el umbral de VAF de 3% a 5% y compara el informe

**Extender el ejercicio:**
```python
# Pide a Claude Code que añada al parser:
# 1. Detección de FLT3-ITD (inserción en tándem) vs FLT3-TKD (D835)
# 2. Cálculo automático del ratio FLT3-ITD/WT a partir de los reads
# 3. Integración con clasificador ELN 2022 (ejercicio 2.2)
```

**Criterios de éxito:**
- [ ] Ejecutas el parser sin errores con el VCF demo
- [ ] Entiendes la estructura de un VCF (CHROM, POS, REF, ALT, FORMAT, SAMPLE)
- [ ] Modificas el umbral de filtrado y entiendes el impacto clínico
- [ ] Clasificas el perfil del VCF demo con el árbol ELN 2022

---

### Ejercicio 3.2 — Heatmap de Expresión Génica en LMA

**Archivo:** `soluciones/nivel3/ejercicio_3_2_heatmap_lma.py`

**Qué hace:**
- Simula una matriz de expresión de 20 genes × 30 muestras (3 subtipos × 10)
- Calcula estadísticos comparativos y ratio HOX/otros por subtipo
- Identifica los 5 genes más diferenciales entre NPM1m y CBF
- Genera heatmap con clustering jerárquico (con seaborn) o básico (sin seaborn)

**Ejecución:**
```bash
python soluciones/nivel3/ejercicio_3_2_heatmap_lma.py
```

**Genes incluidos y su significado clínico:**

| Gen | Por qué importa en LMA |
|-----|----------------------|
| HOXA9, HOXA10, HOXB3, HOXB4, HOXB7 | Firma HOX: elevada en NPM1m y KMT2A-r; suprimida en CBF |
| MEIS1 | Co-factor de HOX; también elevado en NPM1m |
| FLT3 | Receptor de tirosina quinasa; alto en blastos primitivos |
| DNMT3A, IDH2, TET2 | Metilación del ADN; mutados frecuentemente en LMA |
| TP53, ASXL1, RUNX1 | Genes de riesgo adverso |
| EVI1/MECOM | Elevado en inv(3)/t(3;3) — riesgo muy adverso |
| CD34 | Marcador de progenitor; alto en CBF y LAM primitiva |
| MPO | Mieloperoxidasa; diferenciación mieloide |
| BCL2 | Antiapoptótico; diana de venetoclax |

**Análisis que devuelve el script:**
```
  NPM1m:
    Media HOX/MEIS1          : 9.18
    Media otros genes         : 6.21
    Ratio HOX/otros           : 1.48x
    → Firma HOX activada (típica de NPM1m / KMT2A-r)

  TOP 5 GENES MÁS DIFERENCIALES (NPM1m vs CBF):
    HOXA9      : ΔlogFC = 7.23  (más alto en NPM1m)
    HOXB4      : ΔlogFC = 6.19  (más alto en NPM1m)
    CD34       : ΔlogFC = 4.72  (más alto en CBF)
    ...
```

**Ejercicio de análisis clínico:**
1. ¿Por qué el CD34 es más alto en CBF que en NPM1m? (pista: primitività del blasto)
2. ¿Qué gen del panel se relaciona directamente con venetoclax? ¿En qué subtipo es más alto?
3. EVI1/MECOM es muy alto en el subtipo adverso: ¿con qué anomalía citogenética se asocia?
4. Si un paciente tiene firma HOX alta pero citogenética normal y NPM1 negativo, ¿qué otra anomalía molecular pensarías?

**Criterios de éxito:**
- [ ] El script genera los gráficos sin errores
- [ ] Interpretas el heatmap: ¿qué genes separan mejor NPM1m de CBF?
- [ ] Respondes las 4 preguntas de análisis clínico
- [ ] Modificas el script para añadir el subtipo KMT2A-rearranged y ver su firma HOX

---

### Ejercicio 3.3 — Diseño de Estudio de Cohorte

**Archivo:** `soluciones/nivel3/ejercicio_3_3_diseno_estudio.md`

**Qué contiene:**
- Protocolo completo de un estudio retrospectivo de cohortes
- Pregunta PICO formal con definición precisa de cada componente
- Cálculo razonado del tamaño muestral (con código Python)
- Lista de variables con tipo, fuente y valores posibles
- Plan de análisis estadístico completo en R (Tabla 1, KM, Cox)
- Sesgos identificados y estrategias de control
- 5 preguntas de reflexión con respuestas detalladas (ocultas)

**Cómo usar este ejercicio:**
```bash
# Lee el documento (no es un script ejecutable)
cat soluciones/nivel3/ejercicio_3_3_diseno_estudio.md

# O con un visor Markdown
# En VSCode: Ctrl+Shift+V
```

**Progresión recomendada:**
1. **Día 1:** Lee solo la Parte A (protocolo). Intenta redactar tu propia hipótesis y PICO antes de leer la solución.
2. **Día 2:** Calcula el tamaño muestral a mano con los parámetros dados, luego compara con el código Python.
3. **Día 3:** Ejecuta el código R de la Parte B con los datos simulados.
4. **Día 4:** Responde las 5 preguntas de reflexión por escrito, luego compara con las respuestas ocultas.
5. **Semana 2:** Aplica este protocolo a una pregunta de investigación de tu propio centro.

**Ejercicio extendido:**
Pide a Claude Code:
```
Basándote en el diseño del ejercicio 3.3, genera el mismo análisis
pero para la pregunta: "¿Impacta la citogenética en la respuesta a
ruxolitinib en mielofibrosis?"

Adapta: la variable de exposición, el outcome, las covariables y
el análisis estadístico.
```

**Criterios de éxito:**
- [ ] Redactas el PICO correctamente con definiciones operativas precisas
- [ ] Calculas el tamaño muestral y entiendes cada supuesto
- [ ] Ejecutas el código R completo y obtienes las curvas KM y el forest plot
- [ ] Respondes correctamente las 5 preguntas de reflexión (≥4/5)
- [ ] Identificas al menos 3 sesgos adicionales no listados en el documento

---

## Ruta de aprendizaje por semanas

```
SEMANA 1 (inicio)
├── Lunes    : Ejercicio 1.1 (clasificador) + teoría anemia del tutorial
├── Miércoles: Ejercicio 1.2 (casos, primera sesión)
└── Viernes  : Ejercicio 1.3 (scatter) + reflexión sobre índices morfológicos

SEMANA 2
├── Lunes    : Ejercicio 1.2 (segunda sesión) — ¿mejoró tu puntuación?
├── Miércoles: Ejercicio 2.1 (IPSS-R) + leer sección SMD del tutorial
└── Viernes  : Ejercicio 2.2 (ELN 2022) + comparar con clasificación OMS

SEMANA 3
├── Lunes    : Ejercicio 2.3 (caso LMC, modo examen) — sin respuestas
├── Miércoles: Ejercicio 2.3 (ver respuestas + estudio de lagunas)
└── Viernes  : Proyecto integrador: clasifica 5 perfiles NGS ficticios
               usando 2.2 (ELN) + 3.1 (parser VCF)

SEMANA 4 (avanzado)
├── Lunes    : Ejercicio 3.1 (VCF parser) — explorar la estructura VCF
├── Miércoles: Ejercicio 3.2 (heatmap) + análisis de firmas génicas
└── Viernes  : Ejercicio 3.3 (diseño estudio) — Parte A y B

SEMANA 5 (integración)
└── Proyecto final: diseña y ejecuta un mini-estudio con datos de tu
    centro (anonimizados) usando las herramientas de los niveles 1-3
```

---

## Cómo pedir ayuda a Claude Code eficientemente

### Si un script da error
```
El script ejercicio_2_1_ipss_r_smd.py da este error:
[pega el traceback completo]

¿Cuál es la causa y cómo lo soluciono?
```

### Si quieres extender un ejercicio
```
En el ejercicio 2.2 (ELN 2022), quiero añadir soporte para
la clasificación ICC 2022 además de ELN 2022.
¿Cuáles son las principales diferencias y cómo las implementarías
en el código existente?
```

### Si quieres practicar más casos
```
Genera 3 perfiles moleculares de LMA con características clínicas,
sin decirme el diagnóstico. Yo los clasificaré con el ELN 2022 y
luego me dices si acerté.
```

### Si quieres conectar los ejercicios
```
Tengo un paciente con este perfil VCF [resultado del ejercicio 3.1].
Pásalo por el clasificador ELN 2022 [ejercicio 2.2] y dime:
1. ¿Qué categoría de riesgo es?
2. ¿Está indicado el aloTPH?
3. ¿Qué marcadores usarías para la ERM?
```

---

*Práctica Guiada Completa | Hematología con Claude Code*
*Todos los datos de pacientes en los scripts son simulados — no datos reales.*
