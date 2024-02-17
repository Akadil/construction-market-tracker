from io import StringIO

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

output_string = StringIO()

def printWholeText():
    with open('services/appendix_parser/examples/appendix_9.pdf', 'rb') as in_file:
        parser = PDFParser(in_file)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        # pages = PDFPage.create_pages(doc)

        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)
    print(output_string.getvalue())


def printLastPages():
    print("Hello World")


if __name__ == "__main__":
    printWholeText()
    # printLastPages()