import Foundation
import Combine

class AssessmentStore: ObservableObject {
    @Published var crsAssessments: [CRSAssessment] = []
    @Published var icansAssessments: [ICANSAssessment] = []

    private let crsKey = "crs_assessments"
    private let icansKey = "icans_assessments"

    init() {
        load()
    }

    func addCRS(_ assessment: CRSAssessment) {
        crsAssessments.insert(assessment, at: 0)
        save()
    }

    func addICANS(_ assessment: ICANSAssessment) {
        icansAssessments.insert(assessment, at: 0)
        save()
    }

    func deleteCRS(at offsets: IndexSet) {
        crsAssessments.remove(atOffsets: offsets)
        save()
    }

    func deleteICANS(at offsets: IndexSet) {
        icansAssessments.remove(atOffsets: offsets)
        save()
    }

    private func save() {
        if let crsData = try? JSONEncoder().encode(crsAssessments) {
            UserDefaults.standard.set(crsData, forKey: crsKey)
        }
        if let icansData = try? JSONEncoder().encode(icansAssessments) {
            UserDefaults.standard.set(icansData, forKey: icansKey)
        }
    }

    private func load() {
        if let crsData = UserDefaults.standard.data(forKey: crsKey),
           let decoded = try? JSONDecoder().decode([CRSAssessment].self, from: crsData) {
            crsAssessments = decoded
        }
        if let icansData = UserDefaults.standard.data(forKey: icansKey),
           let decoded = try? JSONDecoder().decode([ICANSAssessment].self, from: icansData) {
            icansAssessments = decoded
        }
    }
}
