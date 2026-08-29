import SwiftUI

struct CRSWizardView: View {
    @EnvironmentObject var store: AssessmentStore
    @State private var assessment = CRSAssessment()
    @State private var showResult = false

    var body: some View {
        NavigationStack {
            Form {
                // Section 1: Fever
                Section {
                    VStack(alignment: .leading, spacing: 12) {
                        Label("¿Tiene fiebre ≥ 38°C?", systemImage: "thermometer.high")
                            .font(.headline)

                        Picker("Fiebre", selection: $assessment.hasFever) {
                            Text("No").tag(false)
                            Text("Sí").tag(true)
                        }
                        .pickerStyle(.segmented)

                        if assessment.hasFever {
                            HStack {
                                Text("Temperatura")
                                Spacer()
                                Text(String(format: "%.1f °C", assessment.temperature))
                                    .monospacedDigit()
                            }
                            Slider(
                                value: $assessment.temperature,
                                in: 36.0...42.0,
                                step: 0.1
                            )
                            .tint(assessment.temperature >= 38.0 ? .orange : .green)
                        }
                    }
                } header: {
                    Text("Paso 1 — Fiebre")
                } footer: {
                    Text("La fiebre ≥38°C es criterio obligatorio para diagnóstico de SLC.")
                }

                if assessment.hasFever && assessment.temperature >= 38.0 {
                    // Section 2: Hypotension
                    Section {
                        VStack(alignment: .leading, spacing: 8) {
                            Label("Estado hemodinámico", systemImage: "waveform.path.ecg")
                                .font(.headline)
                            Text("Seleccione el nivel más grave observado")
                                .font(.caption)
                                .foregroundStyle(.secondary)
                        }

                        ForEach(CRSAssessment.HypotensionLevel.allCases, id: \.self) { level in
                            SelectionRow(
                                title: level.rawValue,
                                isSelected: assessment.hypotensionLevel == level,
                                badge: level == .none ? nil : "G\(level.grade)"
                            ) {
                                assessment.hypotensionLevel = level
                            }
                        }
                    } header: {
                        Text("Paso 2 — Hipotensión")
                    }

                    // Section 3: Hypoxia
                    Section {
                        VStack(alignment: .leading, spacing: 8) {
                            Label("Estado respiratorio / oxigenación", systemImage: "lungs.fill")
                                .font(.headline)
                            Text("Seleccione el soporte de O₂ requerido")
                                .font(.caption)
                                .foregroundStyle(.secondary)
                        }

                        ForEach(CRSAssessment.HypoxiaLevel.allCases, id: \.self) { level in
                            SelectionRow(
                                title: level.rawValue,
                                isSelected: assessment.hypoxiaLevel == level,
                                badge: level == .none ? nil : "G\(level.grade)"
                            ) {
                                assessment.hypoxiaLevel = level
                            }
                        }
                    } header: {
                        Text("Paso 3 — Hipoxia")
                    }

                    // Section 4: Organ Toxicity
                    Section {
                        VStack(alignment: .leading, spacing: 8) {
                            Label("Toxicidad orgánica (CTCAE)", systemImage: "heart.text.square.fill")
                                .font(.headline)
                            Text("Incluye toxicidad cardiaca, hepática, renal u otras")
                                .font(.caption)
                                .foregroundStyle(.secondary)
                        }

                        ForEach(CRSAssessment.OrganToxicityLevel.allCases, id: \.self) { level in
                            SelectionRow(
                                title: level.rawValue,
                                isSelected: assessment.organToxicity == level,
                                badge: level == .none ? nil : "G\(level.grade)"
                            ) {
                                assessment.organToxicity = level
                            }
                        }
                    } header: {
                        Text("Paso 4 — Toxicidad Orgánica")
                    }

                    // Result preview
                    Section {
                        GradePreviewRow(
                            syndrome: "SLC / CRS",
                            grade: assessment.computedGrade.displayName,
                            urgency: assessment.computedGrade.urgencyLevel,
                            colorName: assessment.computedGrade.colorName
                        )
                    } header: {
                        Text("Grado Calculado")
                    }
                }
            }
            .navigationTitle("Evaluación SLC / CRS")
            .toolbar {
                if assessment.hasFever && assessment.temperature >= 38.0 {
                    ToolbarItem(placement: .confirmationAction) {
                        Button("Ver Resultado") {
                            showResult = true
                        }
                        .fontWeight(.semibold)
                    }
                }
                ToolbarItem(placement: .cancellationAction) {
                    Button("Limpiar") {
                        assessment = CRSAssessment()
                    }
                    .foregroundStyle(.red)
                }
            }
            .sheet(isPresented: $showResult) {
                CRSResultView(assessment: assessment) {
                    store.addCRS(assessment)
                    assessment = CRSAssessment()
                    showResult = false
                }
            }
        }
    }
}

struct SelectionRow: View {
    let title: String
    let isSelected: Bool
    let badge: String?
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            HStack {
                Image(systemName: isSelected ? "checkmark.circle.fill" : "circle")
                    .foregroundStyle(isSelected ? .blue : .secondary)
                    .font(.title3)

                Text(title)
                    .foregroundStyle(.primary)
                    .font(.subheadline)
                    .multilineTextAlignment(.leading)

                Spacer()

                if let badge {
                    Text(badge)
                        .font(.caption.bold())
                        .foregroundStyle(.white)
                        .padding(.horizontal, 8)
                        .padding(.vertical, 3)
                        .background(gradeColor(badge))
                        .clipShape(Capsule())
                }
            }
        }
        .buttonStyle(.plain)
    }

    private func gradeColor(_ badge: String) -> Color {
        switch badge {
        case "G1": return .yellow
        case "G2": return .orange
        case "G3": return .red
        case "G4": return .purple
        default: return .gray
        }
    }
}

struct GradePreviewRow: View {
    let syndrome: String
    let grade: String
    let urgency: String
    let colorName: String

    var body: some View {
        HStack {
            VStack(alignment: .leading, spacing: 4) {
                Text(syndrome)
                    .font(.caption)
                    .foregroundStyle(.secondary)
                Text(grade)
                    .font(.title2.bold())
                    .foregroundStyle(gradeColor)
            }
            Spacer()
            VStack(alignment: .trailing, spacing: 4) {
                Text("Nivel de urgencia")
                    .font(.caption2)
                    .foregroundStyle(.secondary)
                Text(urgency)
                    .font(.subheadline.bold())
                    .foregroundStyle(gradeColor)
            }
        }
        .padding(.vertical, 4)
    }

    private var gradeColor: Color {
        switch colorName {
        case "gradeGreen": return .green
        case "gradeYellow": return .yellow
        case "gradeOrange": return .orange
        case "gradeRed": return .red
        case "gradePurple": return .purple
        case "gradeBlack": return .primary
        default: return .primary
        }
    }
}
