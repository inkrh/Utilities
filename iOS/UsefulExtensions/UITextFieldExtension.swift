import UIKit

public extension UITextField {
    
    private func reject() {
        self.backgroundColor = UIColor(.red)
    }
    
    private func approve() {
        self.backgroundColor = UIColor(.green)
    }
    
    func notNil() -> Bool {
        //checks if string is empty or has no characters
        if (self.text ?? "").notNil() {
           approve()
        } else {
            reject()
        }
        return (self.text ?? "").notNil()
    }
    
    func getEscapedText() -> String {
        //escapes text
        return (self.text ?? "").getEscapedText()
    }
    
    func isValidEmail() -> Bool {
        //checks if format is string@string.string
        if (self.text ?? "").isValidEmail() {
           approve()
        } else {
            reject()
        }
        return (self.text ?? "").isValidEmail()
    }
    
    func isValidURI() -> Bool {
        //checks if format is a valid URL format
        if (self.text ?? "").isValidURI() {
            approve()
        } else {
            reject()
        }
        return (self.text ?? "").isValidURI()
    }
}
