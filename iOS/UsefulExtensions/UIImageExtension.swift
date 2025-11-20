import UIKit

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

