from pyPdf import PdfFileWriter, PdfFileReader

dir = "../data"

pdf = PdfFileReader(file(dir+"/serrablo 153.pdf", "rb"))
pn=0
pdf.
for page in pdf.pages:
    pn = pn + 1
    print pn 
    print page.extractText()
    
print "fin...."    