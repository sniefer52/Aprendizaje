import SwiftUI

struct ICANSWizardView: View {
    @EnvironmentObject var store: AssessmentStore
    @State private var assessment = ICANSAssessment()
    @State private var showResult = false

    var body: some View {
        NavigationStack {
            Form {
                // ICE Score Section
                Section {
                    VStack(alignment: .leading, spacing: 6) {
                        Label("Puntuación ICE", systemImage: "brain")
                            .font(.headline)
                        Text("Immune Effector Cell-Associated Encephalopathy Score")
                            .font(.caption)
                            .foregroundStyle(.secondary)

                        HStack {
                            Text("Total ICE:")
                                .font(.subheadline)
                            Spacer()
                            Text("\(assessment.iceScore) / 10")
                                .font(.title3.bold().monospacedDigit())
                                .foregroundStyle(iceScoreColor)
                        }
                        .padding(.top, 4)

                        ProgressView(value: Double(assessment.iceScore), total: 10.0)
                            .tint(iceScoreColor)
                    }
                    .padding(.vertical, 4)

                    // Orientation (0-4)
                    ICESubScoreRow(
                        label: "Orientación",
                        detail: "Año / Mes / Ciudad / Hospital",
                        value: $assessment.orientationScore,
                        maxValue: 4
                    )

                    // Naming (0-3)
                    ICESubScoreRow(
                        label: "Nominación de objetos",
                        detail: "Nombrar 3 objetos (ej: reloj, bolígrafo, silla)",
                        value: $assessment.namingScore,
                        maxValue: 3
                    )

                    // Following Commands (0-3)
                    ICESubScoreRow(
                        label: "Seguimiento de órdenes",
                        detail: "Mostrar 2 dedos / Cerrar ojos / Sacar lengua",
                        value: $assessment.commandsScore,
                        maxValue: 3
                    )

                    // Writing (0-1)
                    ICESubScoreRow(
                        label: "Escritura",
                        detail: "Escribir una frase estándar",
                        value: $assessment.writingScore,
                        maxValue: 1
                    )

                    // Attention (0-1)
                    ICESubScoreRow(
                        label: "Atención",
                        detail: "Contar de 100 a 10 de 10 en 10",
                        value: $assessment.attentionScore,
                        maxValue: 1
                    )
                } header: {
                    Text("Paso 1 — Escala ICE (0–10)")
                } footer: {
                    iceScorefooterText
                }

                // Level of Consciousness
                Section {
                    VStack(alignment: .leading, spacing: 8) {
                        Label("Nivel de consciencia", systemImage: "eye.fill")
                            .font(.headline)
                    }

                    ForEach(ICANSAssessment.ConsciousnessLevel.allCases, id: \.self) { level in
                        SelectionRow(
                            title: level.rawValue,
                            isSelected: assessment.levelOfConsciousness == level,
                            badge: "G\(level.grade)"
                        ) {
                            assessment.levelOfConsciousness = level
                        }
                    }
                } header: {
                    Text("Paso 2 — Nivel de Consciencia")
                }

                // Seizures
                Section {
                    VStack(alignment: .leading, spacing: 8) {
                        Label("Actividad convulsiva", systemImage: "bolt.fill")
                            .font(.headline)
                    }

                    ForEach(ICANSAssessment.SeizureType.allCases, id: \.self) { type in
                        SelectionRow(
                            title: type.rawValue,
                            isSelected: assessment.seizureType == type,
                            badge: type == .none ? nil : "G\(type.grade)"
                        ) {
                            assessment.seizureType = type
                        }
                    }
                } header: {
                    Text("Paso 3 — Convulsiones")
                }

                // Additional Findings
                Section {
                    Toggle(isOn: $assessment.hasFocalMotorFindings) {
                        VStack(alignment: .leading, spacing: 2) {
                            Label("Signos motores focales", systemImage: "figure.walk.motion")
                                .font(.subheadline)
                            Text("Hemiplejia, temblor focal, apraxia")
                                .font(.caption)
                                .foregroundStyle(.secondary)
                        }
                    }

                    Toggle(isOn: $assessment.hasElevatedICP) {
                        VStack(alignment: .leading, spacing: 2) {
                            Label("HIC / PIC elevada", systemImage: "arrow.up.circle.fill")
                                .font(.subheadline)
                            Text("Hipertensión intracraneal (papiledema, Cushing, etc.)")
                                .font(.caption)
                                .foregroundStyle(.secondary)
                        }
                    }

                    Toggle(isOn: $assessment.hasCerebralEdema) {
                        VStack(alignment: .leading, spacing: 2) {
                            Label("Edema cerebral difuso", systemImage: "brain.fill")
                                .font(.subheadline)
                            Text("Confirmado por neuroimagen (TC o RM)")
                                .font(.caption)
                                .foregroundStyle(.secondary)
                        }
                    }
                } header: {
                    Text("Paso 4 — Hallazgos Adicionales")
                } footer: {
                    Text("Signos motores focales, PIC elevada o edema cerebral difuso elevan el grado a ≥3.")
                }

                // Result preview
                Section {
                    GradePreviewRow(
                        syndrome: "ICANS",
                        grade: assessment.computedGrade.displayName,
                        urgency: assessment.computedGrade.urgencyLevel,
                        colorName: assessment.computedGrade.colorName
                    )
                } header: {
                    Text("Grado Calculado")
                }
            }
            .navigationTitle("Evaluación ICANS")
            .toolbar {
                ToolbarItem(placement: .confirmationAction) {
                    Button("Ver Resultado") {
                        showResult = true
                    }
                    .fontWeight(.semibold)
                }
                ToolbarItem(placement: .cancellationAction) {
                    Button("Limpiar") {
                        assessment = ICANSAssessment()
                    }
                    .foregroundStyle(.red)
                }
            }
            .sheet(isPresented: $showResult) {
                ICANSResultView(assessment: assessment) {
                    store.addICANS(assessment)
                    assessment = ICANSAssessment()
                    showResult = false
                }
            }
        }
    }

    private var iceScoreColor: Color {
        switch assessment.iceScore {
        case 9...10: return .green
        case 7...8: return .yellow
        case 3...6: return .orange
        default: return .red
        }
    }

    private var iceScorefooterText: Text {
        switch assessment.iceScore {
        case 9...10: return Text("Normal o casi normal (Grado 1 si hay otras manifestaciones)")
        case 7...8: return Text("ICE 7-8 → Grado 1 ICANS").foregroundColor(.yellow)
        case 3...6: return Text("ICE 3-6 → Grado 2 ICANS").foregroundColor(.orange)
        default: return Text("ICE 0-2 → Grado 3 ICANS").foregroundColor(.red)
        }
    }
}

struct ICESubScoreRow: View {
    let label: String
    let detail: String
    @Binding var value: Int
    let maxValue: Int

    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            HStack {
                VStack(alignment: .leading, spacing: 2) {
                    Text(label)
                        .font(.subheadline.bold())
                    Text(detail)
                        .font(.caption)
                        .foregroundStyle(.secondary)
                }
                Spacer()
                Text("\(value)/\(maxValue)")
                    .font(.subheadline.monospacedDigit())
                    .foregroundStyle(value == maxValue ? .green : value == 0 ? .red : .orange)
                    .frame(minWidth: 36, alignment: .trailing)
            }

            HStack(spacing: 8) {
                ForEach(0...maxValue, id: \.self) { point in
                    Button {
                        value = point
                    } label: {
                        Text("\(point)")
                            .font(.caption.bold())
                            .foregroundStyle(value == point ? .white : .primary)
                            .frame(width: 36, height: 36)
                            .background(value == point ? pointColor(point) : Color.secondary.opacity(0.15))
                            .clipShape(Circle())
                    }
                    .buttonStyle(.plain)
                }
                Spacer()
            }
        }
        .padding(.vertical, 4)
    }

    private func pointColor(_ point: Int) -> Color {
        if point == maxValue { return .green }
        if point == 0 { return .red }
        return .orange
    }
}
