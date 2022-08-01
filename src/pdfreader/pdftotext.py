"""
Documentation
THe script extracts text and saves it to a text file it is not good with tables but works with text that is either
one column or two columns. There are two libraries used PYPDF2 and pdfplumber PyPDF2 does the extraction and pdfplumber
recognizes if the pdf is one or two column(if the pdf has two pages in one like a book)

Also don't worry about the PdfReadWarning that happens when the table is not formatted correctly
"""

import PyPDF2

import tkinter.filedialog
# from nltk import word_tokenize
# from nltk.corpus import stopwords
import pdfplumber
from io import StringIO
from Postprocess import PostProcessing
from justimages import imageextraction



def conversion(filename, outfile):

    print(f"\nYour input file is {filename.rsplit('/', 1)[-1]}")
    print(f"\nYour output file is {outfile}\n")
    double_column = pdfplumber.open(filename)
    # This part check if the pdf is one column or two
    # If text tolerance is above 12 it starts to have issues
    isDoubleColumn = bool(double_column.pages[2].extract_table(dict(vertical_strategy='text', text_tolerance=12)))

    # Open the pdf as a binary and also converts into UTF-8 characters
    pdfFileObj = open(filename, 'rb')
    # Reads the pdf as an object
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

    num_pages = pdfReader.numPages
    count = 0
    text = ""

    # Use a while loop to extract all the text from all the pages and put them in a string
    while count < num_pages:
        pageObj = pdfReader.getPage(3)
        count += 1
        # All the reading is done here
        text += pageObj.extractText()

    # Double column is tough to just print out and understand so there is another file that does the post-processing
    if isDoubleColumn:
        print(f"\n{filename.rsplit('/', 1)[-1]} is a double column pdf\n")
        text = PostProcessing(text)
    else:
        print(f"\n{filename} is a single column pdf\n")

    # Incase you want to use a tokinizer to better help the program I don't know how to use it but have left it here
    '''tokens = word_tokenize(text)
    
    punctuations = [';', ':', '[', ']', ',']
    stop_words = stopwords.words('english')
    keywords = [word for word in tokens if not word in stop_words and not word in punctuations]'''

    # Join all the words back together into one string to write the text
    words = "".join(text)

    # Extracting the images from the pdf
    imageextraction(filename)


    # Writing to a txt file
    with open(outfile, "w") as f:
        f.write(words)
    # print(words)
    print(f'\nSuccessfully converted to {outfile}')


if __name__ == "__main__":
    root = tkinter.Tk()
    filename = tkinter.filedialog.askopenfilename(
        initialdir=[""], filetypes=[("pdf files", "*.pdf")])
    root.destroy()
    outfile = filename.rsplit('/', 1)[1]
    outfile = f"{outfile.rsplit('.', 1)[0]}_parsedText.txt"
    conversion(filename, outfile)

