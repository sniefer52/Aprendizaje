import SwiftUI

@main
struct CTCAEGradeApp: App {
    @StateObject private var store = AssessmentStore()

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(store)
        }
    }
}
