"""
Ejercicio 1.2 — Banco de Casos de Hemograma
Nivel 1 | Hematología con Claude Code

Modo de uso:
  1. Ejecuta el script: python ejercicio_1_2_casos_hemograma.py
  2. Se presenta un caso con el hemograma completo (sin diagnóstico)
  3. Escribe tu interpretación antes de ver la respuesta
  4. El script revela el diagnóstico y la explicación
  5. Calcula tu puntuación al final

Objetivo: practicar interpretación sistemática de hemogramas.
"""

import random
import sys


# ── Banco de casos ────────────────────────────────────────────────────────────

CASOS = [
    {
        "id": 1,
        "hemograma": {
            "Hb": "6.2 g/dL",
            "VCM": "115 fL",
            "HCM": "38 pg",
            "CHCM": "33 g/dL",
            "Leucocitos": "2.800 /µL",
            "Neutrófilos": "58% (1.624 /µL)",
            "Linfocitos": "32% (896 /µL)",
            "Plaquetas": "88.000 /µL",
            "Reticulocitos": "0.4% (IR corregido = 0.3)",
        },
        "contexto": "Varón 71 años. Astenia progresiva 4 meses. "
                    "Frotis: hipersegmentación de neutrófilos (6-7 lóbulos), "
                    "macroovalocitos.",
        "diagnostico": "Anemia megaloblástica grave por déficit de vitamina B12",
        "explicacion": (
            "Patrón clásico de megaloblastosis:\n"
            "• Macrocitosis marcada (VCM>115) + pancitopenia\n"
            "• Mecanismo arregenerativo (IR=0.3): fallo medular por déficit de B12\n"
            "• La hipersegmentación neutrofílica (>5 lóbulos) es el hallazgo "
            "más temprano y específico del déficit B12/folato\n"
            "• Los macroovalocitos son característicos vs macrocitosis de hepatopatía\n"
            "• Edad+sexo+astenia lenta: pensar gastritis atrófica/anemia perniciosa\n"
            "Pruebas clave: B12 sérica, anticuerpos anti-factor intrínseco, "
            "ácido metilmalónico"
        ),
        "trampa": "La pancitopenia puede hacer pensar en SMD o aplasia — "
                  "el frotis con megaloblastos y la B12 baja lo aclaran.",
    },
    {
        "id": 2,
        "hemograma": {
            "Hb": "10.4 g/dL",
            "VCM": "68 fL",
            "HCM": "21 pg",
            "CHCM": "30 g/dL",
            "ADE (RDW)": "19% (elevado)",
            "Leucocitos": "7.200 /µL (normal)",
            "Plaquetas": "520.000 /µL",
            "Reticulocitos": "1.8% (IR corregido = 1.1)",
            "Ferritina": "4 µg/L",
            "IST": "5%",
        },
        "contexto": "Mujer 32 años. Menorragia intensa desde los 14 años. "
                    "Trombocitosis. Frotis: microcitos e hipocromía.",
        "diagnostico": "Anemia ferropénica moderada con trombocitosis reactiva",
        "explicacion": (
            "Ferropenia clásica:\n"
            "• Microcitosis + hipocromía + ferritina baja + IST bajo\n"
            "• ADE elevado: heterogeneidad en tamaño eritrocitario "
            "(mix microcitos + normocitos durante la depleción de Fe)\n"
            "• Trombocitosis reactiva: la ferropenia estimula la trombopoyesis "
            "a través de la TPO; desaparece con el tratamiento\n"
            "• IR 1.1: arregenerativa a pesar de microambiente inflamado "
            "(no hay hierro para sintetizar Hb)\n"
            "Causa: menorragia. Tratamiento: hierro oral + investigar causa ginecológica."
        ),
        "trampa": "La trombocitosis puede alarmar — en ferropenia es reactiva y benigna, "
                  "no requiere estudio de SMP.",
    },
    {
        "id": 3,
        "hemograma": {
            "Hb": "8.1 g/dL",
            "VCM": "91 fL",
            "HCM": "31 pg",
            "Leucocitos": "4.100 /µL",
            "Fórmula": "N 52%, L 38%, M 6%, E 2%, B 2%",
            "Plaquetas": "62.000 /µL",
            "Reticulocitos": "8.9% (IR corregido = 5.2)",
            "LDH": "980 UI/L (x3 LSN)",
            "Bilirrubina indirecta": "3.8 mg/dL",
            "Haptoglobina": "<0.1 g/L (indetectable)",
        },
        "contexto": "Mujer 45 años con LES. Ictericia escleral brusca. "
                    "Frotis: esferocitos abundantes (>10/campo), poiquilocitosis.",
        "diagnostico": "Anemia hemolítica autoinmune (AHAI) por anticuerpos calientes (IgG)",
        "explicacion": (
            "Patrón de hemólisis activa extravascular:\n"
            "• Anemia normocítica REGENERATIVA (IR=5.2): médula respondiendo activamente\n"
            "• Hemólisis: LDH↑ + BI↑ + haptoglobina indetectable (consumida)\n"
            "• Esferocitos: los macrófagos esplénicos fagocitan fragmentos de membrana "
            "recubiertos de IgG → el hematíe pierde bicóncavidad\n"
            "• LES: contexto de autoinmunidad favorece AHAI\n"
            "Confirmación: Coombs directo (IgG+, ±complemento)\n"
            "Tratamiento: prednisona 1 mg/kg/día → rituximab si refractario"
        ),
        "trampa": "El VCM 'normal' con IR=5.2 puede confundir — los reticulocitos "
                  "son macrocíticos y elevan el VCM medio; el patrón real es hemolítico.",
    },
    {
        "id": 4,
        "hemograma": {
            "Hb": "14.2 g/dL",
            "VCM": "88 fL",
            "Leucocitos": "68.000 /µL",
            "Blastos": "82%",
            "Plaquetas": "28.000 /µL",
            "LDH": "2.400 UI/L (x8 LSN)",
        },
        "contexto": "Niño 6 años. Fiebre 10 días, petequias, esplenomegalia moderada. "
                    "Frotis urgente: blastos con núcleo grande, cromatina laxa, "
                    "nucleolo prominente, citoplasma escaso. Sin granulaciones ni "
                    "bastones de Auer.",
        "diagnostico": "Leucemia aguda linfoblástica (LAL) — probable B-ALL",
        "explicacion": (
            "Presentación clásica de LAL en pediatría:\n"
            "• Pancitopenia + blastos circulantes (82%)\n"
            "• Morfología L1/L2 (FAB): blastos pequeños-medianos, sin gránulos, "
            "sin bastones de Auer (que son de LMA)\n"
            "• Edad (pico 2-8 años), esplenomegalia y fiebre: contexto típico\n"
            "• LDH muy elevada: alta carga tumoral\n"
            "Diagnóstico definitivo: inmunofenotipo (CD10+, CD19+, TdT+), "
            "citogenética (buscar t(12;21), hiperdiploidía favorable), "
            "FISH y PCR molecular"
        ),
        "trampa": "En adultos la LAL es menos frecuente y tiene peor pronóstico. "
                  "En niños, la LAL B-common con hiperdiploidía tiene >90% curación.",
    },
    {
        "id": 5,
        "hemograma": {
            "Hb": "11.8 g/dL",
            "VCM": "86 fL",
            "Leucocitos": "3.400 /µL",
            "Neutrófilos": "1.240 /µL",
            "Plaquetas": "105.000 /µL",
            "Reticulocitos": "0.6% (IR = 0.4)",
            "ADE (RDW)": "18%",
        },
        "contexto": "Varón 67 años. Astenia y disnea leve. Macrocitosis leve. "
                    "Frotis: displasia en serie eritroide (células binucleadas, "
                    "puentes internucleares). Algún mieloblasto aislado (<2%). "
                    "Sin historia de quimioterapia previa.",
        "diagnostico": "Síndrome mielodisplásico (SMD) — sospecha AR/ARSA",
        "explicacion": (
            "Patrón sugestivo de SMD:\n"
            "• Pancitopenia leve con anemia arregenerativa (IR=0.4) — médula no responde\n"
            "• Macrocitosis + ADE elevado: diseritropoyesis\n"
            "• Displasia en frotis: criterio morfológico mayor para SMD\n"
            "• Edad >60 años: incidencia máxima de SMD\n"
            "• No déficit de B12/folato (pensar siempre en ellos primero)\n"
            "Confirmación obligatoria: aspirado medular + biopsia + citogenética "
            "(del5q, -7, compleja)\n"
            "Estratificación: IPSS-R para orientar tratamiento"
        ),
        "trampa": "No confundir con ferropenia/déficit B12 — ambas dan macrocitosis, "
                  "pero la displasia morfológica y la citogenética son específicas del SMD.",
    },
]


# ── Motor del ejercicio ───────────────────────────────────────────────────────

def presentar_caso(caso: dict) -> None:
    print("\n" + "═" * 65)
    print(f"  CASO {caso['id']}")
    print("═" * 65)
    print("\n  HEMOGRAMA:")
    for param, valor in caso["hemograma"].items():
        print(f"    {param:<30} {valor}")
    print(f"\n  CONTEXTO CLÍNICO:")
    print(f"    {caso['contexto']}")
    print()


def mostrar_respuesta(caso: dict, respuesta_usuario: str) -> bool:
    print("\n" + "─" * 65)
    print(f"  DIAGNÓSTICO CORRECTO: {caso['diagnostico']}")
    print("\n  EXPLICACIÓN:")
    for linea in caso["explicacion"].split("\n"):
        print(f"    {linea}")
    print(f"\n  TRAMPA FRECUENTE:")
    print(f"    {caso['trampa']}")
    print("─" * 65)

    # Auto-evaluación básica: palabras clave en la respuesta del usuario
    claves = caso["diagnostico"].lower().split()
    aciertos = sum(1 for c in claves if c in respuesta_usuario.lower())
    correcto = aciertos >= max(1, len(claves) // 3)
    estado = "CORRECTO" if correcto else "INCORRECTO / PARCIAL"
    print(f"\n  Tu respuesta: \"{respuesta_usuario}\"")
    print(f"  Evaluación  : {estado}\n")
    return correcto


def ejecutar_sesion(n_casos: int = 3, aleatorio: bool = True) -> None:
    casos_seleccionados = CASOS.copy()
    if aleatorio:
        random.shuffle(casos_seleccionados)
    casos_seleccionados = casos_seleccionados[:n_casos]

    print("\n" + "═" * 65)
    print("  EJERCICIO 1.2 — BANCO DE CASOS DE HEMOGRAMA")
    print("  Instrucciones:")
    print("  • Lee el hemograma y el contexto clínico")
    print("  • Escribe tu interpretación/diagnóstico")
    print("  • Presiona Enter para ver la respuesta")
    print("═" * 65)

    aciertos = 0
    for i, caso in enumerate(casos_seleccionados, 1):
        print(f"\n  [{i}/{n_casos}]", end="")
        presentar_caso(caso)

        respuesta = input("  Tu diagnóstico (o presiona Enter para ver directamente): ").strip()
        if not respuesta:
            respuesta = "(sin respuesta)"

        if mostrar_respuesta(caso, respuesta):
            aciertos += 1

        if i < n_casos:
            input("  Presiona Enter para el siguiente caso...")

    # Resultado final
    print("\n" + "═" * 65)
    print(f"  RESULTADO FINAL: {aciertos}/{n_casos} correctos "
          f"({round(aciertos/n_casos*100)}%)")
    if aciertos == n_casos:
        print("  Excelente — dominas la interpretación básica del hemograma.")
    elif aciertos >= n_casos * 0.6:
        print("  Bien — repasa los casos fallados y sus explicaciones.")
    else:
        print("  Sigue practicando — vuelve a la sección 9 del tutorial.")
    print("═" * 65 + "\n")


if __name__ == "__main__":
    # Permite pasar el número de casos como argumento: python ejercicio_1_2.py 5
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    ejecutar_sesion(n_casos=min(n, len(CASOS)), aleatorio=True)
