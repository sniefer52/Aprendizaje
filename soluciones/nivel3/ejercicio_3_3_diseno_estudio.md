# Ejercicio 3.3 — Diseño de Estudio de Cohorte Retrospectivo
## Hematología con Claude Code | Nivel 3

**Pregunta de investigación:**
Evaluar el impacto de la **negativización de la ERM por NPM1** (tras el primer ciclo de consolidación) en la tasa de recaída de LMA NPM1 mutada.

---

## PARTE A — Protocolo del Estudio

### 1. Pregunta PICO

| Componente | Definición |
|------------|-----------|
| **P** (Población) | Pacientes adultos (≥18 años) con LMA NPM1 mutada en primera remisión completa (RC1) tras inducción con DA o DA+gemtuzumab |
| **I** (Intervención/Exposición) | ERM negativa por NPM1 (BCR-ABL NPM1 <0.01% IS ó <10⁻⁴) en sangre periférica al final del primer ciclo de consolidación (día 28±7) |
| **C** (Comparador) | ERM positiva (NPM1 ≥ 0.01% IS) en el mismo punto temporal |
| **O** (Outcome primario) | Supervivencia libre de recaída (SLR) a 2 años |
| **O** (Outcomes secundarios) | Supervivencia global (SG), tiempo hasta recaída, tasa de RC2, mortalidad relacionada con el tratamiento |

**Hipótesis:** La ERM negativa tras consolidación 1 se asocia con SLR a 2 años significativamente superior (HR < 0.5) respecto a ERM positiva.

---

### 2. Diseño y marco temporal

- **Diseño:** Cohorte retrospectiva unicéntrica (o multicéntrica si hay colaboración)
- **Periodo de inclusión:** Diagnósticos desde 2015 hasta 2023 (mínimo 8 años para tener seguimiento adecuado en los casos más recientes)
- **Tamaño muestral estimado:** Ver sección 4
- **Centro(s):** Servicio de Hematología del centro; si unicéntrico, esperar ~80-120 pacientes con LMA NPM1m en 8 años

---

### 3. Criterios de selección

#### Inclusión
- [ ] LMA de novo o secundaria con mutación NPM1 documentada (secuenciación o PCR)
- [ ] ≥18 años al diagnóstico
- [ ] RC1 documentada (blastos MO <5%, sin células de Auer, recuento periférico recuperado)
- [ ] Al menos un ciclo de consolidación recibido
- [ ] Determinación de ERM por NPM1 disponible al finalizar consolidación 1 (día 28±7)
- [ ] Seguimiento mínimo de 12 meses desde la consolidación (o evento antes)

#### Exclusión
- [ ] LPA (t(15;17))
- [ ] Participación en ensayo clínico que modifique el tratamiento estándar
- [ ] Trasplante alogénico realizado antes del punto de medición de ERM (confundiría el análisis)
- [ ] Datos de ERM no disponibles o muestra inadecuada

---

### 4. Tamaño muestral y potencia estadística

**Supuestos:**

| Parámetro | Valor supuesto | Fuente |
|-----------|---------------|--------|
| SLR 2 años — ERM negativa | 75% | Ivey et al. NEJM 2016 |
| SLR 2 años — ERM positiva | 40% | Ivey et al. NEJM 2016 |
| HR esperado | 0.45 | Basado en datos publicados |
| Ratio ERM-neg/ERM-pos | 60/40 | (60% logran ERM neg) |
| Potencia (1-β) | 80% | Estándar |
| Error tipo I (α) | 0.05 | Bilateral |
| Pérdidas de seguimiento | 10% | Estimado |

**Cálculo:**

Usando la fórmula de Schoenfeld para supervivencia:

```
N eventos necesarios = (z_α/2 + z_β)² / [p₁p₂ × (log HR)²]

Con z_0.025 = 1.96, z_0.20 = 0.84:
N eventos = (1.96 + 0.84)² / [0.6 × 0.4 × (log 0.45)²]
           = 7.84 / [0.24 × 0.607]
           ≈ 54 eventos (recaídas)

N total = N_eventos / tasa_evento_esperada / (1-pérdidas)
Si tasa de recaída global ~45%:
N total ≈ 54 / 0.45 / 0.90 ≈ 133 pacientes
```

**Conclusión:** Se necesitan **~133 pacientes** con LMA NPM1m en RC1 con ERM medida.

**Verificación con Python:**

```python
# Script de cálculo de tamaño muestral (para ejecutar con lifelines o statsmodels)
import numpy as np
from scipy.stats import norm

def n_supervivencia(p1, p2, alpha=0.05, potencia=0.80,
                    ratio_grupos=1.0, perdidas=0.10):
    """
    p1: probabilidad de evento en grupo expuesto (ERM neg)
    p2: probabilidad de evento en grupo control (ERM pos)
    """
    z_alpha = norm.ppf(1 - alpha/2)
    z_beta  = norm.ppf(potencia)
    
    # Tasa media ponderada
    p_media = (p1 + ratio_grupos * p2) / (1 + ratio_grupos)
    
    n1 = ((z_alpha + z_beta)**2 * (p1*(1-p1) + p2*(1-p2)/ratio_grupos)) / (p1-p2)**2
    n1 = int(np.ceil(n1 / (1 - perdidas)))
    n2 = int(np.ceil(n1 * ratio_grupos))
    
    return n1, n2, n1 + n2

# Usando tasas de recaída (inverso de SLR): ERM-neg 25%, ERM-pos 60%
n_erm_neg, n_erm_pos, n_total = n_supervivencia(
    p1=0.25, p2=0.60,   # tasas de RECAÍDA (1 - SLR)
    alpha=0.05, potencia=0.80,
    ratio_grupos=1.5,   # más ERM-neg que ERM-pos
    perdidas=0.10
)
print(f"N ERM-neg: {n_erm_neg}, N ERM-pos: {n_erm_pos}, N total: {n_total}")
```

---

### 5. Variables a recoger

#### Variables principales

| Variable | Tipo | Fuente | Valores |
|---------|------|--------|---------|
| ERM NPM1 post-consol 1 | Binaria/continua | Lab molecular | neg/<0.01% vs pos/≥0.01% |
| Tiempo hasta recaída (días) | Numérica | HIS | Desde RC1 |
| Evento recaída | Binaria | HIS | 0=no, 1=sí |
| SLR (meses) | Numérica | HIS | Tiempo hasta recaída o último seguimiento |
| Exitus | Binaria | HIS | 0=vivo, 1=fallecido |

#### Variables de exposición y covariables

| Variable | Tipo | Categorías |
|---------|------|-----------|
| Edad al diagnóstico | Continua/categorizada | <60 / ≥60 años |
| Sexo | Binaria | M / F |
| FLT3-ITD | Binaria + ratio | neg / pos (ratio <0.5 / ≥0.5) |
| DNMT3A R882 | Binaria | neg / pos |
| IDH1/IDH2 | Binaria | neg / pos |
| Categoría ELN 2022 | Categórica | Favorable / Intermedio / Adverso |
| Inducción | Categórica | DA / DA+GO / DA+otros |
| Blastos al diagnóstico | Continua | % |
| Leucocitos al dx | Continua | /µL |
| Tipo de consolidación | Categórica | HDAC×3 / HDAC×4 / otros |
| aloTPH realizado | Binaria + momento | No / Sí (en CR1 / en CR2) |
| ERM cinética | Continua | log10 NPM1/ABL1 en timepoints seriados |

---

### 6. Plan de análisis estadístico

#### 6.1 Estadística descriptiva

```r
# En R con tableone
library(tableone)
vars <- c("edad", "sexo", "flt3_itd", "dnmt3a", "idh1_2",
          "eln_2022", "blastos_dx", "leucocitos_dx")
tabla1 <- CreateTableOne(vars = vars, strata = "erm_pos1",
                          data = df_lma, test = TRUE)
print(tabla1, smd = TRUE)
```

#### 6.2 Outcome primario: Supervivencia libre de recaída

```r
library(survival)
library(survminer)

# Modelo Kaplan-Meier
km_fit <- survfit(Surv(slr_meses, evento_recaida) ~ erm_pos1, data = df_lma)
ggsurvplot(km_fit,
           data = df_lma,
           pval = TRUE,
           risk.table = TRUE,
           palette = c("#E63946", "#457B9D"),
           legend.labs = c("ERM positiva", "ERM negativa"),
           title = "SLR según estado ERM post-consolidación 1",
           xlab = "Tiempo (meses)",
           ylab = "Probabilidad SLR",
           break.time.by = 6)
```

#### 6.3 Análisis multivariante — Modelo de Cox

```r
# Modelo completo
modelo_cox <- coxph(
  Surv(slr_meses, evento_recaida) ~
    erm_pos1 +        # variable de interés
    edad +
    flt3_itd_ratio +
    dnmt3a_r882 +
    eln_categoria +
    tph_cr1,          # covariable importante (puede explicar parte del efecto)
  data = df_lma
)
summary(modelo_cox)

# Forest plot
ggforest(modelo_cox, data = df_lma,
         main = "HR de recaída — Modelo de Cox multivariante")
```

#### 6.4 Tratamiento del aloTPH como variable tiempo-dependiente

El aloTPH en CR1 es un problema de **confusión por indicación** y de **"time-varying covariate"**:
- Los pacientes ERM-pos tienen más indicación de TPH
- El TPH ocurre en un punto intermedio entre consolidación y seguimiento

```r
# Modelo de Cox con covariable tiempo-dependiente
# Requiere formato largo (un registro por tramo de tiempo)
df_td <- tmerge(df_lma, df_lma, id = id,
                event_recaida = event(slr_meses, evento_recaida),
                tph = tdc(tiempo_tph_meses, tph_realizado))

modelo_td <- coxph(Surv(tstart, tstop, event_recaida) ~
                   erm_pos1 + tph + edad + flt3_itd_ratio,
                   data = df_td)
```

#### 6.5 Análisis de sensibilidad

1. **Restricción a pacientes sin TPH en CR1** — efecto "puro" de la ERM
2. **ERM como variable continua** (log10 copies) en vez de binaria
3. **Diferentes puntos de corte de ERM** (0.1% vs 0.01% vs 1%)
4. **Análisis por subgrupo FLT3-ITD** (test de interacción ERM × FLT3)

---

### 7. Sesgos y limitaciones

| Sesgo | Descripción | Estrategia de control |
|-------|-------------|----------------------|
| Sesgo de selección | Solo pacientes con ERM medida (no es aleatorio) | Comparar características de incluidos vs excluidos |
| Confusión por indicación | Pacientes ERM-pos reciben más TPH | Cox tiempo-dependiente; análisis restringido |
| Información incompleta | Datos moleculares históricos incompletos | Análisis de datos faltantes (imputación múltiple) |
| Centro único | Bajo volumen puede limitar generalización | Colaboración multicéntrica o REBIOP |
| Heterogeneidad de técnicas | Cambio en las técnicas de ERM en 8 años | Estratificar por periodo o técnica |
| Seguimiento diferencial | Pacientes en ensayos tienen mejor seguimiento | Análisis de censura informativa |

---

## PARTE B — Código de Análisis Completo en R

Guarda esto como `analisis_erm_npm1.R` y ejecútalo desde RStudio:

```r
# ══════════════════════════════════════════════════════════════════
# Análisis ERM-NPM1 en LMA — Estudio retrospectivo
# Ejercicio 3.3 | Hematología con Claude Code
# ══════════════════════════════════════════════════════════════════

# ── Instalación de paquetes (ejecutar una vez) ─────────────────────
# install.packages(c("survival", "survminer", "tableone", "ggplot2",
#                    "dplyr", "mice", "cmprsk"))

library(survival)
library(survminer)
library(tableone)
library(ggplot2)
library(dplyr)

# ── 1. Simular dataset (reemplazar con tus datos reales) ───────────
set.seed(42)
n <- 140

df <- data.frame(
  id            = 1:n,
  erm_negativa  = rbinom(n, 1, 0.60),   # 1=ERM neg, 0=ERM pos
  edad          = round(rnorm(n, 55, 14)),
  sexo          = sample(c("M","F"), n, replace=TRUE),
  flt3_itd      = rbinom(n, 1, 0.35),
  dnmt3a_r882   = rbinom(n, 1, 0.30),
  eln_adverso   = rbinom(n, 1, 0.20),
  tph_cr1       = rbinom(n, 1, 0.25)
)

# Simular tiempos de recaída (exponencial) según ERM
df$lambda_recaida <- ifelse(df$erm_negativa == 1, 1/30, 1/12)
df$tiempo_recaida <- rexp(n, rate = df$lambda_recaida)
df$tiempo_seguimiento <- pmin(df$tiempo_recaida, runif(n, 18, 60))
df$evento_recaida <- as.integer(df$tiempo_recaida <= df$tiempo_seguimiento)

# ── 2. Tabla 1 ─────────────────────────────────────────────────────
vars_tabla <- c("edad", "sexo", "flt3_itd", "dnmt3a_r882",
                "eln_adverso", "tph_cr1")
tab1 <- CreateTableOne(vars = vars_tabla,
                        strata = "erm_negativa",
                        data = df, test = TRUE)
print(tab1, smd = TRUE)

# ── 3. Kaplan-Meier ────────────────────────────────────────────────
km_fit <- survfit(
  Surv(tiempo_seguimiento, evento_recaida) ~ erm_negativa,
  data = df
)

p_km <- ggsurvplot(
  km_fit, data = df,
  pval = TRUE, pval.method = TRUE,
  conf.int = TRUE,
  risk.table = TRUE, risk.table.height = 0.25,
  palette = c("#E63946", "#457B9D"),
  legend.labs = c("ERM positiva", "ERM negativa"),
  title = "Supervivencia libre de recaída según ERM post-consolidación 1\nLMA NPM1 mutada",
  xlab = "Tiempo (meses)", ylab = "Probabilidad SLR",
  break.time.by = 6, xlim = c(0, 48),
  surv.median.line = "hv",
  ggtheme = theme_bw(base_size = 12)
)
print(p_km)
ggsave("km_slr_erm.pdf", plot = print(p_km), width = 10, height = 8)

# ── 4. Modelo de Cox multivariante ────────────────────────────────
cox_mv <- coxph(
  Surv(tiempo_seguimiento, evento_recaida) ~
    erm_negativa + edad + flt3_itd + dnmt3a_r882 + eln_adverso + tph_cr1,
  data = df
)
summary(cox_mv)

# Forest plot
p_forest <- ggforest(
  cox_mv, data = df,
  main = "HR de recaída (Cox multivariante)\nLMA NPM1m — ERM post-consolidación 1",
  cpositions = c(0.02, 0.20, 0.35)
)
ggsave("forest_cox_erm.pdf", plot = p_forest, width = 10, height = 7)

# ── 5. SLR a 2 años por grupo ─────────────────────────────────────
summary(km_fit, times = 24)

cat("\n══ Análisis completado ══\n")
cat("Archivos generados: km_slr_erm.pdf, forest_cox_erm.pdf\n")
```

---

## PARTE C — Autoevaluación

Después de diseñar y ejecutar el estudio, responde:

### Preguntas de reflexión

1. **¿Por qué usamos Cox tiempo-dependiente para el TPH en vez de incluirlo como covariable estática?**
   > Pista: piensa en qué pasa si un paciente recibe TPH a los 6 meses — ¿en qué grupo está antes y después del TPH?

2. **Si el HR de ERM negativa es 0.42 (IC95% 0.28-0.62), ¿cómo lo interpretas en términos clínicos?**
   > Pista: HR=1 es sin efecto; HR<1 es protector; ¿de qué es un 58% menor?

3. **Si encuentras que el efecto de la ERM es diferente en pacientes FLT3-ITD+ vs FLT3-ITD-, ¿qué test usarías y cómo lo interpretas?**
   > Pista: test de interacción en el modelo de Cox: `erm_negativa * flt3_itd`

4. **¿Qué cambia en tu interpretación si el 40% de los pacientes ERM+ recibieron aloTPH en CR1 vs solo el 10% de los ERM-neg?**
   > Pista: confusión por indicación — ¿en qué dirección sesgaría tu HR?

5. **¿Puede este estudio retrospectivo cambiar la práctica clínica? ¿Qué diseño sería necesario para una recomendación de nivel 1A?**
   > Pista: diferencia entre evidencia observacional e intervencional.

---

### Respuestas de autoevaluación

<details>
<summary>Ver respuestas (solo después de reflexionar)</summary>

1. **Cox tiempo-dependiente para TPH:** Un paciente que recibe TPH a los 6 meses pasa de "no trasplantado" a "trasplantado" en ese momento. Si lo codificamos como variable estática al inicio, asignamos el efecto del TPH a todo el periodo de seguimiento, incluso antes de recibirlo (sesgo inmortalidad / "immortal time bias"). La covariable tiempo-dependiente soluciona esto: el paciente contribuye tiempo "no-TPH" hasta el día del trasplante y tiempo "TPH" después.

2. **HR 0.42:** La ERM negativa se asocia con un riesgo de recaída un **58% menor** que la ERM positiva (ajustado por las covariables del modelo), con un intervalo de confianza que no incluye el 1 → estadísticamente significativo. En la práctica: los pacientes con ERM negativa tienen mucha mejor evolución libre de recaída.

3. **Test de interacción:** Añadir al modelo `erm_negativa:flt3_itd` y evaluar si el p del término de interacción es significativo (<0.05). Si HR_interacción ≠ 1, el efecto de la ERM es diferente según FLT3. Un subgrupo análisis separado (Kaplan-Meier por FLT3) es orientativo pero tiene baja potencia.

4. **Confusión por indicación:** Si los pacientes ERM+ reciben más TPH (que es curativo), el TPH "salva" parcialmente a ese grupo, diluyendo la diferencia real entre ERM+ y ERM-. Tu HR estaría sesgado hacia el 1 (efecto aparente menor del que realmente tiene la ERM). Análisis restringido a no-TPH + análisis tiempo-dependiente son las soluciones.

5. **Nivel de evidencia:** Un estudio retrospectivo genera evidencia observacional (nivel 2b-3). Para recomendación 1A necesitaríamos un **ensayo clínico aleatorizado** (ECA) donde la decisión de tratamiento se randomizara según el estado de ERM (ej: ERM-pos → aloTPH vs observación; ERM-neg → mantenimiento con inhibidor vs observación). Estudios como HOVON 132 o MRD-guided therapy trials intentan esto.

</details>

---

*Ejercicio 3.3 | Práctica Guiada Completa | Hematología con Claude Code*
