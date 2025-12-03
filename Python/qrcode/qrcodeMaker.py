import qrcode, sys

def getQRCode(text):
    return qrcode.make(text)
    
print ("Basic QRCode generator")
print ("Usage python qrcodeMaker.py <URL>")
print ("Requires qrcode from https://pypi.org/project/qrcode/")
print ("pip install qrcode[pil]")

if len(sys.argv) >1:
    url=sys.argv[1]
    print(url)
    getQRCode(url).save("QRCode.png","PNG")
