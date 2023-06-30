import io
import textract
import re
import camelot

from io import StringIO

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

from pdfminer.layout import LTTextBoxHorizontal

from pdfminer.layout import LAParams
# from pdfminer.converter import PDFResourceManager, PDFPageAggregator

from pdfminer.layout import LTTextBoxHorizontal
# from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer
from pdfminer.pdfinterp import resolve1

def pdf_2_text_whole_document(pdf_path):
    """
    Takes as input a path to a PDF document and converts it to text.
    """
    output_string = StringIO()
    with open(pdf_path, 'rb') as in_file:
        parser = PDFParser(in_file)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        for page in PDFPage.create_pages(doc):
            # print("Page=",page)
            interpreter.process_page(page)

    pdf_text = output_string.getvalue()
    device.close()
    output_string.close()

    return pdf_text


def extract_text_by_page(pdf_path):
    with open(pdf_path, 'rb') as fh:
        for page in PDFPage.get_pages(fh,
                                      caching=True,
                                      check_extractable=True):
            resource_manager = PDFResourceManager()
            fake_file_handle = io.StringIO()
            converter = TextConverter(resource_manager, fake_file_handle)
            page_interpreter = PDFPageInterpreter(resource_manager, converter)
            page_interpreter.process_page(page)

            text = fake_file_handle.getvalue()
            yield text

            # close open handles
            converter.close()
            fake_file_handle.close()


def extract_text(pdf_path):
    for page in extract_text_by_page(pdf_path):
        print(page)
        print()



if __name__ == "__main__":

    typeOne = '/Users/gonsongo/Desktop/research/gems/IaaAgDataNER/Data/potatoes/BoulderProfile.pdf'
    typeTwo = '/Users/gonsongo/Desktop/research/gems/IaaAgDataNER/Data/potatoes/Mesa-Russet-Information-Sheet-20140217.pdf'
    typeThree = '/Users/gonsongo/Desktop/research/gems/IaaAgDataNER/Data/wheat/canvas.pdf'
    typeFour = '/Users/gonsongo/Desktop/research/gems/IaaAgDataNER/Data/wheat/Bond-CL-Reprint.pdf'

    text = textract.process(typeFour,method='pdfminer').decode('utf-8')
    # clean_text = text.replace("  ", " ").replace("\n", "; ").replace(';', ' ')
    print(text)


