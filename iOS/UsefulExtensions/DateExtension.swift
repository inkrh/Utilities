import Foundation

public extension Date {
    static func days(since date: Date) -> Int {
        let calendar = Calendar(identifier: .gregorian)
        let components = calendar.dateComponents([.day], from: date, to: Date())
        return components.day ?? 0
    }
}
