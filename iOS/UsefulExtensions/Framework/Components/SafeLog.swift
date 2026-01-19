//  Relatively safe local logging

import Foundation

func stringFromAny(_ value:Any?) -> String {
    //converts Any to String
    if let nonNil = value, !(nonNil is NSNull) {
        return String(describing: nonNil)
    }
    return ""
}

public func RSLog(_ message:Any) {
    //logs if not debug
    #if !NDEBUG
    NSLog("%@", stringFromAny(message))
    #endif
}


public func RSLog(label: String, message: Any) {
    //logs if not debug
    #if !NDEBUG
    NSLog("%@, %@", label, stringFromAny(message))
    #endif
}

// Use this for easy custom messages as errors
public struct StringError: Error, CustomStringConvertible {
    public let message: String
    public var description: String { message }
    
    public init(_ message: String) {
        self.message = message
    }
}
