import Foundation

// ASTCT 2019 Consensus Grading for ICANS
struct ICANSAssessment: Identifiable, Codable {
    var id: UUID = UUID()
    var date: Date = Date()

    // ICE Score components
    var orientationScore: Int = 4       // 0-4: año, mes, ciudad, hospital
    var namingScore: Int = 3            // 0-3: 3 objetos
    var commandsScore: Int = 3          // 0-3: 3 comandos
    var writingScore: Int = 1           // 0-1: escribir frase
    var attentionScore: Int = 1         // 0-1: contar de 100 a 10 de 10 en 10

    // Additional clinical features
    var levelOfConsciousness: ConsciousnessLevel = .spontaneous
    var hasSeizure: Bool = false
    var seizureType: SeizureType = .none
    var hasFocalMotorFindings: Bool = false
    var hasElevatedICP: Bool = false
    var hasCerebralEdema: Bool = false

    enum ConsciousnessLevel: String, CaseIterable, Codable {
        case spontaneous = "Espontáneo (normal)"
        case voice = "Despierta a la voz"
        case tactile = "Despierta solo al estímulo táctil"
        case unresponsive = "No responde / coma"

        var grade: Int {
            switch self {
            case .spontaneous: return 1
            case .voice: return 2
            case .tactile: return 3
            case .unresponsive: return 4
            }
        }

        var description: String { rawValue }
    }

    enum SeizureType: String, CaseIterable, Codable {
        case none = "Sin convulsiones"
        case briefResolved = "Convulsión clínica breve, autolimitada"
        case prolonged = "Convulsión clínica prolongada o convulsiones repetidas sin recuperación entre episodios"
        case statusEpilepticus = "Estado epiléptico"

        var grade: Int {
            switch self {
            case .none: return 0
            case .briefResolved: return 3
            case .prolonged: return 3
            case .statusEpilepticus: return 4
            }
        }
    }

    var iceScore: Int {
        orientationScore + namingScore + commandsScore + writingScore + attentionScore
    }

    var iceGrade: Int {
        switch iceScore {
        case 7...10: return 1
        case 3...6: return 2
        case 0...2: return 3
        default: return 0
        }
    }

    var computedGrade: ICANSGrade {
        // Grade 4 conditions
        if iceScore == 0 && levelOfConsciousness == .unresponsive {
            return .grade4
        }
        if hasCerebralEdema || hasElevatedICP {
            return .grade4
        }
        if seizureType == .statusEpilepticus {
            return .grade4
        }

        // Grade 3 conditions
        if levelOfConsciousness == .tactile {
            return .grade3
        }
        if seizureType == .briefResolved || seizureType == .prolonged {
            return .grade3
        }
        if hasFocalMotorFindings {
            return .grade3
        }
        if iceScore <= 2 {
            return .grade3
        }

        // Grade 2 conditions
        if levelOfConsciousness == .voice {
            return .grade2
        }
        if iceScore >= 3 && iceScore <= 6 {
            return .grade2
        }

        // Grade 1 conditions
        if levelOfConsciousness == .spontaneous && iceScore >= 7 {
            return .grade1
        }

        return .grade1
    }
}

enum ICANSGrade: Int, Comparable {
    case grade0 = 0
    case grade1 = 1
    case grade2 = 2
    case grade3 = 3
    case grade4 = 4

    static func < (lhs: ICANSGrade, rhs: ICANSGrade) -> Bool {
        lhs.rawValue < rhs.rawValue
    }

    var displayName: String { "Grado \(rawValue)" }

    var description: String {
        switch self {
        case .grade0: return "Sin evidencia de ICANS"
        case .grade1: return "Puntuación ICE 7-9 o nivel de conciencia espontáneo"
        case .grade2: return "Puntuación ICE 3-6 o despertar a la voz"
        case .grade3: return "Puntuación ICE 0-2, despertar solo al tacto, convulsiones o signos motores focales"
        case .grade4: return "Paciente no responde, edema cerebral difuso, estado epiléptico o postura patológica"
        }
    }

    var management: [String] {
        switch self {
        case .grade0:
            return ["Monitorización neurológica de rutina"]
        case .grade1:
            return [
                "Evaluación neurológica frecuente con escala ICE",
                "Monitorización de signos vitales",
                "Considerar neuroimagen (TC craneal) si cambio agudo",
                "Evitar sedantes que interfieran con evaluación neurológica",
                "Levetiracetam 750mg/12h IV como profilaxis anticomicial si no está ya pautado"
            ]
        case .grade2:
            return [
                "Ingreso hospitalario con monitorización continua",
                "Dexametasona 10mg IV cada 6h",
                "EEG si sospecha de actividad epiléptica no convulsiva",
                "TC craneal urgente para descartar edema / hemorragia",
                "Consulta neurología",
                "Levetiracetam o equivalente como profilaxis",
                "Reevaluar escala ICE cada 4-6h"
            ]
        case .grade3:
            return [
                "Ingreso en UCI o unidad de monitorización intensiva",
                "Dexametasona 10mg IV cada 6h (o metilprednisolona 1mg/kg cada 12h)",
                "EEG continuo — descartar estado epiléptico no convulsivo",
                "RM craneal urgente si es posible, o TC craneal",
                "Punción lumbar si no hay contraindicación para descartar infección",
                "Si convulsiones: Lorazepam IV agudo, Levetiracetam mantenimiento",
                "Evitar Tocilizumab como tratamiento primario de ICANS",
                "Suspender infusiones adicionales de células T",
                "Consulta urgente Neurología + Hematooncología"
            ]
        case .grade4:
            return [
                "UCI — monitorización neurológica intensiva",
                "Metilprednisolona 2mg/kg IV dos veces al día o dexametasona 20mg IV cada 6h",
                "EEG continuo obligatorio",
                "RM craneal urgente / TC seriado para seguimiento del edema",
                "Si edema cerebral: manitol 0.25-1g/kg IV, hiperventilación controlada",
                "Valorar monitorización de PIC si edema refractario",
                "Manejo de convulsiones según protocolo de estado epiléptico",
                "Intubación electiva si compromiso de vía aérea",
                "Suspender toda terapia de células T",
                "Consulta urgente Neurología + UCI + Hematooncología"
            ]
        }
    }

    var colorName: String {
        switch self {
        case .grade0: return "gradeGreen"
        case .grade1: return "gradeYellow"
        case .grade2: return "gradeOrange"
        case .grade3: return "gradeRed"
        case .grade4: return "gradePurple"
        }
    }

    var urgencyLevel: String {
        switch self {
        case .grade0: return "Rutina"
        case .grade1: return "Vigilancia"
        case .grade2: return "Ingreso"
        case .grade3: return "UCI"
        case .grade4: return "UCI — Crítico"
        }
    }
}
