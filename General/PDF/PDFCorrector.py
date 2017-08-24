from PyPDF2 import PdfFileReader, PdfFileWriter
import os

##utility to remove front page from PDFs (e.g. EPA's archive statement)
##should really put new files in a separate folder but was a little lazy

def FileWalk(path):
    for root, subdirs, files in os.walk(path):
        for f in files:
            fp = os.path.join(root, f)

            if f.endswith('.pdf'):
                print(f)
                outPDF = PdfFileWriter()
                inPDF = PdfFileReader(fp)
                pages = inPDF.getNumPages()
                for p in range(1, pages):
                    outPDF.addPage(inPDF.getPage(p))

                n = fp.replace(".pdf", "n.pdf")
                outputStream = open(n, 'wb')
                outPDF.write(outputStream)
                outputStream.close()
