"""
Ejercicio 2.3 — Caso Clínico: Leucemia Mieloide Crónica
Nivel 2 | Hematología con Claude Code

Modo de uso:
  1. Lee el caso clínico
  2. Responde las preguntas antes de ver las respuestas
  3. Ejecuta: python ejercicio_2_3_caso_lmc.py [--respuestas]
     Sin --respuestas: solo muestra el caso y las preguntas
     Con --respuestas: muestra las respuestas completas

Objetivo: diagnóstico y manejo de LMC en fase crónica.
"""

import sys

CASO_CLINICO = """
╔══════════════════════════════════════════════════════════════════╗
║  EJERCICIO 2.3 — CASO CLÍNICO: Leucemia Mieloide Crónica        ║
║  Hematología con Claude Code | Nivel 2                          ║
╚══════════════════════════════════════════════════════════════════╝

PRESENTACIÓN
────────────
Mujer de 45 años, sin antecedentes relevantes conocidos, que acude a su
médico de atención primaria por sensación de distensión abdominal,
saciedad precoz y fatiga de 2 meses de evolución.
La exploración física revela ESPLENOMEGALIA MASIVA (bazo palpable a 14 cm
bajo reborde costal izquierdo). Sin adenopatías. Afebril.

HEMOGRAMA URGENTE
─────────────────
  Hb             : 10.2 g/dL   (VCM 84 fL, normocítica)
  Leucocitos     : 180.000 /µL  ← LEUCOCITOSIS MASIVA
  Fórmula diferencial:
    Blastos       2%
    Promielocitos 4%
    Mielocitos    12%
    Metamielocitos 10%
    Cayados       8%
    Segmentados   55%
    Basófilos     6%    ← BASOFILIA SIGNIFICATIVA
    Eosinófilos   3%
  Plaquetas      : 820.000 /µL  ← TROMBOCITOSIS

BIOQUÍMICA
──────────
  LDH            : 3× LSN
  Ácido úrico    : 9.2 mg/dL (elevado)
  Vitamina B12   : 1.840 pg/mL (muy elevada — transcobalamina III)
  Fosfatasa alcalina leucocitaria (FAL): 8 U/L (MUY BAJA — VR 40-130)
"""

PREGUNTAS = [
    {
        "num": 1,
        "texto": "¿Cuál es tu diagnóstico más probable? Razona por qué.",
        "pista": "Fíjate en la basofilia, la trombocitosis, la B12 elevada y la FAL baja.",
    },
    {
        "num": 2,
        "texto": "¿Qué prueba confirmaría definitivamente el diagnóstico?",
        "pista": "Piensa en la anomalía genética característica de esta entidad.",
    },
    {
        "num": 3,
        "texto": "¿En qué fase de la enfermedad se encuentra la paciente? ¿Cuáles son los criterios?",
        "pista": "Blastos 2%, basófilos 6%... ¿cuáles son los umbrales de fase acelerada?",
    },
    {
        "num": 4,
        "texto": "¿Cuál es el tratamiento de primera línea actual? ¿Qué opciones existen?",
        "pista": "Inhibidores de tirosina quinasa (ITK) — primera, segunda y tercera generación.",
    },
    {
        "num": 5,
        "texto": "¿Cuál es el objetivo del tratamiento y cómo se monitoriza la respuesta?",
        "pista": "Piensa en respuesta hematológica, citogenética y molecular. Escala de log.",
    },
    {
        "num": 6,
        "texto": "¿En qué circunstancias considerarías el trasplante alogénico en LMC hoy en día?",
        "pista": "¿En qué fase ya no es opcional? ¿Qué mutación específica cambia el manejo?",
    },
]

RESPUESTAS = [
    {
        "num": 1,
        "titulo": "Diagnóstico: Leucemia Mieloide Crónica (LMC) en fase crónica",
        "desarrollo": """
El patrón es prácticamente patognomónico de LMC:

DATOS CLAVE Y SU INTERPRETACIÓN:
• Leucocitosis masiva (180.000/µL) con fórmula "escalonada":
  blastos < promielocitos < mielocitos... hasta segmentados
  → Serie granulocítica completa en sangre periférica
  → Esto no ocurre en reacciones leucemoides (que tienen solo cayados y segmentados)

• Basofilia (6%): característica de LMC — el basófilo es el "sello" de la LMC
  En reacciones leucemoides no hay basofilia

• Trombocitosis (820.000): la LMC estimula las 3 series
  (puede haber trombopenia en LMC avanzada/crisis blástica)

• B12 muy elevada: la transcobalamina III producida por granulocitos
  está elevada cuando hay hiperproducción granulocítica

• FAL muy baja (8 U/L): la actividad de fosfatasa alcalina LEUCOCITARIA
  es característica baja en LMC (a diferencia de reacciones leucemoides
  donde es alta — útil para el diagnóstico diferencial)

• Esplenomegalia masiva: por infiltración y hematopoyesis extramedular

DIAGNÓSTICO DIFERENCIAL:
  → Reacción leucemoide: FAL alta, no hay basofilia, causa precipitante
  → LMC vs otros SMP (PV, TE, MF): diferente fórmula y genética
  → LMC juvenil (LMMC): diferente biología""",
    },
    {
        "num": 2,
        "titulo": "Confirmación diagnóstica: detección del cromosoma Filadelfia / BCR::ABL1",
        "desarrollo": """
El diagnóstico definitivo de LMC requiere demostrar la anomalía BCR::ABL1:

TÉCNICAS (en orden de práctica clínica):
1. FISH en sangre periférica o MO: detecta t(9;22)(q34;q11)
   — Rápido (24-48h), sensibilidad ~95% — primera prueba en urgencias

2. Citogenética convencional (cariotipo):
   — Detecta el cromosoma Ph+ (Philadelphia) = der(22)
   — Confirma variantes citogenéticas adicionales (ACAs)
   — Necesita MO, tarda 10-14 días

3. RT-PCR cuantitativa (qPCR) de BCR::ABL1:
   — Cuantifica el transcrito (p210 en >95%, p190 en ~5%, p230 raro)
   — Establece la línea basal para monitorización
   — Escala IS (International Scale): el resultado en %IS es el estándar

4. NGS del dominio quinasa ABL1:
   — No en diagnóstico; sí en resistencia a ITK para detectar mutaciones
   — T315I = "gatekeeper mutation" → resistencia a todos los ITK excepto ponatinib

IMPORTANTE: la qPCR BCR::ABL1 basal es OBLIGATORIA al diagnóstico
para poder calcular la reducción logarítmica en la monitorización.""",
    },
    {
        "num": 3,
        "titulo": "Fase crónica — Criterios de fases según OMS/ELN",
        "desarrollo": """
FASE CRÓNICA (esta paciente):
• Blastos MO o SP < 10%
• Basófilos < 20%
• Plaquetas > 100.000
• Sin características de fase acelerada ni crisis blástica

Esta paciente:
  Blastos 2% (< 10%) ✓
  Basófilos 6% (< 20%) ✓
  Plaquetas 820.000 (> 100.000) ✓
  → FASE CRÓNICA confirmada

CRITERIOS DE FASE ACELERADA (cualquiera de):
  • Blastos MO o SP 10-19%
  • Basófilos ≥ 20%
  • Plaquetas < 100.000 sin relación con tratamiento
  • Plaquetas > 1.000.000 sin respuesta a terapia
  • Evolución citogenética clonal (CCA/Ph+)
  • Esplenomegalia creciente resistente a tratamiento

CRITERIOS DE CRISIS BLÁSTICA (cualquiera de):
  • Blastos MO o SP ≥ 20%
  • Proliferación extramedular de blastos
  • Focos grandes de blastos en biopsia de MO

La fase condiciona el tratamiento y el pronóstico:
  Fase crónica → ITK oral → excelentes resultados
  Fase acelerada → ITK 2G + evaluar TPH
  Crisis blástica → como leucemia aguda + ITK""",
    },
    {
        "num": 4,
        "titulo": "Tratamiento de primera línea: Inhibidores de Tirosina Quinasa (ITK)",
        "desarrollo": """
PRIMERA LÍNEA — opciones actuales (ELN 2020):

ITK 1ª GENERACIÓN:
  • Imatinib 400 mg/día v.o.
    Pionero. Excelente tolerancia a largo plazo.
    Tasa de RMM (BCR-ABL ≤0.1% IS) a 5 años ~60-65%
    Indicado especialmente si TFG reducido, edad avanzada o preocupación toxicidad

ITK 2ª GENERACIÓN (preferidos en pacientes de riesgo intermedio-alto):
  • Dasatinib 100 mg/día v.o.
    Más potente. RMM más rápida. Efectos adversos: derrame pleural, HAP
  • Nilotinib 300 mg/12h v.o. (en ayunas)
    Muy potente en fase crónica. Riesgo CV (estenosis arterial)
  • Bosutinib 400 mg/día v.o.
    Alternativa; menos mielosupresión

ITK 3ª GENERACIÓN (segunda línea / mutación T315I):
  • Ponatinib: activo frente a T315I — uso más restringido por toxicidad CV
  • Asciminib (STAMP inhibitor): nueva clase; se une al sitio miristoilo de ABL1

SCORE DE RIESGO (orienta la elección del ITK):
  Sokal score o ELTS score al diagnóstico:
  → Bajo riesgo: imatinib o 2G son equivalentes en SG a largo plazo
  → Intermedio/Alto riesgo: 2G recomendado (respuesta más profunda y rápida)

OBJETIVO TERAPÉUTICO:
  Llegar a remisión molecular mayor (RMM: BCR-ABL ≤0.1% IS)
  Idealmente remisión molecular profunda (RM4.5: BCR-ABL ≤0.0032% IS)
  para poder intentar la retirada del tratamiento (TFR — Treatment-Free Remission)""",
    },
    {
        "num": 5,
        "titulo": "Monitorización de la respuesta — Escala IS y hitos terapéuticos",
        "desarrollo": """
La respuesta al tratamiento se mide en tres niveles con hitos temporales (ELN 2020):

RESPUESTA HEMATOLÓGICA COMPLETA (RHC):
  • Leucocitos < 10.000/µL
  • Plaquetas < 450.000/µL
  • Fórmula normal, sin blastos
  • Bazo no palpable
  → Debe conseguirse en 3 meses

RESPUESTA CITOGENÉTICA COMPLETA (RCCit):
  • 0% metafases Ph+ en cariotipo
  ≡ BCR-ABL1 ≤1% IS (por RT-PCR) según equivalencia ELN
  → Debe conseguirse a los 12 meses

RESPUESTA MOLECULAR MAYOR (RMM):
  • BCR-ABL1 ≤0.1% IS (reducción ≥3-log desde línea basal)
  → Hito óptimo a los 12-18 meses
  → Si no se consigue → cambiar ITK

RESPUESTA MOLECULAR PROFUNDA (RM4, RM4.5):
  • RM4: BCR-ABL1 ≤0.01% IS
  • RM4.5: BCR-ABL1 ≤0.0032% IS
  → Necesaria para intentar TFR (retirada de tratamiento)

ESCALA IS (International Scale):
  El resultado se expresa como % BCR-ABL1/ABL1 en escala IS
  BCR-ABL1 10% IS = al diagnóstico (punto de partida)
  Cada log de reducción = 10 veces menos enfermedad
  RMM (0.1% IS) = reducción de 3 logaritmos desde el 100% IS

MONITORIZACIÓN PRÁCTICA:
  • 3 meses: RT-PCR qPCR BCR-ABL1
  • 6 meses: RT-PCR qPCR
  • 12 meses: RT-PCR qPCR + valorar cariotipo si no se ha documentado RCCit
  • Cada 3-6 meses hasta RM4.5 estable
  • Si fallo de respuesta: secuenciar dominio quinasa ABL1""",
    },
    {
        "num": 6,
        "titulo": "aloTPH en LMC — cuándo sigue siendo necesario",
        "desarrollo": """
CON LOS ITK MODERNOS, EL TPH EN LMC SE HA CONVERTIDO EN EXCEPCIONAL:

INDICACIONES ACTUALES DE aloTPH EN LMC:

1. CRISIS BLÁSTICA:
   → El TPH es la única opción curativa después de volver a remisión
   → La crisis blástica mieloide (30-40% de casos) tiene peor pronóstico que la linfoide

2. FASE ACELERADA AVANZADA O REFRACTARIA A ITK 2G/3G:
   → Si progresión a pesar de 2 líneas de ITK

3. MUTACIÓN T315I ("gatekeeper mutation"):
   → Causa resistencia a todos los ITK de 1ª y 2ª generación
   → Solo ponatinib y asciminib son activos
   → Si no hay respuesta a ponatinib: evaluar TPH

4. INTOLERANCIA A TODOS LOS ITK DISPONIBLES:
   → Raro pero posible (toxicidad cardíaca, hepática, renal graves)

5. LMC PEDIÁTRICA/JUVENIL DE ALTO RIESGO:
   → LMMC juvenil: diferente biología, ITK menos eficaces

EN FASE CRÓNICA ACTUAL:
La supervivencia con ITK es comparable a la población general
El TPH tiene mortalidad relacionada con el procedimiento (TRM 5-15%)
Por tanto, NO se indica TPH en fase crónica que responde a ITK

LA MUTACIÓN T315I EN CONTEXTO CLÍNICO:
  Si la paciente de este caso desarrollase resistencia al imatinib
  y la secuenciación mostrase T315I:
  → Cambiar a ponatinib (30 mg/día) o asciminib (200 mg/12h)
  → Si no respuesta: buscar donante y planificar aloTPH

RETIRADA DEL TRATAMIENTO (TFR):
  Objetivo actual en muchos pacientes: dejar el ITK
  Requisitos: RM4.5 mantenida ≥2 años + sin resistencia previa
  Tasa de éxito: ~50% mantienen RMM sin tratamiento a 2 años
  Monitorización muy estrecha tras retirada""",
    },
]


# ── Motor del ejercicio ───────────────────────────────────────────────────────

def mostrar_caso_y_preguntas() -> None:
    print(CASO_CLINICO)
    print("\n" + "─" * 65)
    print("  PREGUNTAS")
    print("─" * 65)
    for p in PREGUNTAS:
        print(f"\n  Pregunta {p['num']}: {p['texto']}")
        print(f"  💡 Pista: {p['pista']}")
    print("\n" + "─" * 65)
    print("  Para ver las respuestas: python ejercicio_2_3_caso_lmc.py --respuestas")
    print("─" * 65 + "\n")


def mostrar_respuestas() -> None:
    print(CASO_CLINICO)
    print("\n" + "═" * 65)
    print("  RESPUESTAS COMENTADAS")
    print("═" * 65)
    for p in PREGUNTAS:
        r = RESPUESTAS[p["num"] - 1]
        print(f"\n━━ Pregunta {p['num']}: {p['texto']}")
        print(f"\n   RESPUESTA: {r['titulo']}")
        for linea in r["desarrollo"].strip().split("\n"):
            print(f"   {linea}")
        print()
    print("═" * 65)
    print("\n  Autoevaluación sugerida:")
    print("  • ¿Identificaste la FAL baja como diagnóstico diferencial clave?")
    print("  • ¿Conocías los hitos de respuesta molecular (escala IS)?")
    print("  • ¿Sabías cuándo ya NO indicar TPH en LMC moderna?")
    print("  → Si fallaste ≥2: revisa las secciones 14 y 15 del tutorial.\n")


if __name__ == "__main__":
    if "--respuestas" in sys.argv:
        mostrar_respuestas()
    else:
        mostrar_caso_y_preguntas()
