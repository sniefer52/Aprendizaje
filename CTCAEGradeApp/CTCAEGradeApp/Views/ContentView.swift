import SwiftUI

struct ContentView: View {
    @EnvironmentObject var store: AssessmentStore
    @State private var selectedTab = 0

    var body: some View {
        TabView(selection: $selectedTab) {
            HomeView()
                .tabItem {
                    Label("Inicio", systemImage: "house.fill")
                }
                .tag(0)

            CRSWizardView()
                .tabItem {
                    Label("SLC / CRS", systemImage: "flame.fill")
                }
                .tag(1)

            ICANSWizardView()
                .tabItem {
                    Label("ICANS", systemImage: "brain.head.profile")
                }
                .tag(2)

            HistoryView()
                .tabItem {
                    Label("Historial", systemImage: "clock.fill")
                }
                .tag(3)
        }
        .tint(.blue)
    }
}
