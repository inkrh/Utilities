import Foundation
import UIKit

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
        //Potential improvement: add in lookup for all known domains (would need maintaining)
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
          // Separation is optional, depends on input Base64String
          let temp = self.components(separatedBy: ",")
          let dataDecoded : Data = Data(base64Encoded: temp[1], options: .ignoreUnknownCharacters)!
          let decodedimage = UIImage(data: dataDecoded)
          return decodedimage!
      }
    }
    
    func replaceYear() -> String {
        //populates YYYY in a string with the year
        return self.replacingOccurrences(of:"YYYY", with: String(Calendar.current.component(.year, from: Date())))
    }
    
    func toDate(with format: String) -> Date? {
        //converts a string to a date object
        //TODO: better error handling
        let dateFormatter = DateFormatter()
        dateFormatter.calendar = Calendar(identifier: .gregorian)
        dateFormatter.locale = Locale(identifier: Locale.current.identifier)
        dateFormatter.timeZone = .current
        dateFormatter.dateFormat = format
        let date = dateFormatter.date(from: self)
        return date
    }
    
}
