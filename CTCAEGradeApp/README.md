# CTCAE Grader — iOS App

Aplicación iOS para evaluación clínica rápida del **Síndrome de Liberación de Citocinas (SLC/CRS)** e **ICANS** según criterios CTCAE/ASTCT 2019.

## Requisitos

- Xcode 16+
- iOS 17.0+ (optimizada para iOS 26)
- Swift 6.0

## Apertura del proyecto

```
open CTCAEGradeApp.xcodeproj
```

## Estructura del proyecto

```
CTCAEGradeApp/
├── CTCAEGradeApp.swift          # App entry point
├── Info.plist
├── Assets.xcassets/
├── Models/
│   ├── CRSModel.swift           # Modelo y lógica de graduación SLC/CRS
│   ├── ICANSModel.swift         # Modelo y lógica de graduación ICANS
│   └── AssessmentStore.swift    # Persistencia en UserDefaults
└── Views/
    ├── ContentView.swift         # TabView principal
    ├── HomeView.swift            # Pantalla de inicio
    ├── CRSWizardView.swift       # Asistente de evaluación CRS
    ├── ICANSWizardView.swift     # Asistente de evaluación ICANS
    ├── CRSResultView.swift       # Resultado y manejo CRS
    ├── ICANSResultView.swift     # Resultado y manejo ICANS
    └── HistoryView.swift         # Historial de evaluaciones
```

## Criterios de Graduación

### SLC / CRS — ASTCT 2019
| Grado | Criterios |
|-------|-----------|
| 1 | Fiebre ≥38°C, sin hipotensión ni hipoxia |
| 2 | Hipotensión que responde a fluidos **O** hipoxia con O₂ bajo flujo |
| 3 | Hipotensión con vasopresor **O** hipoxia O₂ alto flujo |
| 4 | Múltiples vasopresores **O** ventilación con presión positiva |

### ICANS — ASTCT 2019 (Escala ICE 0–10)
| Grado | ICE Score | Nivel de Consciencia | Otras |
|-------|-----------|---------------------|-------|
| 1 | 7–9 | Espontáneo | — |
| 2 | 3–6 | Despierta a la voz | — |
| 3 | 0–2 | Solo al estímulo táctil | Convulsiones / signos focales |
| 4 | 0 | No responde | Edema cerebral / estado epiléptico |

**Escala ICE:** Orientación (4) + Nominación (3) + Órdenes (3) + Escritura (1) + Atención (1) = 10

## Referencias

- Lee DW, et al. *ASTCT Consensus Grading for Cytokine Release Syndrome.* Biol Blood Marrow Transplant. 2019
- Santomasso BD, et al. *ASTCT Consensus Grading for Neurologic Toxicity.* Biol Blood Marrow Transplant. 2019
- NCI CTCAE v5.0 — Common Terminology Criteria for Adverse Events

---
> **Aviso:** Herramienta de apoyo clínico. El diagnóstico y tratamiento son responsabilidad del profesional médico.
