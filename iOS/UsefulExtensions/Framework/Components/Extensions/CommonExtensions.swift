import UIKit
import Foundation
import SwiftUI
import CommonCrypto


//UIImage extensions
public extension UIImage {
    convenience init?(color: UIColor, size: CGSize = CGSize(width: 1, height: 1)) {
        //initializes an image with a fill color
           let rect = CGRect(origin: .zero, size: size)
           UIGraphicsBeginImageContextWithOptions(rect.size, false, 0.0)
           color.setFill()
           UIRectFill(rect)
           let image = UIGraphicsGetImageFromCurrentImageContext()
           UIGraphicsEndImageContext()

           guard let cgImage = image?.cgImage else {
               return nil
           }
           self.init(cgImage: cgImage)
       }
}

//Bundle extensions
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

//UI Button Extensions
public extension UIButton {
    private func image(withColor color: UIColor) -> UIImage? {
        //returns image button with fill color
        let rect = CGRect(x: 0.0, y: 0.0, width: 1.0, height: 1.0)
        UIGraphicsBeginImageContext(rect.size)
        let context = UIGraphicsGetCurrentContext()

        context?.setFillColor(color.cgColor)
        context?.fill(rect)

        let image = UIGraphicsGetImageFromCurrentImageContext()
        UIGraphicsEndImageContext()

        return image
    }

    func setBackgroundColor(_ color: UIColor, for state: UIControl.State) {
        //sets button background color
        self.setBackgroundImage(image(withColor: color), for: state)
    }
}

//UITextField Extensions
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
    

public extension Bool {
     var asString: String {
        //returns string value of bool
        if self {return "true"}
        
        return "false"
    }
}


//String extensions
public extension String {
    
    var asBool: Bool? {
        //returns bool value of string
            switch self.lowercased() {
            case "true", "t", "yes", "y", "1":
                return true
            case "false", "f", "no", "n", "0":
                return false
            default:
                return nil
            }
        }


    func notNil() -> Bool {
        //checks if string is empty or has no characters
        return !self.isEmpty && self.count > 0
    }
    
    func getEscapedText() -> String {
        //escapes text
        let wrapper = "\""
        //if nil will be ""
        var textToCheck:String = ""
        if(self.notNil()) {
            textToCheck = self.trimmingCharacters(in: .whitespacesAndNewlines).trimmingCharacters(in: .illegalCharacters).trimmingCharacters(in: .controlCharacters)
            textToCheck = "\(wrapper)\(textToCheck)\(wrapper)"
        }
        
        return textToCheck
    }
    
    func isValidEmail() -> Bool {
        //checks if format is string@string.string
        let emailRegEx = "[A-Z0-9a-z._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,64}"
        
        var textToCheck:String = self
        if(self.notNil()) {
            textToCheck = textToCheck.trimmingCharacters(in: .whitespacesAndNewlines)
            let emailPred = NSPredicate(format:"SELF MATCHES %@", emailRegEx)
            return emailPred.evaluate(with: textToCheck)
        }
        
        return false
    }
    
    func isValidURI() -> Bool {
        //checks if format is a valid URL format
        let urlRegEx = "^(https?://)?(www\\.)?([-a-z0-9]{1,63}\\.)*?[a-z0-9][-a-z0-9]{0,61}[a-z0-9]\\.[a-z]{2,6}(/[-\\w@\\+\\.~#\\?&/=%]*)?$"
        
        let textToCheck:String = self
        let urlTest = NSPredicate(format:"SELF MATCHES %@", urlRegEx)
        return urlTest.evaluate(with: textToCheck)
    }
    
    func base64ToImage() -> UIImage{
        //converts a base64 string to UIImage
      if (self.isEmpty) {
          return #imageLiteral(resourceName: "no_image_found")
      }else {
          // !!! Separation part is optional, depends on your Base64String !!!
          let temp = self.components(separatedBy: ",")
          let dataDecoded : Data = Data(base64Encoded: temp[1], options: .ignoreUnknownCharacters)!
          let decodedimage = UIImage(data: dataDecoded)
          return decodedimage!
      }
    }
    
    func replaceYear() -> String {
        //populates the year in the copyright
        return self.replacingOccurrences(of:"YYYY", with: String(Calendar.current.component(.year, from: Date())))
    }
    
    func toDate(with format: String) -> Date? {
        let dateFormatter = DateFormatter()
        dateFormatter.calendar = Calendar(identifier: .gregorian)
        dateFormatter.locale = Locale(identifier: Locale.current.identifier)
        dateFormatter.timeZone = .current
        dateFormatter.dateFormat = format
        let date = dateFormatter.date(from: self)
        return date
    }
    
}

public extension UIScreen {
   static let screenWidth = UIScreen.main.bounds.size.width
   static let screenHeight = UIScreen.main.bounds.size.height
   static let screenSize = UIScreen.main.bounds.size
}

public extension Date {
    static func days(since date: Date) -> Int {
        let calendar = Calendar(identifier: .gregorian)
        let components = calendar.dateComponents([.day], from: date, to: Date())
        return components.day ?? 0
    }
}
