"""
Ejercicio 1.1 — Clasificador de Anemias
Nivel 1 | Hematología con Claude Code

Objetivo: función que clasifique anemias por morfología y mecanismo
y devuelva el diagnóstico diferencial ordenado por probabilidad.
"""

from dataclasses import dataclass, field
from typing import Optional
import json


# ── Constantes clínicas ──────────────────────────────────────────────────────

REFERENCIA_HB = {'M': 13.0, 'F': 12.0}  # g/dL — adultos

VCM_BAJO  = 80   # fL
VCM_ALTO  = 100  # fL
HCM_BAJO  = 27   # pg
IR_UMBRAL = 2.0  # índice reticulocitario que separa regenerativa/arregenerativa


# ── Estructura de datos ──────────────────────────────────────────────────────

@dataclass
class ParametrosAnemia:
    hb: float              # Hemoglobina g/dL
    vcm: float             # Volumen corpuscular medio fL
    hcm: float             # Hemoglobina corpuscular media pg
    chcm: float            # Concentración de Hb corpuscular media g/dL
    reticulocitos_pct: float   # Reticulocitos en %
    sexo: str              # 'M' o 'F'
    edad: int
    contexto_clinico: Optional[str] = None   # pistas adicionales opcionales


@dataclass
class ResultadoClasificacion:
    tiene_anemia: bool
    gravedad: Optional[str] = None           # leve / moderada / grave / muy grave
    morfologia: Optional[str] = None         # microcítica / normocítica / macrocítica
    colorimetria: Optional[str] = None       # hipocrómica / normocrómica
    mecanismo: Optional[str] = None          # arregenerativa / regenerativa
    indice_reticulocitario: Optional[float] = None
    diagnostico_diferencial: list = field(default_factory=list)
    alertas_criticas: list = field(default_factory=list)
    pruebas_recomendadas: list = field(default_factory=list)
    comentario_clinico: str = ""


# ── Lógica de clasificación ──────────────────────────────────────────────────

def clasificar_anemia(p: ParametrosAnemia) -> ResultadoClasificacion:
    ref_hb = REFERENCIA_HB.get(p.sexo.upper(), 13.0)
    resultado = ResultadoClasificacion(tiene_anemia=False)

    if p.hb >= ref_hb:
        resultado.comentario_clinico = "Hemoglobina dentro de rango normal."
        return resultado

    resultado.tiene_anemia = True

    # ── Gravedad ──────────────────────────────────────────────────────────────
    if p.hb >= 10.0:
        resultado.gravedad = "leve"
    elif p.hb >= 8.0:
        resultado.gravedad = "moderada"
    elif p.hb >= 6.5:
        resultado.gravedad = "grave"
    else:
        resultado.gravedad = "muy grave"
        resultado.alertas_criticas.append(
            f"ALERTA: Hb {p.hb} g/dL — riesgo vital, valorar transfusión urgente"
        )

    # ── Morfología / colorimetría ─────────────────────────────────────────────
    if p.vcm < VCM_BAJO:
        resultado.morfologia = "microcítica"
        resultado.colorimetria = "hipocrómica" if p.hcm < HCM_BAJO else "normocrómica"
    elif p.vcm > VCM_ALTO:
        resultado.morfologia = "macrocítica"
        resultado.colorimetria = "normocrómica"  # macrocítica suele ser normocrómica
    else:
        resultado.morfologia = "normocítica"
        resultado.colorimetria = "hipocrómica" if p.hcm < HCM_BAJO else "normocrómica"

    # ── Mecanismo: índice reticulocitario corregido ───────────────────────────
    # IR = (retic% × Hb_paciente/Hb_normal) / factor_maduración
    # Factor de maduración: 1 si Hb≥10, 1.5 si 8-10, 2 si <8
    if p.hb >= 10:
        factor = 1.0
    elif p.hb >= 8:
        factor = 1.5
    else:
        factor = 2.0
    ir = (p.reticulocitos_pct * (p.hb / ref_hb)) / factor
    resultado.indice_reticulocitario = round(ir, 2)
    resultado.mecanismo = "regenerativa" if ir >= IR_UMBRAL else "arregenerativa"

    # ── Diagnóstico diferencial (ordenado por probabilidad según patrón) ──────
    dd, pruebas = _diagnostico_diferencial(resultado.morfologia,
                                           resultado.mecanismo,
                                           p)
    resultado.diagnostico_diferencial = dd
    resultado.pruebas_recomendadas = pruebas

    # ── Comentario clínico integrador ────────────────────────────────────────
    resultado.comentario_clinico = (
        f"Anemia {resultado.gravedad} {resultado.morfologia} {resultado.colorimetria}, "
        f"{resultado.mecanismo} (IR={resultado.indice_reticulocitario}). "
        f"Diagnóstico más probable: {dd[0] if dd else 'indeterminado'}."
    )

    return resultado


def _diagnostico_diferencial(morfologia: str, mecanismo: str,
                              p: ParametrosAnemia) -> tuple[list, list]:
    """Devuelve (lista_dd, lista_pruebas) según patrón morfológico y mecanismo."""

    if morfologia == "microcítica":
        if mecanismo == "arregenerativa":
            dd = [
                "1. Ferropenia (causa más frecuente de anemia microcítica)",
                "2. Anemia de proceso crónico/inflamación (APC) — puede ser microcítica",
                "3. Talasemia minor (alfa o beta)",
                "4. Anemia sideroblástica",
                "5. Intoxicación por plomo",
            ]
            pruebas = [
                "Hierro sérico, ferritina, IST (índice de saturación de transferrina)",
                "Receptor soluble de transferrina (rsTfR)",
                "Hepcidina sérica (distingue ferropenia de APC)",
                "Hemoglobina A2 y HbF (HPLC para talasemia)",
                "Frotis de sangre periférica (dianocitos en talasemia, punteado basófilo)",
                "Si APC sospechada: PCR, VSG, perfil hepático",
            ]
        else:  # regenerativa microcítica es raro → pensar talasemia homocigota o hemólisis
            dd = [
                "1. Talasemia intermedia o major",
                "2. Hemoglobinopatía estructural (HbS, HbC, HbE)",
                "3. Anemia sideroblástica congénita con respuesta parcial",
            ]
            pruebas = [
                "HPLC de hemoglobinas",
                "Electroforesis de hemoglobina",
                "Estudio familiar",
            ]

    elif morfologia == "macrocítica":
        if mecanismo == "arregenerativa":
            dd = [
                "1. Déficit de vitamina B12 (cobalamina)",
                "2. Déficit de ácido fólico",
                "3. Síndrome mielodisplásico (SMD) — especialmente en >60 años",
                "4. Hipotiroidismo",
                "5. Hepatopatía crónica / alcoholismo",
                "6. Fármacos (metotrexato, hidroxiurea, zidovudina, quimioterapia)",
                "7. Aplasia medular (si pancitopenia asociada)",
            ]
            pruebas = [
                "Vitamina B12 sérica",
                "Ácido fólico (eritrocitario más fiable que el sérico)",
                "Ácido metilmalónico y homocisteína (si B12 en zona gris 150-300 pg/mL)",
                "TSH (hipotiroidismo)",
                "Función hepática, GGT",
                "Frotis: megaloblastosis, hipersegmentación de neutrófilos (>5 lóbulos)",
                "Si SMD sospechado: aspirado de médula ósea + citogenética",
            ]
        else:  # macrocítica regenerativa → reticulocitosis
            dd = [
                "1. Hemólisis con reticulocitosis (reticulocitos macrocíticos)",
                "2. Sangrado agudo con respuesta medular activa",
                "3. Tratamiento de ferropenia / déficit B12 en fase de respuesta",
            ]
            pruebas = [
                "Bilirrubina indirecta, LDH, haptoglobina",
                "Test de Coombs directo (hemólisis inmune)",
                "Frotis (esquistocitos, esferocitos)",
            ]

    else:  # normocítica
        if mecanismo == "arregenerativa":
            dd = [
                "1. Anemia de proceso crónico/inflamación (APC) — forma normocítica",
                "2. Anemia de insuficiencia renal (déficit EPO)",
                "3. Aplasia medular",
                "4. Infiltración medular (leucemia, linfoma, metástasis, mielofibrosis)",
                "5. Hipotiroidismo (forma normocítica)",
                "6. Déficit mixto B12+Fe en estadio inicial",
                "7. Síndrome mielodisplásico (forma normocítica)",
            ]
            pruebas = [
                "Creatinina, filtrado glomerular (insuficiencia renal)",
                "Ferritina, IST, PCR (APC vs ferropenia)",
                "TSH",
                "LDH, ácido úrico (infiltración medular)",
                "Frotis de sangre periférica",
                "Biopsia de médula ósea si pancitopenia o sospecha de infiltración",
            ]
        else:  # normocítica regenerativa → hemólisis o sangrado
            dd = [
                "1. Anemia hemolítica autoinmune (AHAI)",
                "2. Esferocitosis hereditaria",
                "3. Deficiencia de G6PD",
                "4. Anemia hemolítica microangiopática (MAT: PTT, SHU, CID)",
                "5. Drepanocitosis en crisis vaso-oclusiva",
                "6. Sangrado agudo oculto",
            ]
            pruebas = [
                "Test de Coombs directo e indirecto",
                "Bilirrubina indirecta, LDH, haptoglobina",
                "Frotis urgente (esferocitos, esquistocitos, drepanoci­tos)",
                "Prueba de fragilidad osmótica (esferocitosis hereditaria)",
                "Actividad G6PD",
                "Dímero-D, APTT, fibrinógeno (si MAT)",
                "Búsqueda de sangrado oculto (SOH, endoscopia)",
            ]

    return dd, pruebas


# ── Presentación del resultado ───────────────────────────────────────────────

def imprimir_resultado(p: ParametrosAnemia, r: ResultadoClasificacion) -> None:
    sep = "─" * 60
    print(f"\n{sep}")
    print(f"  INFORME DE CLASIFICACIÓN DE ANEMIA")
    print(f"  Paciente: {p.sexo}/{p.edad} años  |  Hb: {p.hb} g/dL  "
          f"VCM: {p.vcm} fL  HCM: {p.hcm} pg")
    print(sep)

    if not r.tiene_anemia:
        print("  → Sin anemia. Hemoglobina dentro de rango normal.\n")
        return

    print(f"  Gravedad    : {r.gravedad.upper()}")
    print(f"  Morfología  : {r.morfologia} {r.colorimetria}")
    print(f"  Mecanismo   : {r.mecanismo} (IR corregido = {r.indice_reticulocitario})")
    print(f"\n  {r.comentario_clinico}")

    if r.alertas_criticas:
        print(f"\n  ⚠  ALERTAS CRÍTICAS:")
        for a in r.alertas_criticas:
            print(f"     {a}")

    print(f"\n  DIAGNÓSTICO DIFERENCIAL:")
    for d in r.diagnostico_diferencial:
        print(f"    {d}")

    print(f"\n  PRUEBAS RECOMENDADAS:")
    for pr in r.pruebas_recomendadas:
        print(f"    • {pr}")
    print(sep + "\n")


# ── Casos de prueba ──────────────────────────────────────────────────────────

CASOS = [
    {
        "descripcion": "Caso A — Ferropenia clásica",
        "params": ParametrosAnemia(hb=8.9, vcm=72, hcm=23, chcm=29,
                                   reticulocitos_pct=1.1, sexo='F', edad=28,
                                   contexto_clinico="Menorragia intensa, sin carne en dieta"),
    },
    {
        "descripcion": "Caso B — Déficit de B12",
        "params": ParametrosAnemia(hb=7.4, vcm=118, hcm=36, chcm=31,
                                   reticulocitos_pct=0.8, sexo='M', edad=68,
                                   contexto_clinico="Parestesias MMII, glositis, gastrectomía hace 10 años"),
    },
    {
        "descripcion": "Caso C — Hemólisis autoinmune",
        "params": ParametrosAnemia(hb=7.1, vcm=98, hcm=32, chcm=33,
                                   reticulocitos_pct=9.4, sexo='F', edad=42,
                                   contexto_clinico="Ictericia, orina oscura, LES conocido"),
    },
    {
        "descripcion": "Caso D — Anemia de proceso crónico",
        "params": ParametrosAnemia(hb=9.8, vcm=84, hcm=28, chcm=32,
                                   reticulocitos_pct=1.3, sexo='M', edad=55,
                                   contexto_clinico="AR activa, PCR 45 mg/L, ferritina 210 µg/L"),
    },
    {
        "descripcion": "Caso E — Anemia muy grave por sangrado (aplasia sospechada)",
        "params": ParametrosAnemia(hb=5.8, vcm=88, hcm=30, chcm=33,
                                   reticulocitos_pct=0.3, sexo='M', edad=34,
                                   contexto_clinico="Pancitopenia, astenia progresiva 3 meses"),
    },
]


if __name__ == "__main__":
    print("=" * 60)
    print("  EJERCICIO 1.1 — Clasificador de Anemias")
    print("  Hematología con Claude Code | Nivel 1")
    print("=" * 60)

    for caso in CASOS:
        print(f"\n>>> {caso['descripcion']}")
        if caso["params"].contexto_clinico:
            print(f"    Contexto: {caso['params'].contexto_clinico}")
        resultado = clasificar_anemia(caso["params"])
        imprimir_resultado(caso["params"], resultado)
