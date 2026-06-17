import SwiftUI

struct ICANSResultView: View {
    let assessment: ICANSAssessment
    let onSave: () -> Void

    @Environment(\.dismiss) private var dismiss

    var grade: ICANSGrade { assessment.computedGrade }

    var body: some View {
        NavigationStack {
            ScrollView {
                VStack(spacing: 20) {
                    // Grade Badge
                    GradeBadgeView(
                        syndrome: "NEUROTOXICIDAD ASOCIADA A CÉLULAS INMUNES",
                        acronym: "ICANS",
                        grade: grade.displayName,
                        colorName: grade.colorName
                    )

                    // ICE Score detail
                    ResultSectionCard(title: "Puntuación ICE", icon: "brain.fill") {
                        VStack(spacing: 12) {
                            HStack {
                                Text("Total")
                                    .font(.subheadline)
                                    .foregroundStyle(.secondary)
                                Spacer()
                                Text("\(assessment.iceScore) / 10")
                                    .font(.title2.bold().monospacedDigit())
                                    .foregroundStyle(iceScoreColor)
                            }

                            Divider()

                            ICEBreakdownRow(label: "Orientación", score: assessment.orientationScore, max: 4)
                            ICEBreakdownRow(label: "Nominación de objetos", score: assessment.namingScore, max: 3)
                            ICEBreakdownRow(label: "Seguimiento de órdenes", score: assessment.commandsScore, max: 3)
                            ICEBreakdownRow(label: "Escritura", score: assessment.writingScore, max: 1)
                            ICEBreakdownRow(label: "Atención", score: assessment.attentionScore, max: 1)
                        }
                    }

                    // Clinical findings
                    ResultSectionCard(title: "Hallazgos Neurológicos", icon: "list.clipboard.fill") {
                        VStack(alignment: .leading, spacing: 8) {
                            FindingRow(
                                label: "Nivel de consciencia",
                                value: assessment.levelOfConsciousness.rawValue,
                                isAbnormal: assessment.levelOfConsciousness != .spontaneous
                            )
                            FindingRow(
                                label: "Convulsiones",
                                value: assessment.seizureType.rawValue,
                                isAbnormal: assessment.seizureType != .none
                            )
                            FindingRow(
                                label: "Signos motores focales",
                                value: assessment.hasFocalMotorFindings ? "Presentes" : "Ausentes",
                                isAbnormal: assessment.hasFocalMotorFindings
                            )
                            FindingRow(
                                label: "PIC elevada / HIC",
                                value: assessment.hasElevatedICP ? "Presente" : "Ausente",
                                isAbnormal: assessment.hasElevatedICP
                            )
                            FindingRow(
                                label: "Edema cerebral difuso",
                                value: assessment.hasCerebralEdema ? "Presente (neuroimagen)" : "No evidenciado",
                                isAbnormal: assessment.hasCerebralEdema
                            )
                        }
                    }

                    // Description
                    ResultSectionCard(title: "Definición del Grado", icon: "info.circle.fill") {
                        Text(grade.description)
                            .font(.subheadline)
                    }

                    // Management
                    ResultSectionCard(title: "Manejo Recomendado", icon: "cross.case.fill", accent: .purple) {
                        VStack(alignment: .leading, spacing: 10) {
                            ForEach(Array(grade.management.enumerated()), id: \.offset) { index, item in
                                HStack(alignment: .top, spacing: 10) {
                                    Text("\(index + 1)")
                                        .font(.caption.bold())
                                        .foregroundStyle(.white)
                                        .frame(width: 22, height: 22)
                                        .background(.purple)
                                        .clipShape(Circle())
                                    Text(item)
                                        .font(.subheadline)
                                        .fixedSize(horizontal: false, vertical: true)
                                }
                            }
                        }
                    }

                    // Urgency banner
                    UrgencyBannerView(level: grade.urgencyLevel, colorName: grade.colorName)

                    // Reference
                    ReferenceFooter(text: "ASTCT Consensus Grading for ICANS • Santomasso et al., Biol Blood Marrow Transplant 2019")
                }
                .padding()
            }
            .navigationTitle("Resultado ICANS")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("Cerrar") { dismiss() }
                }
                ToolbarItem(placement: .confirmationAction) {
                    Button("Guardar") { onSave() }
                        .fontWeight(.semibold)
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
}

struct ICEBreakdownRow: View {
    let label: String
    let score: Int
    let max: Int

    var body: some View {
        HStack {
            Text(label)
                .font(.caption)
                .foregroundStyle(.secondary)
            Spacer()
            HStack(spacing: 4) {
                ForEach(0..<max, id: \.self) { i in
                    Circle()
                        .fill(i < score ? Color.blue : Color.secondary.opacity(0.3))
                        .frame(width: 10, height: 10)
                }
            }
            Text("\(score)/\(max)")
                .font(.caption.monospacedDigit())
                .foregroundStyle(.secondary)
                .frame(width: 30, alignment: .trailing)
        }
    }
}
