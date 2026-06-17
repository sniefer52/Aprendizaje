import SwiftUI

struct CRSResultView: View {
    let assessment: CRSAssessment
    let onSave: () -> Void

    @Environment(\.dismiss) private var dismiss

    var grade: CRSGrade { assessment.computedGrade }

    var body: some View {
        NavigationStack {
            ScrollView {
                VStack(spacing: 20) {
                    // Grade Badge
                    GradeBadgeView(
                        syndrome: "SÍNDROME LIBERACIÓN CITOCINAS",
                        acronym: "SLC / CRS",
                        grade: grade.displayName,
                        colorName: grade.colorName
                    )

                    // Description
                    ResultSectionCard(title: "Definición", icon: "info.circle.fill") {
                        Text(grade.description)
                            .font(.subheadline)
                    }

                    // Clinical findings summary
                    ResultSectionCard(title: "Hallazgos Registrados", icon: "list.clipboard.fill") {
                        VStack(alignment: .leading, spacing: 8) {
                            FindingRow(
                                label: "Temperatura",
                                value: String(format: "%.1f °C", assessment.temperature),
                                isAbnormal: assessment.temperature >= 38.0
                            )
                            FindingRow(
                                label: "Hipotensión",
                                value: assessment.hypotensionLevel.rawValue,
                                isAbnormal: assessment.hypotensionLevel != .none
                            )
                            FindingRow(
                                label: "Hipoxia",
                                value: assessment.hypoxiaLevel.rawValue,
                                isAbnormal: assessment.hypoxiaLevel != .none
                            )
                            FindingRow(
                                label: "Toxicidad orgánica",
                                value: assessment.organToxicity.rawValue,
                                isAbnormal: assessment.organToxicity != .none
                            )
                        }
                    }

                    // Management
                    ResultSectionCard(title: "Manejo Recomendado", icon: "cross.case.fill", accent: .blue) {
                        VStack(alignment: .leading, spacing: 10) {
                            ForEach(Array(grade.management.enumerated()), id: \.offset) { index, item in
                                HStack(alignment: .top, spacing: 10) {
                                    Text("\(index + 1)")
                                        .font(.caption.bold())
                                        .foregroundStyle(.white)
                                        .frame(width: 22, height: 22)
                                        .background(.blue)
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
                    ReferenceFooter(text: "ASTCT Consensus Grading for CRS • Lee et al., Biol Blood Marrow Transplant 2019")
                }
                .padding()
            }
            .navigationTitle("Resultado SLC / CRS")
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
}

// MARK: - Shared Result Components

struct GradeBadgeView: View {
    let syndrome: String
    let acronym: String
    let grade: String
    let colorName: String

    private var color: Color {
        switch colorName {
        case "gradeGreen": return .green
        case "gradeYellow": return Color(red: 0.85, green: 0.7, blue: 0)
        case "gradeOrange": return .orange
        case "gradeRed": return .red
        case "gradePurple": return .purple
        default: return .gray
        }
    }

    var body: some View {
        VStack(spacing: 12) {
            Text(syndrome)
                .font(.caption.bold())
                .foregroundStyle(.secondary)
                .tracking(1)
                .multilineTextAlignment(.center)

            ZStack {
                Circle()
                    .fill(color.opacity(0.15))
                    .frame(width: 140, height: 140)
                Circle()
                    .strokeBorder(color, lineWidth: 4)
                    .frame(width: 140, height: 140)
                VStack(spacing: 4) {
                    Text(grade)
                        .font(.system(size: 32, weight: .heavy, design: .rounded))
                        .foregroundStyle(color)
                    Text(acronym)
                        .font(.caption.bold())
                        .foregroundStyle(color.opacity(0.8))
                }
            }
        }
        .frame(maxWidth: .infinity)
        .padding(.vertical, 8)
    }
}

struct ResultSectionCard<Content: View>: View {
    let title: String
    let icon: String
    var accent: Color = .primary
    @ViewBuilder let content: Content

    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            Label(title, systemImage: icon)
                .font(.headline)
                .foregroundStyle(accent)
            content
        }
        .frame(maxWidth: .infinity, alignment: .leading)
        .padding()
        .background(.regularMaterial)
        .clipShape(RoundedRectangle(cornerRadius: 16))
    }
}

struct FindingRow: View {
    let label: String
    let value: String
    let isAbnormal: Bool

    var body: some View {
        VStack(alignment: .leading, spacing: 2) {
            Text(label)
                .font(.caption)
                .foregroundStyle(.secondary)
            HStack {
                Image(systemName: isAbnormal ? "exclamationmark.circle.fill" : "checkmark.circle.fill")
                    .foregroundStyle(isAbnormal ? .orange : .green)
                    .font(.caption)
                Text(value)
                    .font(.subheadline)
                    .foregroundStyle(isAbnormal ? .orange : .primary)
            }
        }
    }
}

struct UrgencyBannerView: View {
    let level: String
    let colorName: String

    private var color: Color {
        switch colorName {
        case "gradeGreen": return .green
        case "gradeYellow": return .yellow
        case "gradeOrange": return .orange
        case "gradeRed": return .red
        case "gradePurple": return .purple
        default: return .gray
        }
    }

    var body: some View {
        HStack {
            Image(systemName: "bell.badge.fill")
                .font(.title3)
                .foregroundStyle(.white)
            VStack(alignment: .leading, spacing: 2) {
                Text("Nivel de Urgencia")
                    .font(.caption)
                    .foregroundStyle(.white.opacity(0.8))
                Text(level)
                    .font(.headline.bold())
                    .foregroundStyle(.white)
            }
            Spacer()
        }
        .padding()
        .background(color)
        .clipShape(RoundedRectangle(cornerRadius: 14))
    }
}

struct ReferenceFooter: View {
    let text: String

    var body: some View {
        Text(text)
            .font(.caption2)
            .foregroundStyle(.tertiary)
            .multilineTextAlignment(.center)
            .padding(.vertical, 8)
    }
}
