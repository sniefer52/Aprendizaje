# Claude Code en Medicina y Hematología
## Tutorial de Autoaprendizaje Paso a Paso

> **Aviso clínico:** Claude Code es una herramienta de asistencia cognitiva. Nunca reemplaza el juicio clínico, la evaluación directa del paciente ni la responsabilidad médica. Todos los ejemplos de este tutorial son educativos.

---

## Índice

### Parte I — Fundamentos
1. [Qué es Claude Code y cómo funciona en medicina](#1-qué-es-claude-code-y-cómo-funciona-en-medicina)
2. [Mapa de capacidades actuales](#2-mapa-de-capacidades-actuales)
3. [Configuración del entorno clínico-técnico](#3-configuración-del-entorno-clínico-técnico)

### Parte II — Capacidades Generales en Medicina
4. [Análisis e interpretación de datos clínicos](#4-análisis-e-interpretación-de-datos-clínicos)
5. [Revisión y síntesis de literatura médica](#5-revisión-y-síntesis-de-literatura-médica)
6. [Documentación clínica asistida](#6-documentación-clínica-asistida)
7. [Educación médica y casos clínicos](#7-educación-médica-y-casos-clínicos)
8. [Investigación y bioestadística](#8-investigación-y-bioestadística)

### Parte III — Hematología: Aplicaciones Específicas
9. [Interpretación del hemograma](#9-interpretación-del-hemograma)
10. [Coagulopatías y hemostasia](#10-coagulopatías-y-hemostasia)
11. [Citopatología: frotis y médula ósea (análisis de imagen)](#11-citopatología-frotis-y-médula-ósea-análisis-de-imagen)
12. [Citometría de flujo](#12-citometría-de-flujo)
13. [Hematología molecular y genómica](#13-hematología-molecular-y-genómica)
14. [Clasificación de neoplasias hematológicas (OMS 2022)](#14-clasificación-de-neoplasias-hematológicas-oms-2022)
15. [Protocolos de quimioterapia y ajuste de dosis](#15-protocolos-de-quimioterapia-y-ajuste-de-dosis)
16. [Trasplante de progenitores hematopoyéticos](#16-trasplante-de-progenitores-hematopoyéticos)
17. [Medicina transfusional](#17-medicina-transfusional)
18. [Hemopatías benignas](#18-hemopatías-benignas)

### Parte IV — Bioinformática Hematológica
19. [Análisis de NGS: variantes somáticas](#19-análisis-de-ngs-variantes-somáticas)
20. [Análisis de RNA-seq en leucemias](#20-análisis-de-rna-seq-en-leucemias)
21. [Automatización de informes de laboratorio](#21-automatización-de-informes-de-laboratorio)

### Parte V — Práctica Guiada
22. [Ejercicios progresivos](#22-ejercicios-progresivos)
23. [Límites éticos y de seguridad](#23-límites-éticos-y-de-seguridad)

---

## PARTE I — FUNDAMENTOS

---

## 1. Qué es Claude Code y cómo funciona en medicina

Claude Code es un agente de IA que opera desde la **terminal de tu ordenador**. A diferencia de un chatbot web, Claude Code puede:

- Leer y escribir archivos locales (historias clínicas anonimizadas, datasets, código)
- Ejecutar código Python, R, bash directamente
- Analizar imágenes (frotis, inmunohistoquímica, citometría)
- Acceder a repositorios de código y documentación
- Mantener contexto de sesiones largas de trabajo

### El modelo mental correcto

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   TÚ                                                        │
│   (médico/investigador)                                     │
│        │                                                    │
│        │ haces preguntas, pasas datos, defines el problema  │
│        ▼                                                    │
│   CLAUDE CODE                                               │
│   (asistente cognitivo)                                     │
│        │                                                    │
│        │ analiza, codifica, sugiere, sintetiza, explica     │
│        ▼                                                    │
│   RESULTADO                                                 │
│   (código, informe, análisis, respuesta clínica)            │
│        │                                                    │
│        │ TÚ validas con criterio clínico                    │
│        ▼                                                    │
│   DECISIÓN FINAL (siempre tuya)                             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Tres modos de uso en medicina

| Modo | Qué haces | Ejemplo hematológico |
|------|-----------|----------------------|
| **Consulta** | Preguntas en lenguaje natural | "Explícame la fisiopatología del síndrome de activación macrofágica" |
| **Análisis** | Pasas datos, pides interpretación | Subes un CSV de hemogramas seriados, pides tendencias |
| **Código** | Pides scripts para automatizar | "Escribe un script que clasifique blastos según criterios FAB" |

---

## 2. Mapa de capacidades actuales

### Capacidades confirmadas en 2025-2026

```
CLAUDE CODE EN MEDICINA
│
├── CONOCIMIENTO CLÍNICO
│   ├── Fisiología y fisiopatología (base amplia)
│   ├── Farmacología y farmacocinética
│   ├── Semiología y diagnóstico diferencial
│   ├── Clasificaciones internacionales (OMS, FAB, REAL, Ann Arbor...)
│   ├── Guías clínicas (NCCN, ELN, ESMO, ASH hasta fecha de corte)
│   └── Literatura médica (PubMed hasta agosto 2025)
│
├── ANÁLISIS DE DATOS
│   ├── Tablas y CSV de laboratorio
│   ├── Datos de citometría de flujo (FCS exportado a CSV/texto)
│   ├── Variantes genómicas (VCF, anotaciones)
│   ├── Datos de expresión génica
│   └── Series temporales de parámetros analíticos
│
├── VISIÓN (análisis de imágenes)
│   ├── Frotis de sangre periférica
│   ├── Aspirados y biopsias de médula ósea
│   ├── Inmunohistoquímica
│   ├── Electroforesis de proteínas
│   └── Gráficas de citometría (dot plots, histogramas)
│
├── GENERACIÓN DE CÓDIGO
│   ├── Python (pandas, scikit-learn, matplotlib, biopython)
│   ├── R (ggplot2, limma, DESeq2, survival)
│   ├── Bash (automatización de pipelines)
│   └── SQL (consultas a bases de datos clínicas)
│
├── DOCUMENTACIÓN
│   ├── Informes de laboratorio
│   ├── Resúmenes de alta
│   ├── Protocolos clínicos
│   └── Materiales educativos
│
└── INVESTIGACIÓN
    ├── Diseño de estudios
    ├── Análisis estadístico
    ├── Revisiones sistemáticas
    └── Redacción científica
```

### Limitaciones importantes

| Limitación | Implicación práctica |
|------------|---------------------|
| Corte de conocimiento: agosto 2025 | No conoce ensayos clínicos publicados después |
| No accede a internet en tiempo real | No consulta PubMed en vivo; usar WebSearch si está disponible |
| No tiene acceso a HIS/LIS | No lee historias clínicas directamente; tú se las pegas |
| Puede alucinar datos numéricos | Verifica siempre valores de referencia y dosis |
| No reemplaza imagen diagnóstica certificada | Sus interpretaciones de imagen son orientativas |

---

## 3. Configuración del entorno clínico-técnico

### Instalación y setup básico

```bash
# Verificar que Claude Code está instalado
claude --version

# Iniciar sesión en el directorio de trabajo
cd ~/Aprendizaje
claude
```

### Estructura de carpetas recomendada para hematología

```bash
mkdir -p medicina/hematologia/{datos,imagenes,scripts,informes,literatura}
mkdir -p medicina/hematologia/datos/{hemogramas,coagulacion,citometria,ngs}
```

```
medicina/hematologia/
├── datos/
│   ├── hemogramas/      ← CSV con series de hemogramas
│   ├── coagulacion/     ← Datos de coagulación
│   ├── citometria/      ← Exports de citómetro
│   └── ngs/             ← VCF, anotaciones de variantes
├── imagenes/            ← Fotos de frotis, biopsias, electroforesis
├── scripts/             ← Código Python/R generado o revisado
├── informes/            ← Informes generados
└── literatura/          ← PDFs de guías y artículos clave
```

### Anonimización — regla fundamental

Antes de pasar cualquier dato a Claude Code, anonimiza:

```python
# Script básico de anonimización (pide a Claude Code que lo mejore)
import pandas as pd
import hashlib

df = pd.read_csv("hemogramas_pacientes.csv")

# Reemplazar NHC por hash irreversible
df['NHC'] = df['NHC'].apply(lambda x: hashlib.sha256(str(x).encode()).hexdigest()[:8])

# Eliminar columnas de identificación directa
df = df.drop(columns=['nombre', 'apellidos', 'fecha_nacimiento', 'DNI'], errors='ignore')

df.to_csv("hemogramas_anonimizados.csv", index=False)
```

---

## PARTE II — CAPACIDADES GENERALES EN MEDICINA

---

## 4. Análisis e interpretación de datos clínicos

### Ejemplo 1: Análisis de hemograma seriado

Supón que tienes este CSV de un paciente con sospecha de aplasia:

```csv
fecha,hb,leucocitos,neutrofilos,plaquetas,reticulocitos
2025-01-10,11.2,4200,2100,180000,52000
2025-02-15,9.8,3100,1400,120000,28000
2025-03-20,8.1,2200,800,65000,12000
2025-04-10,7.4,1800,620,42000,8000
```

**Prompt efectivo:**

```
Analiza esta serie temporal de hemograma (CSV adjunto o pegado).
El paciente es varón de 34 años sin antecedentes relevantes.

Por favor:
1. Identifica la tendencia de cada serie
2. Señala qué umbrales clínicos se han cruzado y cuándo
3. Calcula la velocidad de descenso de cada línea
4. Propón el diagnóstico diferencial más probable
5. Indica qué pruebas adicionales priorizarías y por qué
```

**Lo que Claude Code hace:**
- Detecta pancitopenia progresiva
- Calcula velocidad de caída (ej: Hb -0.97 g/dL/mes)
- Clasifica la gravedad según criterios de Camitta (aplasia grave: neutrófilos <500, plaquetas <20.000, reticulocitos <20.000)
- Genera diagnóstico diferencial ordenado por probabilidad
- Sugiere biopsia de médula ósea, prueba de Coombs, PNH, B12/folato, etc.

### Ejemplo 2: Generar código de análisis automático

```
Escríbeme un script Python que:
1. Lea un CSV con columnas: fecha, hb, leucocitos, neutrofilos, plaquetas, reticulocitos
2. Detecte automáticamente si hay citopenias según criterios OMS
3. Clasifique la gravedad de aplasia según Camitta si procede
4. Genere un gráfico de tendencias con líneas de umbral en rojo
5. Exporte un informe en texto con el resumen clínico

Usa pandas y matplotlib. Comenta el código para que lo pueda entender y modificar.
```

---

## 5. Revisión y síntesis de literatura médica

### Preguntas clínicas precisas (formato PICO)

```
Usando el formato PICO, necesito síntesis de evidencia sobre:

P: Pacientes con LMA de novo en mayores de 70 años
I: Venetoclax + azacitidina
C: Azacitidina en monoterapia
O: SG a 12 meses, tasa de RC, toxicidad hematológica grado ≥3

Resume los estudios clave que conoces hasta tu fecha de corte (agosto 2025),
indicando nivel de evidencia y limitaciones de cada uno.
```

### Comparación rápida de guías

```
Compara las recomendaciones actuales de ELN 2022, NCCN 2024 y ESMO
para el tratamiento de LMA con mutación FLT3-ITD en primera línea:
- ¿En qué coinciden?
- ¿En qué difieren?
- ¿Qué recomienda cada guía sobre el trasplante en primera remisión?
Formato: tabla comparativa
```

### Explicación de artículos difíciles

```
Explícame los métodos estadísticos de este abstract de ensayo clínico.
En concreto: ¿qué es un análisis por intención de tratar modificado?
¿Por qué se usa Fine-Gray en vez de Kaplan-Meier aquí?
¿Qué significa HR 0.52 (IC95% 0.38-0.71)?

[pega el abstract]
```

---

## 6. Documentación clínica asistida

### Informe de interconsulta

```
Genera un informe de interconsulta de Hematología basado en estos datos:

MOTIVO: Pancitopenia en paciente ingresado en Medicina Interna
DATOS: [pega los datos relevantes]

El informe debe incluir:
- Resumen de los hallazgos analíticos
- Diagnóstico diferencial razonado
- Plan de estudio propuesto con orden de prioridad
- Medidas urgentes si procede
Tono: técnico, conciso, sin abreviaturas no estándar
```

### Hoja de información al paciente

```
El paciente acaba de ser diagnosticado de policitemia vera JAK2+.
Tiene 58 años, nivel educativo medio, está muy ansioso.

Escribe una hoja informativa que explique:
1. Qué es la policitemia vera en lenguaje accesible
2. Por qué se produce y qué significa el JAK2
3. En qué consiste el tratamiento con flebotomías e hidroxiurea
4. Qué síntomas debe vigilar y cuándo consultar urgente
5. Qué actividades puede hacer con normalidad

Máximo 500 palabras. Sin jerga médica. Empático y esperanzador pero honesto.
```

---

## 7. Educación médica y casos clínicos

### Generación de casos para docencia

```
Genera un caso clínico educativo nivel R2 de Hematología con las siguientes características:
- Diagnóstico final: linfoma de Hodgkin clásico, esclerosis nodular
- Presentación: joven de 22 años con síntomas B
- Nivel de dificultad: incluye un diagnóstico diferencial no obvio
- Estructura: presentación → preguntas de razonamiento → respuestas comentadas
- Incluye los hallazgos típicos de TC-PET y biopsia
- Añade la estadificación de Ann Arbor y el IPS
```

### Preguntas tipo MIR / USMLE

```
Genera 5 preguntas tipo test de nivel MIR sobre:
- Tema: Síndrome mielodisplásico
- Dificultad: alta (preguntas de segundo orden, no memorísticas)
- Incluye explicación razonada de por qué cada opción es correcta o incorrecta
- Cubre: criterios diagnósticos IPSS-R, tratamiento según riesgo, indicaciones de TPH
```

### Simulación de guardia

```
Actúa como un paciente en Urgencias de Hematología.
Tienes 67 años, LMC en tratamiento con imatinib desde hace 3 años.
Vienes por fiebre de 38.8°C de 24h de evolución.
Responde solo con los síntomas y datos que yo te pregunte.
Cuando yo llegue a un diagnóstico o plan, dame el feedback de si es correcto.
¡Empieza! (yo haré la anamnesis)
```

---

## 8. Investigación y bioestadística

### Diseño de estudio

```
Quiero hacer un estudio retrospectivo sobre:
Objetivo: Factores predictivos de respuesta a ruxolitinib en mielofibrosis
Datos disponibles: 120 pacientes de mi centro, 2015-2024

Ayúdame a:
1. Definir la pregunta de investigación en formato PICO
2. Identificar los sesgos potenciales y cómo controlarlos
3. Proponer las variables a recoger (exposure, outcome, confounders)
4. Calcular el tamaño muestral necesario para detectar HR 0.6 con poder 80%
5. Sugerir el análisis estadístico apropiado
```

### Análisis de supervivencia en R

```
Tengo un dataset de 120 pacientes con mielofibrosis (archivo: mielofibrosis.csv)
con columnas: id, edad, sexo, dipss_plus, mutacion_jak2, mutacion_calr,
tiempo_seguimiento_meses, evento_muerte (0/1), respuesta_ruxolitinib (0/1)

Escríbeme en R:
1. Curvas de Kaplan-Meier por categoría DIPSS-Plus con log-rank test
2. Modelo de Cox multivariante ajustado por edad, sexo y mutación
3. Forest plot de los HRs con IC95%
4. Gráficos con ggplot2, paleta daltonismo-friendly
5. Tabla de características basales (Tabla 1) con p-values
```

---

## PARTE III — HEMATOLOGÍA: APLICACIONES ESPECÍFICAS

---

## 9. Interpretación del hemograma

### Interpretación sistemática completa

```
Interpreta este hemograma de forma exhaustiva y sistemática:

Serie roja:
- Hb: 7.8 g/dL  VCM: 112 fL  HCM: 38 pg  CHCM: 33 g/dL
- Reticulocitos: 1.2%  Índice reticulocitario: 0.6

Serie blanca:
- Leucocitos: 3.200/µL
- Fórmula: N 45%, L 42%, M 8%, E 3%, B 2%
- Neutrófilos abs: 1.440/µL  Linfocitos abs: 1.344/µL

Plaquetas: 98.000/µL  VPM: 11.2 fL

Contexto: mujer 62 años, astenia 3 meses, glositis, parestesias MMII

Responde:
1. Caracteriza cada línea (morfología, aritmética)
2. Sintetiza el patrón global
3. Diagnóstico diferencial razonado y ordenado por probabilidad
4. Pruebas diagnósticas inmediatas y de segundo nivel
5. Criterios de urgencia o ingreso
```

### Script de clasificación automática

```python
# Script que Claude Code puede generar y ejecutar
# Clasificador de anemias según índices eritrocitarios

def clasificar_anemia(hb, vcm, hcm, reticulocitos, sexo='M'):
    """
    Clasifica anemias por morfología y mecanismo.
    Retorna dict con clasificación y diagnóstico diferencial.
    """
    referencia_hb = 13.0 if sexo == 'M' else 12.0
    anemia = hb < referencia_hb

    if not anemia:
        return {"anemia": False}

    # Clasificación morfológica
    if vcm < 80:
        morfologia = "microcítica"
        if hcm < 27:
            morfologia += " hipocrómica"
        dd = ["Ferropénica", "Talasemia", "Anemia de proceso crónico",
              "Sideroblástica", "Intoxicación por plomo"]
    elif vcm > 100:
        morfologia = "macrocítica"
        dd = ["Déficit B12", "Déficit folato", "Hipotiroidismo",
              "Hepatopatía", "Síndrome mielodisplásico", "Reticulocitosis"]
    else:
        morfologia = "normocítica"
        dd = ["Anemia de proceso crónico", "Aplasia", "Hemolítica",
              "Insuficiencia renal", "Infiltración médula ósea"]

    # Clasificación por mecanismo (índice reticulocitario)
    # IR = (reticulocitos% × hb/hb_normal) / 2 (si hay eritropoyesis aumentada)
    ir = (reticulocitos * (hb / referencia_hb)) / 2
    mecanismo = "regenerativa" if ir > 2.0 else "arregenerativa"

    gravedad = "leve" if hb >= 10 else ("moderada" if hb >= 8 else "grave")

    return {
        "anemia": True,
        "gravedad": gravedad,
        "morfologia": morfologia,
        "mecanismo": mecanismo,
        "indice_reticulocitario": round(ir, 2),
        "diagnostico_diferencial": dd
    }

# Ejemplo de uso
resultado = clasificar_anemia(hb=7.8, vcm=112, hcm=38, reticulocitos=1.2, sexo='F')
for k, v in resultado.items():
    print(f"{k}: {v}")
```

---

## 10. Coagulopatías y hemostasia

### Interpretación del estudio de coagulación

```
Interpreta este estudio de hemostasia:

Hemostasia primaria:
- Plaquetas: 220.000/µL (normal)
- Tiempo de hemorragia (Ivy): 12 min (VR <8 min) → ALARGADO
- PFA-100 Col/ADP: 120 seg (VR <70) → ALARGADO
- PFA-100 Col/EPI: 195 seg (VR <165) → ALARGADO

Coagulación (hemostasia secundaria):
- TP/INR: 1.1 (normal)
- APTT: 78 seg (VR <38 seg) → ALARGADO — ratio 2.1
- TT: normal
- Fibrinógeno: 320 mg/dL (normal)

Mezcla con plasma normal (APTT):
- Inmediata: 38 seg → CORRIGE
- A los 120 min: 55 seg → CORRIGE PARCIALMENTE

Contexto: niño 8 años, sangrados mucosos recurrentes, hemartrosis espontáneas

Respuesta esperada:
1. Patrón de la alteración (hemostasia primaria/secundaria/mixta)
2. Corrección en mezcla: ¿déficit o inhibidor?
3. Diagnóstico más probable y diagnóstico diferencial
4. Algoritmo diagnóstico siguiente
5. Tratamiento urgente si hay sangrado activo
```

### Calculadora de CID

```
Calcula el score de CID de la ISTH con estos datos y orienta el tratamiento:

Recuento plaquetas: 45.000/µL
TP: INR 2.2
Fibrinógeno: 80 mg/dL
Dímero-D: >10 µg/mL FEU (>20 × límite superior normalidad)

Contexto: sepsis por gram-negativo en UCI, sangrado en sitios de punción
```

---

## 11. Citopatología: Frotis y Médula Ósea (análisis de imagen)

Esta es una de las capacidades más potentes: puedes pasar imágenes a Claude Code y pedir análisis morfológico.

### Cómo pasar imágenes a Claude Code

En la terminal de Claude Code, puedes referenciar imágenes directamente:

```
Analiza la imagen del frotis de sangre periférica que está en:
/medicina/hematologia/imagenes/frotis_caso01.jpg

Por favor:
1. Describe la morfología de los hematíes (tamaño, forma, coloración, inclusiones)
2. Describe los leucocitos visibles
3. Identifica cualquier célula anómala
4. Sugiere el diagnóstico más probable
5. Indica qué tinción adicional solicitarías
```

### Tipos de imágenes que Claude Code puede analizar

**Frotis de sangre periférica:**
- Morfología eritrocitaria: esferocitos, drepanocitosy, esquistocitos, acantocitos, células diana, punteado basófilo, cuerpos de Howell-Jolly
- Morfología leucocitaria: hipersegmentación, Pelger-Huët, granulaciones tóxicas, vacuolización
- Blastos: morfología, granulaciones, bastones de Auer
- Células linfoides anómalas: linfocitos vellosos, células de Sézary, células de Reed-Sternberg

**Aspirado de médula ósea:**
- Celularidad global
- Serie eritroide: megaloblastosis, diseritropoyesis
- Serie mieloide: maduración, displasia
- Blastos: porcentaje, morfología
- Serie megacariocítica: micromegacariocitos, hipogranulación

**Biopsia de médula ósea:**
- Celularidad
- Fibrosis (gradación MF-0 a MF-3)
- Infiltración neoplásica

### Prompt para análisis sistemático de frotis

```
Soy residente de Hematología. Tengo una imagen del frotis de un paciente
con anemia hemolítica microangiopática sospechada.

Analiza la imagen con el mismo sistema que usaría un hematólogo experto:
1. ¿Qué porcentaje aproximado de cada morfología eritrocitaria ves?
2. ¿Cuántos esquistocitos por campo de 100x (si los hay)?
3. ¿El patrón es compatible con MAT? ¿Con qué entidad concretamente (PTT, SHU, CID)?
4. ¿Qué otros hallazgos relevantes observas?

Imagen: [ruta/a/imagen.jpg]
```

---

## 12. Citometría de Flujo

### Interpretación de inmunofenotipo

```
Interpreta este inmunofenotipo de citometría de flujo:

Muestra: Sangre periférica. Linfocitosis de 22.000/µL.
Población anómala: 78% de los linfocitos

Marcadores positivos: CD19+, CD5+, CD23+, CD200+, CD43+, sIg débil
Marcadores negativos: CD10-, FMC7-, CD79b débil/neg, ciclina D1-

Índice de Matutes: calcúlalo con estos datos

Contexto: varón 72 años, hallazgo casual en analítica rutinaria

Responde:
1. Calcula el score de Matutes
2. Diagnóstico más probable
3. Diagnóstico diferencial con el fenotipo (especialmente LLC vs otras)
4. ¿Qué marcadores adicionales pedirías? ¿Por qué?
5. ¿Cuándo está indicado el estudio citogenético/FISH/mutación IGHV?
```

### Análisis de dot plots con imagen

```
Adjunto los dot plots de citometría de flujo de un aspirado medular.
El paciente tiene una pancitopenia de 3 meses de evolución.

Por favor analiza:
1. El dot plot FSC/SSC: ¿hay población anómala de localización inusual?
2. Los dot plots de blastos: ¿expresan CD34, CD117, CD33?
3. ¿El patrón inmunofenotípico sugiere LMA, SMD o aplasia?
4. ¿Qué score de aberración fenotípica inferirías?

Imagen: [ruta/a/dotplot.png]
```

### Generación de informe de citometría

```
Con estos datos de citometría, genera un informe estructurado siguiendo
el formato recomendado por la EuroFlow:

[pega los datos de positividad/negatividad de cada marcador]

El informe debe incluir:
- Descripción técnica (marcadores usados)
- Descripción de la población anómala
- Diagnóstico fenotípico
- Diagnóstico diferencial
- Correlación clínico-biológica recomendada
```

---

## 13. Hematología Molecular y Genómica

### Interpretación de panel NGS en leucemia

```
Interpreta este panel de NGS somático en una LMA de novo:

Muestra: médula ósea al diagnóstico, 72% blastos

Variantes detectadas:
- NPM1: c.863_864insCATG (p.W288Cfs*12) — VAF 48.3%
- FLT3-ITD: inserción de 39 pb en exón 14 — ratio 0.8
- DNMT3A: p.R882H — VAF 46.1%
- IDH2: p.R140Q — VAF 47.8%

Variantes no detectadas: TP53, RUNX1, ASXL1, CEBPa, RAS, KIT

Citogenética: 46,XX (cariotipo normal)

Responde:
1. Clasifica según ELN 2022 (¿qué categoría de riesgo?)
2. ¿Hay marcadores que cambien el tratamiento estándar? ¿Cuáles y cómo?
3. ¿Qué dianas terapéuticas identificas?
4. ¿Está indicado midostaurina? ¿Enasidenib? ¿Venetoclax?
5. ¿En qué cambia la indicación de TPH en CR1 con este perfil molecular?
6. ¿Qué variantes usarías para monitorización de ERM?
```

### Interpretación de FISH en mieloma múltiple

```
Paciente con mieloma múltiple en diagnóstico. FISH en células plasmáticas:

Positivo:
- t(4;14)(p16;q32): FGFR3/MMSET — presente en 85% de células
- del(17p): TP53 — presente en 12% de células

Negativo:
- t(11;14): negativo
- t(14;16): negativo
- Amplificación 1q21: negativa
- del(13q): negativa

ISS: estadio III  R-ISS: estadio II

Responde:
1. Perfil citogenético de riesgo según Mayo Stratification (mSMART 3.0)
2. ¿Alto riesgo, riesgo estándar o riesgo intermedio?
3. ¿Cómo modifica la del(17p) la estrategia terapéutica?
4. ¿Está indicado el mantenimiento con bortezomib?
5. ¿Cuándo considerar alotrasplante en este perfil?
```

### Script para anotación de variantes somáticas

```
Escríbeme un script Python que:
1. Lea un archivo VCF con variantes somáticas de un panel de leucemia
2. Consulte localmente una tabla de anotaciones (CSV con gen, variante, patogenicidad, evidencia)
3. Clasifique cada variante como: patogénica, probablemente patogénica, VUS, benigna
4. Identifique variantes en genes del panel ELN/NCCN relevantes
5. Genere un informe en PDF con tabla resumen y alertas clínicas

Usa: pandas, reportlab o fpdf para el PDF
```

---

## 14. Clasificación de Neoplasias Hematológicas (OMS 2022)

### Clasificación interactiva

```
Tengo un paciente con estas características. Aplica la clasificación OMS 2022:

Datos:
- Paciente: varón 55 años
- Blastos en MO: 22%
- Citogenética: t(8;21)(q22;q22.1); RUNX1::RUNX1T1
- Morfología: blastos con granulaciones azurófilas y bastones de Auer
- Inmunofenotipo: CD34+, CD117+, CD33+, CD13+, MPO+, CD19+(aberrante)

Responde:
1. ¿Cuál es el diagnóstico exacto según OMS 2022?
2. ¿Por qué la t(8;21) modifica el umbral del 20% de blastos?
3. ¿Cómo se llamaba en la clasificación FAB anterior?
4. ¿Cuál es la implicación pronóstica de la t(8;21) en LMA?
5. ¿Qué biomarcador de ERM es específico de esta entidad?
```

### Tabla comparativa OMS 2022 vs clasificación ICC 2022

```
Genera una tabla comparativa detallada de las diferencias entre
OMS 2022 (5ª edición) e ICC 2022 para las leucemias agudas mieloides.

Enfócate especialmente en:
- Cambios en el umbral de blastos
- Nuevas entidades definidas genéticamente
- Cambios en LMA con cambios relacionados con mielodisplasia
- Cambios en LMA post-citotóxica
- Diferencias en el manejo de CHIP/CCUS
```

---

## 15. Protocolos de Quimioterapia y Ajuste de Dosis

> **ADVERTENCIA:** Claude Code puede proporcionar información sobre protocolos como referencia educativa. La prescripción real debe validarse siempre con el farmacéutico de oncología y el software de prescripción electrónica del centro.

### Consulta de protocolo

```
Descríbeme el protocolo de inducción DA+GO (daunorrubicina + citarabina +
gemtuzumab ozogamicina) para LMA CD33+ según el ensayo MyloFrance-3:

1. Dosis, vías y esquema de administración de cada fármaco
2. Criterios de inclusión y exclusión
3. Principales toxicidades esperadas y su manejo
4. Criterios de respuesta (RC, RCi, MLFS)
5. Cuándo se considera el segundo ciclo de inducción
```

### Ajuste de dosis por toxicidad

```
Paciente en ciclo 3 de R-CHOP por linfoma difuso de célula B grande.
Desarrolló neutropenia febril grado 4 en el ciclo anterior.

Datos relevantes:
- Nadir de neutrófilos: 80/µL en día +12
- Sin infección documentada, afebril tras 5 días de antibiótico IV
- Actualmente: neutrófilos 3.200/µL, apto para tratamiento

Ayúdame a razonar:
1. ¿Está indicada la reducción de dosis? ¿Según qué criterios?
2. ¿Cuándo es obligatoria la profilaxis primaria con G-CSF (ASCO/ESMO)?
3. ¿Hay evidencia de que la reducción de dosis en R-CHOP compromete la SG?
4. ¿Cuál sería tu recomendación y por qué?
```

---

## 16. Trasplante de Progenitores Hematopoyéticos

### Evaluación de candidatura a TPH

```
Evalúa la candidatura a trasplante alogénico de este paciente:

Diagnóstico: LMA con mutación TP53, compleja (≥3 anomalías citogenéticas)
Situación: 2ª RC tras reinducción con decitabina + venetoclax
Blastos MO: 3% (día +30 reinducción)
ERM por NPM1: negativa

Paciente: varón 61 años, ECOG 1, HCTCI score 2
Comorbilidades: HTA controlada, DM2 bien regulada (HbA1c 6.8%)
Función orgánica: DLCO 74%, FEV1 89%, LVEF 58%, creatinina 0.9 mg/dL

Donante disponible: hermano HLA-idéntico 10/10 (58 años, sano)

Por favor:
1. ¿Es candidato a aloTPH? Razona según EBMT y NCCN
2. ¿Qué tipo de acondicionamiento recomendarías (mieloablativo vs RIC)?
3. ¿Cuáles son los principales riesgos dados el perfil genético?
4. ¿Qué información le darías sobre la enfermedad injerto contra huésped?
5. ¿Cuál es la probabilidad de SLE a 2 años aproximada con este perfil?
```

---

## 17. Medicina Transfusional

### Indicaciones de transfusión restrictiva

```
Paciente postrasplante de médula ósea día +15:
- Hb: 7.2 g/dL  Plaquetas: 8.000/µL
- Sin fiebre, hemodinámicamente estable
- Mucositis grado 2, sin sangrado activo visible
- Dependencia transfusional alta: 2 concentrados/semana

Pregunta 1: ¿Cuál es el umbral de transfusión de hematíes en este contexto?
  (según AABB, BCSH, SETS 2024)

Pregunta 2: ¿Cuál es el umbral de transfusión de plaquetas aquí?
  ¿Cambia por la mucositis? ¿Por el estado febril/no febril?

Pregunta 3: ¿Qué características especiales deben tener los productos
  transfundidos en este paciente (irradiación, CMV negativo, leucodepleción)?
```

### Manejo de la refractariedad plaquetaria

```
Explícame el algoritmo diagnóstico y terapéutico de la refractariedad plaquetaria:

1. Definición de refractariedad (incremento correcto de plaquetas, ICC)
2. Causas no inmunes vs inmunes
3. Cómo estudiar la aloinmunización anti-HLA
4. Qué tipo de plaquetas pedir cuando hay refractariedad anti-HLA
5. Papel de los antifibrinolíticos y TPO-agonistas en este contexto
```

---

## 18. Hemopatías Benignas

### Ferropenia: caso con complejidad

```
Mujer 34 años, ferropenia refractaria a hierro oral (6 meses de tratamiento):

Analítica:
- Hb 9.2 g/dL, VCM 71 fL, HCM 22 pg
- Ferritina 4 µg/L, IST 6%, Fe sérico 28 µg/dL
- Receptor soluble de transferrina: 5.8 mg/L (elevado)
- Hepcidina: 2.1 nM (muy baja — VR 5-25 nM en mujeres)

Contexto: sin sangrado aparente, adherente al tratamiento oral

1. ¿Por qué fracasa el hierro oral si la hepcidina es baja (no hay bloqueo)?
2. Diagnóstico diferencial de ferropenia refractaria a oral con hepcidina baja
3. ¿Cuándo está indicado el hierro IV? ¿Qué preparado elegiría?
4. ¿Qué estudio adicional descartaría una enteropatía pierde-hierro?
5. ¿Cuál es el papel del gen TMPRSS6 en este contexto?
```

### Trombofilia y gestación

```
Mujer 28 años, 8 semanas de embarazo, 2 abortos previos de <10 semanas.
Estudio de trombofilia:
- Anticoagulante lúpico: positivo en 2 determinaciones (12 semanas aparte)
- Anticuerpos anticardiolipina IgG: 52 U/GPL (positivo moderado)
- Anti-β2 glicoproteína I: 28 U (positivo bajo)

Antecedentes: sin trombosis previas

1. Criterios de Sapporo/Sydney: ¿tiene síndrome antifosfolípido obstétrico?
2. Clasificación de riesgo según GAPSS score
3. Tratamiento recomendado en este embarazo (HBPM + AAS, solo AAS, nada)
4. ¿Cuándo iniciar, cómo monitorizar, cuándo suspender antes del parto?
5. ¿Está indicada la anticoagulación posparto? ¿Cuánto tiempo?
```

---

## PARTE IV — BIOINFORMÁTICA HEMATOLÓGICA

---

## 19. Análisis de NGS: Variantes Somáticas

### Pipeline completo de análisis

```
Escríbeme un pipeline en Python/bash para análisis básico de variantes somáticas
de un panel de 54 genes de leucemia (input: archivos FASTQ paired-end):

Pasos:
1. Control de calidad con FastQC + MultiQC
2. Alineamiento con BWA-MEM2 contra hg38
3. Marcado de duplicados con GATK MarkDuplicates
4. Variant calling con GATK Mutect2 (modo tumor-only con panel of normals)
5. Filtrado con FilterMutectCalls
6. Anotación con Variant Effect Predictor (VEP)
7. Filtrado por genes del panel y profundidad mínima (100x)
8. Generación de informe HTML con variantes clasificadas

Entorno: Conda, Linux. Muéstrame el código completo con comentarios.
```

### Cálculo de VAF y evolución clonal

```python
# Pide a Claude Code que genere este script completo

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

def plot_evolucion_clonal(archivo_csv):
    """
    Visualiza la evolución de clones (VAF) a lo largo del tiempo.
    Input CSV: gen, variante, timepoint, vaf, profundidad
    """
    df = pd.read_csv(archivo_csv)

    # Pivot para tener timepoints como columnas
    pivot = df.pivot_table(values='vaf', index=['gen', 'variante'],
                           columns='timepoint', fill_value=0)

    fig, ax = plt.subplots(figsize=(12, 6))
    colors = cm.tab20(np.linspace(0, 1, len(pivot)))

    for i, (idx, row) in enumerate(pivot.iterrows()):
        label = f"{idx[0]} {idx[1]}"
        ax.plot(pivot.columns, row.values, marker='o',
                label=label, color=colors[i], linewidth=2)

    ax.axhline(y=5, color='red', linestyle='--', alpha=0.5, label='Umbral detección 5%')
    ax.set_xlabel('Timepoint')
    ax.set_ylabel('VAF (%)')
    ax.set_title('Evolución Clonal - Dinámica de Variantes Somáticas')
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('evolucion_clonal.pdf', bbox_inches='tight', dpi=300)
    plt.show()

# Uso:
# plot_evolucion_clonal('variantes_seguimiento.csv')
```

---

## 20. Análisis de RNA-seq en Leucemias

### Análisis diferencial de expresión

```
Tengo datos de RNA-seq bulk de 20 muestras de LMA:
- 10 pacientes con NPM1 mutado (NPM1m)
- 10 pacientes con NPM1 wild-type (NPM1wt)

Los datos están en formato: matriz de counts (genes × muestras)

Escríbeme el análisis completo en R:
1. Control de calidad con DESeq2 (PCA, heatmap de clustering)
2. Análisis diferencial de expresión NPM1m vs NPM1wt
3. Volcano plot con genes significativos (FDR<0.05, |log2FC|>1) etiquetados
4. Gene Set Enrichment Analysis (GSEA) con hallmarks de MSigDB
5. Heatmap de los top 50 genes diferenciales
6. Identificación de la firma de HOX genes (característica de NPM1m)

Incluye el código completo para reproducir el análisis desde cero.
```

---

## 21. Automatización de Informes de Laboratorio

### Informe automático de hemograma

```python
# Pide a Claude Code que genere esta plantilla y la complete

from dataclasses import dataclass
from typing import Optional
import json

@dataclass
class Hemograma:
    # Serie roja
    hb: float          # g/dL
    vcm: float         # fL
    hcm: float         # pg
    chcm: float        # g/dL
    reticulocitos: float  # %

    # Serie blanca
    leucocitos: int    # /µL
    neutrofilos_pct: float
    linfocitos_pct: float
    monocitos_pct: float
    eosinofilos_pct: float
    basofilos_pct: float

    # Plaquetas
    plaquetas: int     # /µL
    vpm: float         # fL

    # Datos del paciente
    sexo: str          # 'M' o 'F'
    edad: int

def interpretar_hemograma(h: Hemograma) -> dict:
    alertas = []
    interpretacion = {}

    # --- Serie roja ---
    ref_hb = 13.0 if h.sexo == 'M' else 12.0
    if h.hb < ref_hb:
        grav = "leve" if h.hb >= 10 else ("moderada" if h.hb >= 8 else "grave")
        alertas.append(f"ANEMIA {grav.upper()}: Hb {h.hb} g/dL")

    morfologia = "normocítica normocrómica"
    if h.vcm < 80:
        morfologia = "microcítica" + (" hipocrómica" if h.hcm < 27 else "")
    elif h.vcm > 100:
        morfologia = "macrocítica"

    interpretacion['serie_roja'] = {
        'morfologia': morfologia,
        'anemia': h.hb < ref_hb,
        'indices_reticulocitario_corregido': round(h.reticulocitos * (h.hb/ref_hb) / 2, 2)
    }

    # --- Serie blanca ---
    n_abs = int(h.leucocitos * h.neutrofilos_pct / 100)
    l_abs = int(h.leucocitos * h.linfocitos_pct / 100)

    if h.leucocitos < 4000:
        alertas.append(f"LEUCOPENIA: {h.leucocitos}/µL")
    if h.leucocitos > 11000:
        alertas.append(f"LEUCOCITOSIS: {h.leucocitos}/µL")
    if n_abs < 1500:
        nivel = "leve" if n_abs >= 1000 else ("moderada" if n_abs >= 500 else "grave/agranulocitosis")
        alertas.append(f"NEUTROPENIA {nivel.upper()}: {n_abs}/µL")
    if n_abs > 7500:
        alertas.append(f"NEUTROFILIA: {n_abs}/µL")

    interpretacion['serie_blanca'] = {
        'neutrofilos_absolutos': n_abs,
        'linfocitos_absolutos': l_abs,
    }

    # --- Plaquetas ---
    if h.plaquetas < 150000:
        nivel = "leve" if h.plaquetas >= 100000 else ("moderada" if h.plaquetas >= 50000 else "grave")
        alertas.append(f"TROMBOCITOPENIA {nivel.upper()}: {h.plaquetas}/µL")
    if h.plaquetas > 450000:
        alertas.append(f"TROMBOCITOSIS: {h.plaquetas}/µL")

    interpretacion['plaquetas'] = {'normal': 150000 <= h.plaquetas <= 450000}
    interpretacion['alertas_criticas'] = alertas
    return interpretacion


# Ejemplo
hemo = Hemograma(
    hb=7.8, vcm=112, hcm=38, chcm=33, reticulocitos=1.2,
    leucocitos=3200, neutrofilos_pct=45, linfocitos_pct=42,
    monocitos_pct=8, eosinofilos_pct=3, basofilos_pct=2,
    plaquetas=98000, vpm=11.2,
    sexo='F', edad=62
)

resultado = interpretar_hemograma(hemo)
print(json.dumps(resultado, indent=2, ensure_ascii=False))
```

---

## PARTE V — PRÁCTICA GUIADA

---

## 22. Ejercicios Progresivos

Sigue la misma filosofía del L99: **intenta primero, pide ayuda después**.

### Nivel 1 — Básico (hemograma e interpretación)

**Ejercicio 1.1**
Escribe una función Python que clasifique anemias en microcítica, normocítica o macrocítica e incluya el diagnóstico diferencial para cada morfología. Pruébala con 5 casos distintos.

**Ejercicio 1.2**
Pide a Claude Code que te presente 5 hemogramas anónimos (sin diagnóstico) y practica interpretarlos antes de pedir la respuesta.

**Ejercicio 1.3**
Genera un gráfico de dispersión de VCM vs Hb para 50 pacientes simulados con anemia ferropénica, talasemia minor y anemia megaloblástica.

---

### Nivel 2 — Intermedio (neoplasias hematológicas)

**Ejercicio 2.1**
Crea una función que calcule el score IPSS-R para SMD usando las variables requeridas y clasifique el riesgo.

```
Inputs: blastos%, hemoglobina, plaquetas, neutrofilos, citogenética (categoria)
Output: puntuación numérica + categoría de riesgo + supervivencia mediana estimada
```

**Ejercicio 2.2**
Dada la clasificación ELN 2022 para LMA, crea un árbol de decisión en Python que, dados los resultados moleculares y citogenéticos, devuelva la categoría de riesgo y la recomendación de TPH en CR1.

**Ejercicio 2.3**
Analiza con Claude Code el siguiente caso y llega a diagnóstico y plan antes de pedir la corrección:
```
Mujer 45 años. Esplenomegalia masiva. Leucocitosis 180.000/µL con fórmula:
blastos 2%, promielocitos 4%, mielocitos 12%, metamielocitos 10%,
cayados 8%, segmentados 55%, basófilos 6%, eosinófilos 3%.
Plaquetas 820.000/µL. Hb 10.2 g/dL.
LDH: 3x el límite superior. ALC normal.
```

---

### Nivel 3 — Avanzado (bioinformática y genómica)

**Ejercicio 3.1**
Escribe un script que lea un archivo VCF simple y extraiga: gen, variante, VAF y profundidad de cobertura para los genes del panel ELN 2022.

**Ejercicio 3.2**
Genera un heatmap de expresión de 20 genes relevantes en LMA (HOXA9, HOXB4, FLT3, NPM1, DNMT3A, TET2, IDH1/2, WT1, EVI1...) usando datos simulados que representen 3 subtipos moleculares.

**Ejercicio 3.3**
Diseña un estudio de cohorte retrospectivo completo para evaluar el impacto de la negativización de ERM (por NPM1) en la recaída de LMA tras el primer ciclo de consolidación. Define: hipótesis, variables, análisis estadístico, tamaño muestral.

---

## 23. Límites Éticos y de Seguridad

### Lo que Claude Code puede hacer

- Educar y formar en hematología clínica
- Analizar datos anonimizados
- Generar código para investigación
- Asistir en revisión de literatura
- Ayudar a razonar casos clínicos complejos
- Generar borradores de documentación clínica

### Lo que Claude Code NO debe hacer (y no hará)

| Acción prohibida | Por qué |
|-----------------|---------|
| Diagnosticar pacientes reales sin supervisión médica | Responsabilidad médica intransferible |
| Prescribir dosis de quimioterapia directamente | Riesgo de error con consecuencias graves |
| Almacenar datos identificativos de pacientes | GDPR/HIPAA; privacidad |
| Reemplazar la evaluación clínica directa | El examen físico y el criterio son irreemplazables |
| Actuar como sistema de alerta de emergencia | No tiene capacidad de respuesta en tiempo real |

### Protocolo de uso seguro

```
ANTES de usar Claude Code en contexto clínico:

✓ Anonimizar todos los datos del paciente
✓ Verificar cualquier dosis o protocolo con fuente primaria
✓ No usar como única fuente de decisión clínica
✓ Documentar en la historia clínica que se usó IA como herramienta de apoyo
✓ Validar los resultados de código antes de aplicarlos a datos reales
```

---

## Ruta de Aprendizaje Recomendada

```
SEMANA 1-2: Fundamentos
├── Lee las secciones 1-3
├── Ejercicios 1.1, 1.2, 1.3
└── Practica interpretación de hemogramas con Claude Code

SEMANA 3-4: Diagnóstico hematológico
├── Secciones 9, 10, 12, 14
├── Ejercicio 2.2 (ELN 2022)
└── 10 casos clínicos generados por Claude Code

SEMANA 5-6: Genómica y molecular
├── Secciones 13, 19, 20
├── Ejercicios 3.1 y 3.2
└── Interpretar 5 paneles NGS simulados

SEMANA 7-8: Proyecto integrador
├── Diseña un estudio completo (ejercicio 3.3)
├── Automatiza un informe de laboratorio (sección 21)
└── Revisa los límites éticos (sección 23)
```

---

*Tutorial creado para el repositorio Aprendizaje — Claude Code en Medicina y Hematología*
*Fecha: mayo 2026 | Conocimiento clínico: actualizado hasta agosto 2025*
