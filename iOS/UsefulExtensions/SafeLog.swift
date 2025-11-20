import Foundation

func stringFromAny(_ value:Any?) -> String {
    //converts Any to String
    if let nonNil = value, !(nonNil is NSNull) {
        return String(describing: nonNil)
    }
    return ""
}

public func SafeLog(_ message:Any) {
    //logs if not debug
    #if !NDEBUG
    NSLog("%@", stringFromAny(message))
    #endif
}


public func SafeLog(label: String, message: Any) {
    //logs if not debug
    #if !NDEBUG
    NSLog("%@, %@", label, stringFromAny(message))
    #endif
}


//for easy custom messages
extension String: @retroactive Error {}
