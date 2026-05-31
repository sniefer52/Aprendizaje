"""
Ejercicio 3.1 — Parser de VCF para Panel ELN/Hematología
Nivel 3 | Hematología con Claude Code

Lee un archivo VCF con variantes somáticas y:
  • Extrae: gen, variante, VAF y profundidad de cobertura
  • Filtra por genes del panel ELN 2022 / paneles de leucemia
  • Clasifica según relevancia clínica
  • Genera informe en texto estructurado

El script puede:
  A) Procesar un VCF real (argumento --vcf archivo.vcf)
  B) Generar un VCF simulado de demostración (por defecto)
"""

import re
import sys
import csv
import json
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Optional
from datetime import date


# ── Panel de genes hematológicos relevantes ───────────────────────────────────

PANEL_ELN_2022_LMA = {
    # Gen: (relevancia_clinica, categoria_eln, diana_terapeutica)
    "NPM1":    ("muy_alta", "favorable",   None),
    "CEBPA":   ("muy_alta", "favorable",   None),
    "FLT3":    ("muy_alta", "intermedio",  "midostaurina / quizartinib"),
    "DNMT3A":  ("alta",     "intermedio",  None),
    "IDH1":    ("alta",     "intermedio",  "ivosidenib"),
    "IDH2":    ("alta",     "intermedio",  "enasidenib"),
    "TET2":    ("alta",     "intermedio",  None),
    "TP53":    ("muy_alta", "adverso",     None),
    "RUNX1":   ("alta",     "adverso",     None),
    "ASXL1":   ("alta",     "adverso",     None),
    "EZH2":    ("alta",     "adverso",     None),
    "SF3B1":   ("alta",     "adverso",     None),
    "SRSF2":   ("alta",     "adverso",     None),
    "STAG2":   ("alta",     "adverso",     None),
    "BCOR":    ("alta",     "adverso",     None),
    "KIT":     ("media",    "intermedio",  "imatinib / dasatinib (CBF)"),
    "NRAS":    ("media",    "intermedio",  None),
    "KRAS":    ("media",    "intermedio",  None),
    "WT1":     ("media",    "variable",    None),
    "PTPN11":  ("media",    "variable",    None),
}

PANEL_LINFOMA = {
    "MYD88":  ("muy_alta", "adverso_DLBCL_ABC",  "ibrutinib"),
    "CD79B":  ("alta",     "intermedio",          "ibrutinib"),
    "EZH2":   ("alta",     "favorable_FL",        "tazemetostat"),
    "TP53":   ("muy_alta", "adverso",             None),
    "CREBBP": ("media",    "adverso_FL",          None),
    "BCL2":   ("alta",     "variable",            "venetoclax"),
    "BCL6":   ("alta",     "variable",            None),
    "MYC":    ("muy_alta", "adverso",             None),
    "BTK":    ("alta",     "resistencia_ITK",     None),
}

PANEL_MIELOMA = {
    "TP53":   ("muy_alta", "adverso", None),
    "RB1":    ("alta",     "adverso", None),
    "FAM46C": ("media",    "variable", None),
    "DIS3":   ("media",    "variable", None),
    "BRAF":   ("alta",     "diana",    "vemurafenib"),
    "KRAS":   ("media",    "variable", None),
    "NRAS":   ("media",    "variable", None),
}

PANELES = {
    "LMA": PANEL_ELN_2022_LMA,
    "LINFOMA": PANEL_LINFOMA,
    "MIELOMA": PANEL_MIELOMA,
}


# ── Estructura de datos ───────────────────────────────────────────────────────

@dataclass
class Variante:
    cromosoma: str
    posicion: int
    ref: str
    alt: str
    gen: str
    efecto: str
    hgvs_c: str
    hgvs_p: str
    vaf: float            # Variant Allele Frequency (%)
    profundidad: int      # Total reads en esa posición
    reads_alt: int        # Reads con el alelo alternativo
    filtro: str           # PASS / LowQual / etc.
    relevancia: str = "desconocida"
    categoria_eln: str = ""
    diana_terapeutica: Optional[str] = None
    en_panel: bool = False


# ── Parser de VCF ────────────────────────────────────────────────────────────

def parsear_vcf(ruta: str, panel: dict) -> list[Variante]:
    variantes = []
    with open(ruta, 'r') as f:
        for linea in f:
            if linea.startswith('#'):
                continue
            campos = linea.strip().split('\t')
            if len(campos) < 8:
                continue

            chrom, pos, id_, ref, alt, qual, filtro, info = campos[:8]
            formato = campos[8] if len(campos) > 8 else ""
            muestra  = campos[9] if len(campos) > 9 else ""

            # Extraer VAF y profundidad del campo FORMAT/SAMPLE
            vaf, profundidad, reads_alt = _extraer_metricas(formato, muestra, info)

            # Extraer anotación del campo INFO (formato VEP/SnpEff/ANNOVAR)
            gen, efecto, hgvs_c, hgvs_p = _extraer_anotacion(info)

            v = Variante(
                cromosoma=chrom, posicion=int(pos),
                ref=ref, alt=alt, gen=gen, efecto=efecto,
                hgvs_c=hgvs_c, hgvs_p=hgvs_p,
                vaf=vaf, profundidad=profundidad, reads_alt=reads_alt,
                filtro=filtro,
            )

            # Anotar con el panel
            if gen in panel:
                rel, cat, diana = panel[gen]
                v.relevancia = rel
                v.categoria_eln = cat
                v.diana_terapeutica = diana
                v.en_panel = True

            variantes.append(v)

    return variantes


def _extraer_metricas(formato: str, muestra: str, info: str) -> tuple[float, int, int]:
    """Intenta extraer VAF, profundidad y reads_alt de campos FORMAT/SAMPLE."""
    vaf, profundidad, reads_alt = 0.0, 0, 0
    try:
        fmt_campos = formato.split(':')
        smp_valores = muestra.split(':')
        fmt_dict = dict(zip(fmt_campos, smp_valores))

        # AD (allelic depths): ref_reads,alt_reads
        if 'AD' in fmt_dict:
            ad = fmt_dict['AD'].split(',')
            if len(ad) >= 2:
                ref_r, alt_r = int(ad[0]), int(ad[1])
                reads_alt = alt_r
                total = ref_r + alt_r
                profundidad = total
                vaf = round(alt_r / total * 100, 2) if total > 0 else 0.0

        # DP: profundidad total
        if 'DP' in fmt_dict and profundidad == 0:
            profundidad = int(fmt_dict['DP'])

        # AF: algunos callers lo incluyen directamente
        if 'AF' in fmt_dict and vaf == 0.0:
            vaf = round(float(fmt_dict['AF']) * 100, 2)

        # VCF de Mutect2: incluye AF en el campo SAMPLE
        if 'AF' in fmt_dict:
            vaf = round(float(fmt_dict['AF']) * 100, 2)

    except (ValueError, IndexError, ZeroDivisionError):
        pass

    # Último recurso: buscar AF= en INFO
    if vaf == 0.0:
        m = re.search(r'AF=([0-9.]+)', info)
        if m:
            vaf = round(float(m.group(1)) * 100, 2)

    return vaf, profundidad, reads_alt


def _extraer_anotacion(info: str) -> tuple[str, str, str, str]:
    """Extrae gen/efecto/HGVS del campo INFO (formato VEP CSQ o ANN SnpEff)."""
    gen, efecto, hgvs_c, hgvs_p = "DESCONOCIDO", ".", ".", "."

    # Formato VEP: CSQ=A|efecto|...|gen|...|hgvs_c|hgvs_p|...
    m_vep = re.search(r'CSQ=([^;]+)', info)
    if m_vep:
        bloques = m_vep.group(1).split(',')
        if bloques:
            campos = bloques[0].split('|')
            if len(campos) > 6:
                gen    = campos[3] if len(campos) > 3 else gen
                efecto = campos[1] if len(campos) > 1 else efecto
                hgvs_c = campos[10] if len(campos) > 10 else "."
                hgvs_p = campos[11] if len(campos) > 11 else "."

    # Formato SnpEff: ANN=A|efecto|impacto|gen|...
    m_ann = re.search(r'ANN=([^;]+)', info)
    if m_ann and gen == "DESCONOCIDO":
        campos = m_ann.group(1).split('|')
        if len(campos) > 3:
            efecto = campos[1]
            gen    = campos[3]

    # Formato simplificado GENE=...; EFFECT=...; HGVSc=...; HGVSp=...
    for tag, var in [("GENE", "gen"), ("EFFECT", "efecto"),
                     ("HGVSc", "hgvs_c"), ("HGVSp", "hgvs_p")]:
        m = re.search(rf'{tag}=([^;]+)', info)
        if m:
            locals()[var]  # referencia para que no se optimice
            if tag == "GENE":   gen    = m.group(1)
            if tag == "EFFECT": efecto = m.group(1)
            if tag == "HGVSc":  hgvs_c = m.group(1)
            if tag == "HGVSp":  hgvs_p = m.group(1)

    return gen, efecto, hgvs_c, hgvs_p


# ── Filtrado y clasificación ──────────────────────────────────────────────────

def filtrar_variantes(variantes: list[Variante],
                      vaf_min: float = 3.0,
                      profundidad_min: int = 50,
                      solo_panel: bool = False) -> list[Variante]:
    filtradas = [
        v for v in variantes
        if v.vaf >= vaf_min
        and v.profundidad >= profundidad_min
        and v.filtro in ("PASS", ".", "")
    ]
    if solo_panel:
        filtradas = [v for v in filtradas if v.en_panel]
    return filtradas


# ── Informe ───────────────────────────────────────────────────────────────────

def generar_informe(variantes: list[Variante], tipo_panel: str,
                    ruta_salida: str = "informe_ngs.txt") -> str:
    lineas = []
    sep = "─" * 70

    lineas.append("═" * 70)
    lineas.append(f"  INFORME NGS — PANEL {tipo_panel}")
    lineas.append(f"  Fecha: {date.today().isoformat()}")
    lineas.append(f"  Variantes analizadas: {len(variantes)}")
    lineas.append("═" * 70)

    # Agrupar por relevancia
    grupos = {
        "muy_alta": [v for v in variantes if v.relevancia == "muy_alta"],
        "alta":     [v for v in variantes if v.relevancia == "alta"],
        "media":    [v for v in variantes if v.relevancia == "media"],
        "desconocida": [v for v in variantes if v.relevancia == "desconocida"],
    }

    for nivel, etiqueta in [("muy_alta",    "VARIANTES DE MUY ALTA RELEVANCIA CLÍNICA"),
                              ("alta",       "VARIANTES DE ALTA RELEVANCIA CLÍNICA"),
                              ("media",      "VARIANTES DE RELEVANCIA MEDIA"),
                              ("desconocida","VARIANTES FUERA DE PANEL")]:
        grupo = grupos[nivel]
        if not grupo:
            continue
        lineas.append(f"\n{sep}")
        lineas.append(f"  {etiqueta} ({len(grupo)})")
        lineas.append(sep)

        for v in sorted(grupo, key=lambda x: -x.vaf):
            lineas.append(f"\n  GEN: {v.gen}")
            lineas.append(f"    Variante    : {v.ref}>{v.alt} en {v.cromosoma}:{v.posicion}")
            if v.hgvs_c != ".":
                lineas.append(f"    HGVSc       : {v.hgvs_c}")
            if v.hgvs_p != ".":
                lineas.append(f"    HGVSp       : {v.hgvs_p}")
            lineas.append(f"    VAF         : {v.vaf}%  "
                          f"({v.reads_alt}/{v.profundidad} reads)")
            lineas.append(f"    Efecto      : {v.efecto}")
            if v.categoria_eln:
                lineas.append(f"    Categoría   : {v.categoria_eln}")
            if v.diana_terapeutica:
                lineas.append(f"    Diana tx    : ⚑ {v.diana_terapeutica}")

    # Resumen de dianas
    dianas = [v for v in variantes if v.diana_terapeutica]
    if dianas:
        lineas.append(f"\n{sep}")
        lineas.append("  RESUMEN DE DIANAS TERAPÉUTICAS")
        lineas.append(sep)
        for v in dianas:
            lineas.append(f"    {v.gen} (VAF {v.vaf}%) → {v.diana_terapeutica}")

    lineas.append(f"\n{'═' * 70}")
    lineas.append("  NOTA: Informe generado con fines educativos.")
    lineas.append("  Toda interpretación clínica requiere validación por especialista.")
    lineas.append("═" * 70 + "\n")

    texto = "\n".join(lineas)
    with open(ruta_salida, 'w') as f:
        f.write(texto)
    return texto


# ── Generador de VCF simulado ─────────────────────────────────────────────────

VCF_SIMULADO_CONTENIDO = """\
##fileformat=VCFv4.2
##source=Mutect2-simulado-educativo
##FILTER=<ID=PASS,Description="Passed all filters">
##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">
##FORMAT=<ID=AD,Number=R,Type=Integer,Description="Allelic depths">
##FORMAT=<ID=AF,Number=A,Type=Float,Description="Allele fractions">
##FORMAT=<ID=DP,Number=1,Type=Integer,Description="Approximate read depth">
#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tTUMOR
chr5\t170837543\t.\tC\tCATG\t.\tPASS\tGENE=NPM1;EFFECT=frameshift_variant;HGVSc=c.863_864insCATG;HGVSp=p.W288Cfs*12\tGT:AD:AF:DP\t0/1:52,48:0.48:100
chr13\t28608310\t.\tA\tT\t.\tPASS\tGENE=FLT3;EFFECT=internal_tandem_duplication;HGVSc=c.1770_1771insTTGATTCACATTATGATTTTGGTTTTGTTGTTTT;HGVSp=p.Y590_D591insITAVWFW\tGT:AD:AF:DP\t0/1:62,58:0.48:120
chr2\t25463483\t.\tG\tA\t.\tPASS\tGENE=DNMT3A;EFFECT=missense_variant;HGVSc=c.2644C>T;HGVSp=p.R882C\tGT:AD:AF:DP\t0/1:58,54:0.48:112
chr17\t7674247\t.\tC\tT\t.\tPASS\tGENE=TP53;EFFECT=missense_variant;HGVSc=c.818G>A;HGVSp=p.R273H\tGT:AD:AF:DP\t0/1:82,18:0.18:100
chr4\t55592179\t.\tC\tT\t.\tPASS\tGENE=IDH2;EFFECT=missense_variant;HGVSc=c.419G>A;HGVSp=p.R140Q\tGT:AD:AF:DP\t0/1:54,46:0.46:100
chr1\t11322965\t.\tG\tA\t.\tPASS\tGENE=ASXL1;EFFECT=frameshift_variant;HGVSc=c.1934dupG;HGVSp=p.G646Wfs*12\tGT:AD:AF:DP\t0/1:65,5:0.07:70
chr9\t107542222\t.\tA\tG\t.\tPASS\tGENE=DESCONOCIDO_XYZ;EFFECT=synonymous_variant;HGVSc=c.123A>G;HGVSp=p.K41K\tGT:AD:AF:DP\t0/1:195,5:0.025:200
"""


def crear_vcf_demo(ruta: str = "demo_leucemia.vcf") -> str:
    with open(ruta, 'w') as f:
        f.write(VCF_SIMULADO_CONTENIDO)
    return ruta


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 70)
    print("  EJERCICIO 3.1 — Parser VCF para Panel Hematológico")
    print("  Hematología con Claude Code | Nivel 3")
    print("=" * 70)

    # Determinar ruta VCF
    if "--vcf" in sys.argv:
        idx = sys.argv.index("--vcf")
        ruta_vcf = sys.argv[idx + 1]
    else:
        print("\n  Usando VCF de demostración (simulado — no datos reales)...")
        ruta_vcf = crear_vcf_demo()

    # Determinar panel
    tipo_panel = "LMA"
    if "--panel" in sys.argv:
        idx = sys.argv.index("--panel")
        tipo_panel = sys.argv[idx + 1].upper()
    panel = PANELES.get(tipo_panel, PANEL_ELN_2022_LMA)

    print(f"  Panel: {tipo_panel} ({len(panel)} genes)")
    print(f"  VCF  : {ruta_vcf}\n")

    # Parsear
    variantes_raw = parsear_vcf(ruta_vcf, panel)
    print(f"  Variantes en el VCF: {len(variantes_raw)}")

    # Filtrar
    variantes_filtradas = filtrar_variantes(variantes_raw, vaf_min=3.0,
                                            profundidad_min=30)
    print(f"  Variantes tras filtrado (VAF≥3%, DP≥30, PASS): {len(variantes_filtradas)}")

    en_panel = [v for v in variantes_filtradas if v.en_panel]
    print(f"  En panel {tipo_panel}: {len(en_panel)}")

    # Generar informe
    informe = generar_informe(variantes_filtradas, tipo_panel)
    print("\n" + informe)

    # Exportar a CSV
    csv_salida = "variantes_filtradas.csv"
    with open(csv_salida, 'w', newline='') as f:
        campos = ["gen", "cromosoma", "posicion", "ref", "alt", "hgvs_p",
                  "vaf", "profundidad", "relevancia", "categoria_eln",
                  "diana_terapeutica", "filtro"]
        w = csv.DictWriter(f, fieldnames=campos, extrasaction='ignore')
        w.writeheader()
        for v in variantes_filtradas:
            w.writerow(asdict(v))
    print(f"  CSV exportado: {csv_salida}")
