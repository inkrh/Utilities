import UIKit

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
