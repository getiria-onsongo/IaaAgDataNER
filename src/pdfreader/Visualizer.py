# pip install py-pdf-parser will fix your issue
# This is not everything that tesseract is reading but it helps to visualize which texts general ocrs recognize from the pdf
from py_pdf_parser.loaders import load_file
from py_pdf_parser.visualise import visualise

document = load_file("c2cy20348k_bulk.pdf")
visualise(document)