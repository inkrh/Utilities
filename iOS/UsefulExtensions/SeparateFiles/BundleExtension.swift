import Foundation

public extension Bundle {
    var releaseVersionNumber: String? {
        //returns release version
        return infoDictionary?["CFBundleShortVersionString"] as? String
    }

    var buildVersionNumber: String? {
        //returns build version
        return infoDictionary?["CFBundleVersion"] as? String
    }
    
    var bundleIdentifier: String? {
        //returns bundleID
        return infoDictionary?["CFBundleIdentifier"] as? String
    }

    var releaseVersionNumberPretty: String {
        //returns formatted release version
        return "v\(releaseVersionNumber ?? "0.0.0")"
    }
    var releaseName: String? {
        //returns bundle name
        return infoDictionary?["CFBundleName"] as? String
    }

    var releaseDisplayName: String? {
        //returns bundle display name
        return infoDictionary?["CFBundleDisplayName"] as? String
    }
}
