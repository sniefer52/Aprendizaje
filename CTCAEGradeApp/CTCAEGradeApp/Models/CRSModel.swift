import Foundation

// ASTCT 2019 Consensus Grading for CRS
struct CRSAssessment: Identifiable, Codable {
    var id: UUID = UUID()
    var date: Date = Date()
    var hasFever: Bool = false
    var temperature: Double = 37.0
    var hypotensionLevel: HypotensionLevel = .none
    var hypoxiaLevel: HypoxiaLevel = .none
    var organToxicity: OrganToxicityLevel = .none

    enum HypotensionLevel: String, CaseIterable, Codable {
        case none = "Sin hipotensión"
        case fluidResponsive = "Responde a fluidos (sin vasopresores)"
        case oneVasopressor = "Requiere 1 vasopresor (± vasopresina)"
        case multipleVasopressors = "Requiere múltiples vasopresores (excluyendo vasopresina)"

        var grade: Int {
            switch self {
            case .none: return 0
            case .fluidResponsive: return 2
            case .oneVasopressor: return 3
            case .multipleVasopressors: return 4
            }
        }
    }

    enum HypoxiaLevel: String, CaseIterable, Codable {
        case none = "Sin hipoxia"
        case lowFlowNasal = "Baja concentración O₂ (<6L cánula nasal / <40% FiO₂)"
        case highFlowOrMask = "Alta concentración O₂ (≥6L cánula nasal / ≥40% FiO₂)"
        case positivePressure = "Ventilación con presión positiva (CPAP, BiPAP, intubación)"

        var grade: Int {
            switch self {
            case .none: return 0
            case .lowFlowNasal: return 2
            case .highFlowOrMask: return 3
            case .positivePressure: return 4
            }
        }
    }

    enum OrganToxicityLevel: String, CaseIterable, Codable {
        case none = "Sin toxicidad orgánica"
        case grade2 = "Toxicidad orgánica Grado 2"
        case grade3 = "Toxicidad orgánica Grado 3 / Toxicidad cardiaca Grado 3"
        case grade4 = "Toxicidad orgánica Grado 4 o toxicidad cardiaca Grado 4"

        var grade: Int {
            switch self {
            case .none: return 0
            case .grade2: return 2
            case .grade3: return 3
            case .grade4: return 4
            }
        }
    }

    var computedGrade: CRSGrade {
        guard hasFever && temperature >= 38.0 else { return .grade0 }

        let maxGrade = max(
            hypotensionLevel.grade,
            hypoxiaLevel.grade,
            organToxicity.grade
        )

        switch maxGrade {
        case 0: return .grade1
        case 2: return .grade2
        case 3: return .grade3
        case 4: return .grade4
        default: return .grade1
        }
    }
}

enum CRSGrade: Int, Comparable {
    case grade0 = 0
    case grade1 = 1
    case grade2 = 2
    case grade3 = 3
    case grade4 = 4
    case grade5 = 5

    static func < (lhs: CRSGrade, rhs: CRSGrade) -> Bool {
        lhs.rawValue < rhs.rawValue
    }

    var displayName: String {
        switch self {
        case .grade0: return "Grado 0"
        case .grade1: return "Grado 1"
        case .grade2: return "Grado 2"
        case .grade3: return "Grado 3"
        case .grade4: return "Grado 4"
        case .grade5: return "Grado 5"
        }
    }

    var description: String {
        switch self {
        case .grade0: return "Sin fiebre ≥38°C ni síntomas de SLC"
        case .grade1: return "Fiebre ≥38°C, sin hipotensión ni hipoxia"
        case .grade2: return "Fiebre ≥38°C con hipotensión que responde a fluidos o hipoxia que requiere O₂ bajo flujo"
        case .grade3: return "Fiebre ≥38°C con hipotensión que requiere vasopresor o hipoxia con O₂ alto flujo"
        case .grade4: return "Fiebre ≥38°C con hipotensión que requiere múltiples vasopresores o ventilación con presión positiva"
        case .grade5: return "Muerte"
        }
    }

    var management: [String] {
        switch self {
        case .grade0:
            return ["Monitorización de rutina"]
        case .grade1:
            return [
                "Antipiréticos (paracetamol)",
                "Monitorización de signos vitales",
                "Hidratación según necesidad",
                "Monitorización ambulatoria posible si clínicamente estable"
            ]
        case .grade2:
            return [
                "Antipiréticos y fluidos IV",
                "Ingreso hospitalario",
                "Monitorización contínua de signos vitales",
                "Considerar Tocilizumab 8mg/kg IV (máx 800mg)",
                "Considerar corticosteroides si no responde a Tocilizumab",
                "O₂ suplementario según necesidad"
            ]
        case .grade3:
            return [
                "Ingreso en UCI o unidad de monitorización intensiva",
                "Tocilizumab 8mg/kg IV (máx 800mg) — puede repetirse a las 8h si no responde",
                "Dexametasona 10mg IV cada 6h (o metilprednisolona 1mg/kg cada 12h)",
                "Vasopresores según protocolo de sepsis",
                "O₂ alto flujo / soporte ventilatorio según necesidad",
                "Monitorización de función orgánica (renal, hepática, cardíaca)",
                "Evitar nuevas infusiones de células T"
            ]
        case .grade4:
            return [
                "UCI — soporte vital intensivo",
                "Tocilizumab 8mg/kg IV — puede repetirse",
                "Metilprednisolona 2mg/kg/día o dexametasona 20mg IV cada 6h",
                "Soporte vasopresor múltiple",
                "Ventilación mecánica invasiva si indicada",
                "Valorar siltuximab si refractario a Tocilizumab",
                "Suspender terapia con células T",
                "Consultar hematooncología de guardia"
            ]
        case .grade5:
            return ["Soporte y cuidados paliativos según deseos del paciente y familia"]
        }
    }

    var colorName: String {
        switch self {
        case .grade0: return "gradeGreen"
        case .grade1: return "gradeYellow"
        case .grade2: return "gradeOrange"
        case .grade3: return "gradeRed"
        case .grade4: return "gradePurple"
        case .grade5: return "gradeBlack"
        }
    }

    var urgencyLevel: String {
        switch self {
        case .grade0: return "Rutina"
        case .grade1: return "Vigilancia"
        case .grade2: return "Ingreso"
        case .grade3: return "UCI"
        case .grade4: return "UCI — Crítico"
        case .grade5: return "—"
        }
    }
}
