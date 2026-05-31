"""
Ejercicio 2.2 — Clasificador de Riesgo ELN 2022 para LMA
Nivel 2 | Hematología con Claude Code

Implementa el árbol de decisión ELN (European LeukemiaNet) 2022
para estratificación de riesgo en leucemia mieloide aguda (LMA).

Referencia: Döhner et al., Blood 2022;140(12):1345-1377

Incluye:
  • Clasificación Favorable / Intermedio / Adverso
  • Indicación de aloTPH en CR1
  • Dianas terapéuticas identificadas
"""

from dataclasses import dataclass, field
from typing import Optional


# ── Estructura de datos de entrada ───────────────────────────────────────────

@dataclass
class PerfilLMA:
    # ── Citogenética ──────────────────────────────────────────────────────────
    t_8_21: bool = False          # t(8;21)(q22;q22.1); RUNX1::RUNX1T1
    inv16_t16_16: bool = False    # inv(16)(p13.1q22) o t(16;16); CBFB::MYH11
    t_15_17: bool = False         # t(15;17) — APL/LPA
    t_9_11: bool = False          # t(9;11)(p21.3;q23.3); KMT2A::MLLT3

    # LPA — excluir antes de ELN para el resto
    es_lpa: bool = False

    # Anomalías citogenéticas adversas
    t_6_9: bool = False           # t(6;9)(p23;q34.1); DEK::NUP214
    t_v_11q23: bool = False       # t(v;11q23.3) excepto t(9;11)
    t_9_22: bool = False          # t(9;22)(q34.1;q11.2); BCR::ABL1
    inv3_t3_3: bool = False       # inv(3)/t(3;3); GATA2/MECOM(EVI1)
    monosomia_5: bool = False     # -5 o del(5q)
    monosomia_7: bool = False     # -7
    monosomia_17: bool = False    # -17/abn(17p)
    cariotipo_complejo: bool = False  # ≥3 anomalías
    cariotipo_monosomal: bool = False

    # ── Molecular ─────────────────────────────────────────────────────────────
    npm1_mut: bool = False        # mutación NPM1
    cebpa_biallelica: bool = False  # CEBPα bialélica
    flt3_itd: bool = False        # FLT3-ITD (cualquier ratio)
    flt3_itd_ratio: Optional[float] = None  # ratio FLT3-ITD/WT
    flt3_tkd: bool = False        # FLT3-TKD (D835)

    tp53_mut: bool = False        # TP53 mutado
    runx1_mut: bool = False       # RUNX1 mutado (sin t(8;21) ni t(9;11))
    asxl1_mut: bool = False       # ASXL1 mutado
    ezh2_mut: bool = False        # EZH2 mutado
    sf3b1_mut: bool = False       # SF3B1 mutado
    srsf2_mut: bool = False       # SRSF2 mutado
    stag2_mut: bool = False       # STAG2 mutado
    u2af1_mut: bool = False       # U2AF1 mutado
    zrsr2_mut: bool = False       # ZRSR2 mutado
    bcor_mut: bool = False        # BCOR mutado
    dnmt3a_r882: bool = False     # DNMT3A R882

    idh1_mut: bool = False        # IDH1 mutado
    idh2_mut: bool = False        # IDH2 mutado

    # ── Contexto clínico ──────────────────────────────────────────────────────
    lma_post_smp: bool = False    # post-SMP (mielofibrosis, PV, TE)
    lma_post_smd: bool = False    # post-SMD (tMD: terapia previa)
    lma_terapia: bool = False     # relacionada con terapia citotóxica/RT
    blastos_mo: Optional[float] = None
    edad: int = 60
    sexo: str = 'M'
    nombre_caso: str = "Caso LMA"


# ── Motor de clasificación ELN 2022 ──────────────────────────────────────────

@dataclass
class ResultadoELN:
    riesgo: str = ""
    subcategoria: str = ""
    justificacion: list = field(default_factory=list)
    indicadores_favorables: list = field(default_factory=list)
    indicadores_adversos: list = field(default_factory=list)
    dianas_terapeuticas: list = field(default_factory=list)
    indicacion_tph_cr1: str = ""
    recomendacion_inhibidores: list = field(default_factory=list)
    marcadores_erm: list = field(default_factory=list)


def clasificar_eln_2022(p: PerfilLMA) -> ResultadoELN:
    r = ResultadoELN()

    # ── Caso especial: LPA ────────────────────────────────────────────────────
    if p.es_lpa or p.t_15_17:
        r.riesgo = "LPA — circuito diagnóstico-terapéutico propio"
        r.subcategoria = "Leucemia promielocítica aguda"
        r.justificacion = [
            "t(15;17)(q24.1;q21.2); PML::RARA — diagnóstico de LPA",
            "NO se aplica la clasificación ELN estándar",
            "Tratamiento: ATRA + ATO (arsénico) ± quimioterapia",
            "Riesgo de CID: iniciar ATRA urgente",
        ]
        r.dianas_terapeuticas = ["PML::RARA → ATRA + trióxido de arsénico"]
        r.marcadores_erm = ["PML::RARA por PCR (sensibilidad 10⁻⁵)"]
        return r

    adversos = []
    favorables = []

    # ── FAVORABLE ─────────────────────────────────────────────────────────────
    es_cbf = p.t_8_21 or p.inv16_t16_16

    if p.t_8_21:
        favorables.append("t(8;21)(q22;q22.1); RUNX1::RUNX1T1 — leucemia de core binding factor")
    if p.inv16_t16_16:
        favorables.append("inv(16)/t(16;16); CBFB::MYH11 — leucemia de core binding factor")
    if p.npm1_mut and not p.flt3_itd:
        favorables.append("NPM1 mutado sin FLT3-ITD — pronóstico favorable")
    if p.npm1_mut and p.flt3_itd and (p.flt3_itd_ratio is not None and p.flt3_itd_ratio < 0.5):
        favorables.append("NPM1 mut + FLT3-ITD ratio bajo (<0.5) — pronóstico favorable según ELN 2022")
    if p.cebpa_biallelica:
        favorables.append("CEBPα bialélica — favorece la diferenciación, buen pronóstico")

    # ── ADVERSO ──────────────────────────────────────────────────────────────
    if p.tp53_mut:
        adversos.append("TP53 mutado — adverso muy alto, especialmente bialélico")
    if p.runx1_mut and not p.t_8_21:
        adversos.append("RUNX1 mutado — adverso (sin contexto t(8;21))")
    if p.asxl1_mut:
        adversos.append("ASXL1 mutado — adverso")
    if p.t_6_9:
        adversos.append("t(6;9)(p23;q34.1); DEK::NUP214 — adverso")
    if p.t_v_11q23:
        adversos.append("t(v;11q23.3) excepto t(9;11) — adverso")
    if p.t_9_22:
        adversos.append("t(9;22)(q34.1;q11.2); BCR::ABL1 — adverso")
    if p.inv3_t3_3:
        adversos.append("inv(3)/t(3;3); GATA2/MECOM — adverso alto")
    if p.monosomia_5:
        adversos.append("-5 o del(5q) — adverso")
    if p.monosomia_7:
        adversos.append("-7 — adverso")
    if p.monosomia_17:
        adversos.append("-17/abn(17p) — adverso")
    if p.cariotipo_complejo:
        adversos.append("Cariotipo complejo (≥3 anomalías) — adverso")
    if p.cariotipo_monosomal:
        adversos.append("Cariotipo monosomal — adverso muy alto")
    if p.lma_terapia:
        adversos.append("LMA relacionada con terapia previa — adverso")
    if p.lma_post_smd:
        adversos.append("LMA con cambios relacionados con mielodisplasia — adverso")
    if any([p.sf3b1_mut, p.srsf2_mut, p.stag2_mut, p.u2af1_mut, p.zrsr2_mut,
            p.ezh2_mut, p.bcor_mut]):
        adversos.append("Mutaciones en genes de splicing/cromatina (SF3B1/SRSF2/STAG2"
                        "/U2AF1/ZRSR2/EZH2/BCOR) — adverso si sin t(8;21)/inv(16)/NPM1m")
    if p.flt3_itd and not p.npm1_mut:
        adversos.append("FLT3-ITD sin NPM1mut — adverso (especialmente si ratio alto)")
    if p.flt3_itd and p.npm1_mut and p.flt3_itd_ratio and p.flt3_itd_ratio >= 0.5:
        adversos.append("FLT3-ITD ratio alto (≥0.5) + NPM1mut — reclasificado a intermedio/adverso ELN 2022")

    # ── Asignación de categoría ───────────────────────────────────────────────
    if adversos and not favorables:
        r.riesgo = "Adverso"
    elif adversos and favorables:
        # Las anomalías adversas dominan sobre las favorables (regla ELN 2022)
        r.riesgo = "Adverso"
        r.subcategoria = "Anomalías adversas presentes a pesar de marcadores favorables"
    elif favorables and not adversos:
        r.riesgo = "Favorable"
    else:
        # Sin marcadores claros → intermedio
        # FLT3-ITD con NPM1m sin ratio o FLT3-TKD solo → intermedio
        if p.flt3_itd and p.npm1_mut:
            r.riesgo = "Intermedio"
            r.subcategoria = "NPM1mut + FLT3-ITD ratio alto o desconocido"
        elif p.t_9_11:
            r.riesgo = "Intermedio"
            r.subcategoria = "t(9;11)(p21.3;q23.3); KMT2A::MLLT3"
            favorables.append("t(9;11): intermedio (mejor que otras t(v;11q23))")
        elif p.dnmt3a_r882:
            r.riesgo = "Intermedio"
            r.subcategoria = "DNMT3A R882 como única alteración"
        else:
            r.riesgo = "Intermedio"
            r.subcategoria = "Sin marcadores citogenéticos/moleculares clasificatorios"

    r.indicadores_favorables = favorables
    r.indicadores_adversos = adversos

    # ── Indicación de aloTPH en CR1 ───────────────────────────────────────────
    if r.riesgo == "Favorable" and not es_cbf:
        r.indicacion_tph_cr1 = (
            "aloTPH en CR1 no indicado de forma estándar en riesgo favorable.\n"
            "Excepción: ERM positiva persistente o recaída molecular."
        )
    elif r.riesgo == "Favorable" and es_cbf:
        r.indicacion_tph_cr1 = (
            "CBF-LMA: consolidación con altas dosis de citarabina (4 ciclos).\n"
            "aloTPH solo en fallo de ERM o recaída."
        )
    elif r.riesgo == "Intermedio":
        r.indicacion_tph_cr1 = (
            "aloTPH en CR1 recomendado si donante disponible y paciente apto.\n"
            "Decisión individualizada según ERM, edad y comorbilidades."
        )
    elif r.riesgo == "Adverso":
        r.indicacion_tph_cr1 = (
            "aloTPH en CR1 FUERTEMENTE recomendado — es el único tratamiento\n"
            "con potencial curativo en LMA de riesgo adverso.\n"
            "Iniciar búsqueda de donante inmediatamente al diagnóstico."
        )

    # ── Dianas terapéuticas ───────────────────────────────────────────────────
    if p.flt3_itd or p.flt3_tkd:
        r.dianas_terapeuticas.append(
            "FLT3 mutado → añadir midostaurina a DA en inducción (RATIFY)"
        )
        r.recomendacion_inhibidores.append(
            "Midostaurina 50 mg/12h v.o. días 8-21 del ciclo"
        )
        if p.flt3_itd:
            r.recomendacion_inhibidores.append(
                "Quizartinib o gilteritinib en recaída/refractariedad"
            )
    if p.idh1_mut:
        r.dianas_terapeuticas.append("IDH1 mutado → ivosidenib (FDA aprobado en RC+/RCi)")
    if p.idh2_mut:
        r.dianas_terapeuticas.append("IDH2 mutado → enasidenib")
    if p.npm1_mut:
        r.dianas_terapeuticas.append("NPM1mut → menin inhibidores (revumenib) en recaída")
    if p.t_9_22:
        r.dianas_terapeuticas.append("BCR::ABL1 → añadir inhibidor de tirosina quinasa (dasatinib)")

    # ── Marcadores ERM ────────────────────────────────────────────────────────
    if p.npm1_mut:
        r.marcadores_erm.append("NPM1mut por PCR cuantitativa (sensibilidad 10⁻⁵ — estándar ELN)")
    if p.t_8_21:
        r.marcadores_erm.append("RUNX1::RUNX1T1 por RT-PCR cuantitativa")
    if p.inv16_t16_16:
        r.marcadores_erm.append("CBFB::MYH11 por RT-PCR cuantitativa")
    if p.flt3_itd:
        r.marcadores_erm.append("FLT3-ITD por PCR (menor sensibilidad — complementar con CMF)")
    if not r.marcadores_erm:
        r.marcadores_erm.append("CMF multiparámetro (citometría) — si no hay marcador molecular específico")

    return r


# ── Presentación ──────────────────────────────────────────────────────────────

def imprimir_resultado_eln(perfil: PerfilLMA, r: ResultadoELN) -> None:
    sep = "═" * 65
    print(f"\n{sep}")
    print(f"  ELN 2022 — {perfil.nombre_caso}")
    print(f"  Paciente: {perfil.sexo}/{perfil.edad} años")
    if perfil.blastos_mo:
        print(f"  Blastos MO: {perfil.blastos_mo}%")
    print(sep)

    print(f"\n  CATEGORÍA DE RIESGO ELN 2022: {r.riesgo.upper()}")
    if r.subcategoria:
        print(f"  Subcategoría: {r.subcategoria}")

    if r.indicadores_favorables:
        print(f"\n  MARCADORES FAVORABLES:")
        for m in r.indicadores_favorables:
            print(f"    ✓ {m}")
    if r.indicadores_adversos:
        print(f"\n  MARCADORES ADVERSOS:")
        for m in r.indicadores_adversos:
            print(f"    ✗ {m}")

    print(f"\n  INDICACIÓN DE aloTPH EN CR1:")
    for linea in r.indicacion_tph_cr1.split("\n"):
        print(f"    {linea}")

    if r.dianas_terapeuticas:
        print(f"\n  DIANAS TERAPÉUTICAS:")
        for d in r.dianas_terapeuticas:
            print(f"    → {d}")

    if r.recomendacion_inhibidores:
        print(f"\n  INHIBIDORES RECOMENDADOS:")
        for rec in r.recomendacion_inhibidores:
            print(f"    • {rec}")

    print(f"\n  MONITORIZACIÓN DE ERM:")
    for m in r.marcadores_erm:
        print(f"    • {m}")
    print(sep + "\n")


# ── Casos de demostración ─────────────────────────────────────────────────────

CASOS_DEMO = [
    PerfilLMA(
        nombre_caso="CBF-LMA — t(8;21)",
        t_8_21=True, blastos_mo=42, edad=45, sexo='M',
    ),
    PerfilLMA(
        nombre_caso="LMA NPM1mut / FLT3-ITD ratio bajo",
        npm1_mut=True, flt3_itd=True, flt3_itd_ratio=0.3,
        dnmt3a_r882=True, idh2_mut=True,
        blastos_mo=68, edad=52, sexo='F',
    ),
    PerfilLMA(
        nombre_caso="LMA FLT3-ITD / NPM1wt — riesgo adverso",
        flt3_itd=True, flt3_itd_ratio=1.4, npm1_mut=False,
        dnmt3a_r882=True, blastos_mo=55, edad=61, sexo='M',
    ),
    PerfilLMA(
        nombre_caso="LMA TP53 bialélico — cariotipo complejo",
        tp53_mut=True, cariotipo_complejo=True, cariotipo_monosomal=True,
        monosomia_5=True, monosomia_7=True,
        blastos_mo=38, edad=70, sexo='M',
        lma_terapia=True,
    ),
    PerfilLMA(
        nombre_caso="LPA — PML::RARA",
        es_lpa=True, t_15_17=True,
        blastos_mo=90, edad=38, sexo='F',
    ),
]


if __name__ == "__main__":
    print("=" * 65)
    print("  EJERCICIO 2.2 — Clasificador ELN 2022 para LMA")
    print("  Hematología con Claude Code | Nivel 2")
    print("=" * 65)

    for caso in CASOS_DEMO:
        resultado = clasificar_eln_2022(caso)
        imprimir_resultado_eln(caso, resultado)
