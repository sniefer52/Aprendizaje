import SwiftUI

struct HomeView: View {
    var body: some View {
        NavigationStack {
            ScrollView {
                VStack(spacing: 24) {
                    // Header
                    VStack(spacing: 8) {
                        Image(systemName: "cross.case.fill")
                            .font(.system(size: 56))
                            .foregroundStyle(.blue)
                        Text("CTCAE Grader")
                            .font(.largeTitle.bold())
                        Text("Síndrome Liberación Citocinas & ICANS")
                            .font(.subheadline)
                            .foregroundStyle(.secondary)
                            .multilineTextAlignment(.center)
                    }
                    .padding(.top, 24)

                    // Quick info cards
                    VStack(spacing: 16) {
                        InfoCard(
                            title: "SLC / CRS",
                            subtitle: "Síndrome de Liberación de Citocinas",
                            icon: "flame.fill",
                            color: .orange,
                            description: "Clasificación ASTCT 2019 • Grados 1–4 basados en fiebre, hipotensión e hipoxia"
                        )
                        InfoCard(
                            title: "ICANS",
                            subtitle: "Neurotoxicidad Asociada a Células Efectoras Inmunes",
                            icon: "brain.head.profile",
                            color: .purple,
                            description: "Escala ICE + nivel de consciencia + convulsiones + edema cerebral"
                        )
                    }
                    .padding(.horizontal)

                    // Grade legend
                    GradeLegendView()
                        .padding(.horizontal)

                    // Disclaimer
                    DisclaimerView()
                        .padding(.horizontal)
                        .padding(.bottom, 24)
                }
            }
            .navigationTitle("CTCAE Grader")
            .navigationBarTitleDisplayMode(.inline)
        }
    }
}

struct InfoCard: View {
    let title: String
    let subtitle: String
    let icon: String
    let color: Color
    let description: String

    var body: some View {
        HStack(alignment: .top, spacing: 16) {
            Image(systemName: icon)
                .font(.title2)
                .foregroundStyle(color)
                .frame(width: 44, height: 44)
                .background(color.opacity(0.15))
                .clipShape(RoundedRectangle(cornerRadius: 12))

            VStack(alignment: .leading, spacing: 4) {
                Text(title)
                    .font(.headline)
                Text(subtitle)
                    .font(.caption)
                    .foregroundStyle(.secondary)
                Text(description)
                    .font(.caption2)
                    .foregroundStyle(.tertiary)
                    .padding(.top, 2)
            }
            Spacer()
        }
        .padding()
        .background(.regularMaterial)
        .clipShape(RoundedRectangle(cornerRadius: 16))
    }
}

struct GradeLegendView: View {
    private let grades: [(String, Color, String)] = [
        ("G1", .yellow, "Leve"),
        ("G2", .orange, "Moderado"),
        ("G3", .red, "Severo"),
        ("G4", .purple, "Crítico"),
    ]

    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text("Escala de Gravedad CTCAE")
                .font(.headline)

            HStack(spacing: 8) {
                ForEach(grades, id: \.0) { grade, color, label in
                    VStack(spacing: 4) {
                        Text(grade)
                            .font(.caption.bold())
                            .foregroundStyle(.white)
                            .frame(width: 36, height: 36)
                            .background(color)
                            .clipShape(Circle())
                        Text(label)
                            .font(.caption2)
                            .foregroundStyle(.secondary)
                    }
                    .frame(maxWidth: .infinity)
                }
            }
        }
        .padding()
        .background(.regularMaterial)
        .clipShape(RoundedRectangle(cornerRadius: 16))
    }
}

struct DisclaimerView: View {
    var body: some View {
        HStack(alignment: .top, spacing: 10) {
            Image(systemName: "exclamationmark.triangle.fill")
                .foregroundStyle(.yellow)
            VStack(alignment: .leading, spacing: 4) {
                Text("Uso Clínico")
                    .font(.caption.bold())
                Text("Esta herramienta es un apoyo a la decisión clínica. El diagnóstico y tratamiento deben ser realizados por profesionales médicos cualificados conforme a los protocolos institucionales vigentes.")
                    .font(.caption2)
                    .foregroundStyle(.secondary)
            }
        }
        .padding()
        .background(Color.yellow.opacity(0.1))
        .clipShape(RoundedRectangle(cornerRadius: 12))
        .overlay(
            RoundedRectangle(cornerRadius: 12)
                .stroke(Color.yellow.opacity(0.3), lineWidth: 1)
        )
    }
}
