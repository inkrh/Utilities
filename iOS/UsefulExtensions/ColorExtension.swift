import SwiftUI


public extension UIColor {
    
    convenience init(hex: String, alpha: CGFloat = 1.0) {
        //initializes color from a 6 character hex string
        var hexFormatted: String = hex.trimmingCharacters(in: CharacterSet.whitespacesAndNewlines).uppercased()
        
        if hexFormatted.hasPrefix("#") {
            hexFormatted = String(hexFormatted.dropFirst())
        }
        
        var rgbValue: UInt64 = 0
        Scanner(string: hexFormatted).scanHexInt64(&rgbValue)
        
        self.init(red: CGFloat((rgbValue & 0xFF0000) >> 16) / 255.0,
                  green: CGFloat((rgbValue & 0x00FF00) >> 8) / 255.0,
                  blue: CGFloat(rgbValue & 0x0000FF) / 255.0,
                  alpha: alpha)
    }
    
    func asColor() -> Color {
        //returns UIColor as a Color
        return Color(self)
    }
    
    func asCGColor() -> CGColor {
        //returns UIColor as a CGColor
        return self.cgColor
    }
    
    static func contrastRatio(between color1: UIColor, and color2: UIColor) -> CGFloat {
        //checks contrast ration between color1 and color2
        // https://www.w3.org/TR/WCAG20-TECHS/G18.html#G18-tests
        
        let luminance1 = color1.luminance()
        let luminance2 = color2.luminance()
        
        let luminanceDarker = min(luminance1, luminance2)
        let luminanceLighter = max(luminance1, luminance2)
        
        return (luminanceLighter + 0.05) / (luminanceDarker + 0.05)
    }
    
    func contrastRatio(with color: UIColor) -> CGFloat {
        //checks contrast ration between self and a given UIColor
        return UIColor.contrastRatio(between: self, and: color)
    }
    
    func luminance() -> CGFloat {
        //returns luminance
        // https://www.w3.org/TR/WCAG20-TECHS/G18.html#G18-tests
        
        let ciColor = CIColor(color: self)
        
        func adjust(colorComponent: CGFloat) -> CGFloat {
            return (colorComponent < 0.04045) ? (colorComponent / 12.92) : pow((colorComponent + 0.055) / 1.055, 2.4)
        }
        
        return 0.2126 * adjust(colorComponent: ciColor.red) + 0.7152 * adjust(colorComponent: ciColor.green) + 0.0722 * adjust(colorComponent: ciColor.blue)
    }
}
