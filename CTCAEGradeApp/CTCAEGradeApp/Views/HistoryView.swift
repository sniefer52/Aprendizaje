import SwiftUI

struct HistoryView: View {
    @EnvironmentObject var store: AssessmentStore
    @State private var selectedSegment = 0

    var body: some View {
        NavigationStack {
            VStack(spacing: 0) {
                Picker("Tipo", selection: $selectedSegment) {
                    Text("SLC / CRS").tag(0)
                    Text("ICANS").tag(1)
                }
                .pickerStyle(.segmented)
                .padding()

                if selectedSegment == 0 {
                    CRSHistoryList()
                } else {
                    ICANSHistoryList()
                }
            }
            .navigationTitle("Historial")
        }
    }
}

struct CRSHistoryList: View {
    @EnvironmentObject var store: AssessmentStore

    var body: some View {
        if store.crsAssessments.isEmpty {
            EmptyHistoryView(type: "SLC / CRS")
        } else {
            List {
                ForEach(store.crsAssessments) { assessment in
                    NavigationLink {
                        CRSResultView(assessment: assessment, onSave: {})
                    } label: {
                        HistoryRowView(
                            date: assessment.date,
                            grade: assessment.computedGrade.displayName,
                            urgency: assessment.computedGrade.urgencyLevel,
                            colorName: assessment.computedGrade.colorName,
                            subtitle: "T: \(String(format: "%.1f", assessment.temperature))°C · \(assessment.hypotensionLevel == .none ? "Sin hipotensión" : "Hipotensión")"
                        )
                    }
                }
                .onDelete { store.deleteCRS(at: $0) }
            }
            .listStyle(.insetGrouped)
        }
    }
}

struct ICANSHistoryList: View {
    @EnvironmentObject var store: AssessmentStore

    var body: some View {
        if store.icansAssessments.isEmpty {
            EmptyHistoryView(type: "ICANS")
        } else {
            List {
                ForEach(store.icansAssessments) { assessment in
                    NavigationLink {
                        ICANSResultView(assessment: assessment, onSave: {})
                    } label: {
                        HistoryRowView(
                            date: assessment.date,
                            grade: assessment.computedGrade.displayName,
                            urgency: assessment.computedGrade.urgencyLevel,
                            colorName: assessment.computedGrade.colorName,
                            subtitle: "ICE: \(assessment.iceScore)/10 · \(assessment.levelOfConsciousness.rawValue)"
                        )
                    }
                }
                .onDelete { store.deleteICANS(at: $0) }
            }
            .listStyle(.insetGrouped)
        }
    }
}

struct HistoryRowView: View {
    let date: Date
    let grade: String
    let urgency: String
    let colorName: String
    let subtitle: String

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
        HStack(spacing: 14) {
            Text(grade.replacingOccurrences(of: "Grado ", with: "G"))
                .font(.headline.bold())
                .foregroundStyle(.white)
                .frame(width: 44, height: 44)
                .background(color)
                .clipShape(RoundedRectangle(cornerRadius: 10))

            VStack(alignment: .leading, spacing: 3) {
                Text(date.formatted(date: .abbreviated, time: .shortened))
                    .font(.subheadline.bold())
                Text(subtitle)
                    .font(.caption)
                    .foregroundStyle(.secondary)
                    .lineLimit(2)
            }

            Spacer()

            Text(urgency)
                .font(.caption2.bold())
                .foregroundStyle(color)
                .padding(.horizontal, 8)
                .padding(.vertical, 4)
                .background(color.opacity(0.15))
                .clipShape(Capsule())
        }
        .padding(.vertical, 2)
    }
}

struct EmptyHistoryView: View {
    let type: String

    var body: some View {
        ContentUnavailableView(
            "Sin evaluaciones",
            systemImage: "clock.badge.xmark",
            description: Text("Las evaluaciones de \(type) guardadas aparecerán aquí.")
        )
    }
}
