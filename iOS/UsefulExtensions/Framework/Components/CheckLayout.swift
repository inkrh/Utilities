import Foundation
import UIKit

public struct CheckLayout {
    //checks given view elements
    public static func buttonSize(_ size:CGFloat) -> CGFloat {
        //checks that button size is > minimum
        return max(size,LayoutConstants.MIN_BUTTON_SIZE);
    }
    
    public static func fontSize(_ size:CGFloat) -> CGFloat {
        //checks that font is > general minimum
        return max(size,LayoutConstants.MIN_FONT_SIZE);
    }

    public static func bodyFontSize(_ size:CGFloat) -> CGFloat {
        //checks that font is > body font size
        return max(size,LayoutConstants.MIN_BODY_FONT_SIZE);
    }

    public static func isContrastOK(colorOne: UIColor, colorTwo: UIColor) -> Bool {
        //checks that given color combination has a greater ratio than 3:1
        //AA Standards WCAG of > 3:1
        return UIColor.contrastRatio(between: colorOne, and: colorTwo) >= 3.1;
    }
}
