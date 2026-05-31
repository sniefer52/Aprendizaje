"""
Ejercicio 2.1 — Calculadora IPSS-R para Síndrome Mielodisplásico
Nivel 2 | Hematología con Claude Code

Implementa el International Prognostic Scoring System Revised (IPSS-R)
para estratificación de riesgo en SMD.

Referencia: Greenberg et al., Blood 2012;120(12):2454-2465
"""

from dataclasses import dataclass
from typing import Optional
import sys


# ── Tablas de puntuación IPSS-R ───────────────────────────────────────────────

# Citogenética: clasificación pronóstica en 5 grupos
CITOGENETICA_GRUPOS = {
    "muy_buena":   (0.0, ["del(11q)", "-Y"]),
    "buena":       (1.0, ["Normal", "del(5q) sola", "del(12p)", "del(20q)",
                           "del(5q) con otra anomalía"]),
    "intermedia":  (2.0, ["del(7q)", "+8", "+19", "i(17q)",
                           "cualquier otra anomalía única o doble independiente"]),
    "mala":        (3.0, ["-7", "inv(3)/t(3q)/del(3q)", "doble con -7/del(7q)",
                           "Compleja (3 anomalías)"]),
    "muy_mala":    (4.0, ["Compleja: >3 anomalías"]),
}

def puntuacion_citogenetica(categoria: str) -> float:
    """categoria: 'muy_buena' | 'buena' | 'intermedia' | 'mala' | 'muy_mala'"""
    cat = categoria.lower().replace(" ", "_")
    if cat not in CITOGENETICA_GRUPOS:
        raise ValueError(f"Categoría citogenética no reconocida: {categoria}\n"
                         f"Opciones: {list(CITOGENETICA_GRUPOS.keys())}")
    return CITOGENETICA_GRUPOS[cat][0]


def puntuacion_blastos(blastos_pct: float) -> float:
    """% blastos en médula ósea"""
    if blastos_pct <= 2:
        return 0.0
    elif blastos_pct <= 4.9:
        return 1.0
    elif blastos_pct <= 10:
        return 2.0
    else:
        return 3.0   # >10%: fuera de rango SMD clásico, considerar LMA


def puntuacion_hemoglobina(hb: float, sexo: str = 'M') -> float:
    """hb en g/dL"""
    if hb >= 10:
        return 0.0
    elif hb >= 8:
        return 1.0
    else:
        return 1.5


def puntuacion_plaquetas(plaquetas: int) -> float:
    """/µL"""
    if plaquetas >= 100_000:
        return 0.0
    elif plaquetas >= 50_000:
        return 0.5
    else:
        return 1.0


def puntuacion_neutrofilos(neutrofilos: float) -> float:
    """/µL"""
    if neutrofilos >= 800:
        return 0.0
    else:
        return 0.5


# ── Clasificación de riesgo y supervivencia ───────────────────────────────────

CATEGORIAS_RIESGO = [
    (1.5,  "Muy bajo",    "≥ 8.8 años",  "No determinada"),
    (3.0,  "Bajo",        "5.3 años",    "Muy prolongada"),
    (4.5,  "Intermedio",  "3.0 años",    "~8-10 años"),
    (6.0,  "Alto",        "1.6 años",    "~3.5 años"),
    (999,  "Muy alto",    "0.8 años",    "~1.4 años"),
]

def clasificar_riesgo(puntuacion_total: float) -> dict:
    for umbral, categoria, sg_mediana, tiempo_25pct_lma in CATEGORIAS_RIESGO:
        if puntuacion_total <= umbral:
            return {
                "categoria": categoria,
                "sg_mediana": sg_mediana,
                "tiempo_25pct_evolucion_lma": tiempo_25pct_lma,
            }
    return {"categoria": "Muy alto", "sg_mediana": "0.8 años",
            "tiempo_25pct_evolucion_lma": "~1.4 años"}


# ── Estructura de datos y cálculo ─────────────────────────────────────────────

@dataclass
class DatosSMD:
    blastos_pct: float           # % blastos en MO
    citogenetica: str            # grupo citogenético IPSS-R
    hemoglobina: float           # g/dL
    plaquetas: int               # /µL
    neutrofilos: float           # /µL
    sexo: str = 'M'
    edad: int = 70
    nombre_caso: str = "Caso"


def calcular_ipss_r(datos: DatosSMD) -> dict:
    # Puntuaciones individuales
    p_blastos  = puntuacion_blastos(datos.blastos_pct)
    p_cito     = puntuacion_citogenetica(datos.citogenetica)
    p_hb       = puntuacion_hemoglobina(datos.hemoglobina, datos.sexo)
    p_plt      = puntuacion_plaquetas(datos.plaquetas)
    p_neut     = puntuacion_neutrofilos(datos.neutrofilos)

    total = p_blastos + p_cito + p_hb + p_plt + p_neut
    riesgo = clasificar_riesgo(total)

    # Ajuste por edad (IPSS-R ajustado por edad — Schanz et al. 2012)
    # Cada 10 años sobre 70 suma ~0.07 puntos al riesgo efectivo
    ajuste_edad = max(0, (datos.edad - 70) / 10 * 0.07)
    total_ajustado = round(total + ajuste_edad, 2)
    riesgo_ajustado = clasificar_riesgo(total_ajustado)

    return {
        "caso": datos.nombre_caso,
        "puntuaciones": {
            "blastos":       p_blastos,
            "citogenetica":  p_cito,
            "hemoglobina":   p_hb,
            "plaquetas":     p_plt,
            "neutrofilos":   p_neut,
        },
        "total":            round(total, 2),
        "total_ajustado_edad": total_ajustado,
        "riesgo":           riesgo["categoria"],
        "riesgo_ajustado_edad": riesgo_ajustado["categoria"],
        "sg_mediana":       riesgo["sg_mediana"],
        "tiempo_25pct_lma": riesgo["tiempo_25pct_evolucion_lma"],
    }


# ── Implicaciones terapéuticas ────────────────────────────────────────────────

RECOMENDACIONES_TRATAMIENTO = {
    "Muy bajo": (
        "Observación activa (watch & wait).\n"
        "Tratar solo complicaciones (transfusiones, factores estimulantes).\n"
        "Eritropoyetina si EPO sérica < 500 mU/mL y transfusión-dependencia baja."
    ),
    "Bajo": (
        "Tratamiento según síntomas y dependencia transfusional.\n"
        "Considerar luspatercept (si anillo de sideroblastos ≥15%) o lenalidomida (del5q).\n"
        "Factores estimulantes eritropoyéticos si EPO <200 mU/mL."
    ),
    "Intermedio": (
        "Valorar tratamiento activo: agentes hipometilantes (azacitidina).\n"
        "Evaluar candidatura a aloTPH (si <70 años y buen estado funcional).\n"
        "Ensayos clínicos recomendados."
    ),
    "Alto": (
        "Tratamiento activo urgente: azacitidina primera línea (nivel 1A).\n"
        "Alogerotrasplante hematopoyético si candidato — único tratamiento curativo.\n"
        "Considerar inducción tipo LMA para inducir remisión pretrasplante."
    ),
    "Muy alto": (
        "Tratamiento activo urgente: azacitidina ± venetoclax (en ensayos).\n"
        "aloTPH lo antes posible si candidato.\n"
        "Expectativa de vida muy reducida sin tratamiento intensivo."
    ),
}


# ── Presentación ─────────────────────────────────────────────────────────────

def imprimir_resultado_ipss_r(datos: DatosSMD, resultado: dict) -> None:
    sep = "═" * 62
    print(f"\n{sep}")
    print(f"  IPSS-R — {resultado['caso']}")
    print(f"  Paciente: {datos.sexo}/{datos.edad} años")
    print(sep)
    print(f"\n  PUNTUACIONES INDIVIDUALES:")
    print(f"    Blastos MO ({datos.blastos_pct}%)       : {resultado['puntuaciones']['blastos']}")
    print(f"    Citogenética ({datos.citogenetica:<15}) : {resultado['puntuaciones']['citogenetica']}")
    print(f"    Hemoglobina ({datos.hemoglobina} g/dL)  : {resultado['puntuaciones']['hemoglobina']}")
    print(f"    Plaquetas ({datos.plaquetas:,}/µL)      : {resultado['puntuaciones']['plaquetas']}")
    print(f"    Neutrófilos ({datos.neutrofilos:,}/µL)  : {resultado['puntuaciones']['neutrofilos']}")
    print(f"\n  PUNTUACIÓN TOTAL         : {resultado['total']}")
    print(f"  PUNTUACIÓN AJUST. EDAD   : {resultado['total_ajustado_edad']}")
    print(f"\n  CATEGORÍA DE RIESGO      : {resultado['riesgo']}")
    print(f"  (Ajustada por edad)      : {resultado['riesgo_ajustado_edad']}")
    print(f"\n  PRONÓSTICO:")
    print(f"    SG mediana estimada        : {resultado['sg_mediana']}")
    print(f"    25% evolución a LMA en     : {resultado['tiempo_25pct_lma']}")
    print(f"\n  IMPLICACIONES TERAPÉUTICAS:")
    for linea in RECOMENDACIONES_TRATAMIENTO.get(resultado['riesgo'], "Ver guías").split("\n"):
        print(f"    • {linea}")
    print(sep + "\n")


# ── Casos de prueba ───────────────────────────────────────────────────────────

CASOS_DEMO = [
    DatosSMD(
        nombre_caso="SMD Bajo Riesgo — del(5q) aislada",
        blastos_pct=2, citogenetica="buena",
        hemoglobina=9.0, plaquetas=320_000, neutrofilos=1800,
        sexo='F', edad=72,
    ),
    DatosSMD(
        nombre_caso="SMD Riesgo Intermedio — anemia refractaria",
        blastos_pct=5, citogenetica="intermedia",
        hemoglobina=8.2, plaquetas=85_000, neutrofilos=950,
        sexo='M', edad=68,
    ),
    DatosSMD(
        nombre_caso="SMD Alto Riesgo — monosomía 7",
        blastos_pct=12, citogenetica="mala",
        hemoglobina=7.1, plaquetas=32_000, neutrofilos=480,
        sexo='M', edad=61,
    ),
    DatosSMD(
        nombre_caso="SMD Muy Alto Riesgo — cariotipo complejo >3 anomalías",
        blastos_pct=17, citogenetica="muy_mala",
        hemoglobina=6.8, plaquetas=18_000, neutrofilos=320,
        sexo='F', edad=55,
    ),
]


if __name__ == "__main__":
    print("=" * 62)
    print("  EJERCICIO 2.1 — Calculadora IPSS-R para SMD")
    print("  Hematología con Claude Code | Nivel 2")
    print("=" * 62)

    for caso in CASOS_DEMO:
        resultado = calcular_ipss_r(caso)
        imprimir_resultado_ipss_r(caso, resultado)

    # Modo interactivo si se pasa argumento --interactivo
    if "--interactivo" in sys.argv:
        print("\n── MODO INTERACTIVO ──")
        print("Introduce los datos del paciente (Enter para omitir):\n")
        try:
            blastos  = float(input("% blastos en MO: "))
            print("Grupos citogenéticos: muy_buena | buena | intermedia | mala | muy_mala")
            cito     = input("Grupo citogenético: ").strip() or "intermedia"
            hb       = float(input("Hemoglobina (g/dL): "))
            plt_     = int(input("Plaquetas (/µL): "))
            neut     = float(input("Neutrófilos (/µL): "))
            sexo     = input("Sexo (M/F): ").strip().upper() or 'M'
            edad     = int(input("Edad (años): ") or "70")

            datos = DatosSMD(blastos_pct=blastos, citogenetica=cito,
                             hemoglobina=hb, plaquetas=plt_, neutrofilos=neut,
                             sexo=sexo, edad=edad, nombre_caso="Caso introducido")
            resultado = calcular_ipss_r(datos)
            imprimir_resultado_ipss_r(datos, resultado)
        except (ValueError, KeyboardInterrupt):
            print("\nEntrada cancelada o inválida.")
