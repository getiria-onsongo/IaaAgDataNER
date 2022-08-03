"""
Documentation

This pdf to text extraction is good for pdfs that don't have texts in images like chemical compound pictures but is a
great text extractor especially pdfs with tables.
The pdf extractor works by using tesseract(Google's pretrained model) to extract text and by using pdfplumber I recognize
if the pdf is one or two column then use different post-processing scripts

***NOTE***
This take a long time if the pdf especially with pdfs that have 10+ pages which almost any type of research paper
"""
import math
import time

import pdfplumber
from pdf2image import convert_from_path
from pytesseract import pytesseract
import os
import tkinter.filedialog
import sys
from justimages import imageextraction




def ocrConversion(infile, outfile):
    start_time=time.time()
    file = pdfplumber.open(infile)
    numPages = len(file.pages)
    pageNum = 3
    if numPages <= 4:
        pageNum = math.ceil(numPages / 2)
    # This part check if the pdf is one column or two
    # If text tolerance is above 12 it starts to have issues
    isDoubleColumn = bool(file.pages[pageNum].extract_table(dict(vertical_strategy='text', text_tolerance=12)))

    # Converts the pdf to object to convert it to a png file
    pages = convert_from_path(infile, 500)

    # Extracting the images from the pdf
    imageextraction(infile)


    i = 0
    text = ""

    # Remove the temp folder incase it exists
    if os.path.exists("%temp%"):
        pass
    else:
        os.mkdir("%temp%")

    # Getting the current directory of the script
    curDir = os.getcwd()

    # Creating a temp folder to convert the pages to png for OCR
    try:
        os.mkdir(curDir + "/%temp%/")
    except:
        pass

    # Changing the directory to a temp folder
    os.chdir(curDir + "/%temp%/")

    filename = infile.rsplit('/', 1)[1]
    print(f"Converting {filename} to a string")

    # Used a for each loop to convert every page into png then extract text
    for page in pages:

        imageName = f'{filename} Page {i}.png'

        # Save the page to png for tessaract to process it
        pages[i].save(imageName, 'PNG')
        # Run the png through tesseract and save it as a string
        text += pytesseract.image_to_string(imageName)

        # This is for the progress bar
        sys.stdout.write('\r')
        sys.stdout.write(f"[%-{len(pages)-1}s] %d%%" % ('.'*i, (i+1)/len(pages) * 100))
        # sys.stdout.write(str(round((i+1)/len(pages) * 100, 1)))
        sys.stdout.flush()

        # Removing the images
        os.remove(imageName)
        i += 1

    # Use this for specific pages
    '''
    pages[i].save(f'%temp%/Page {i}.png', 'PNG')
    text += pytesseract.image_to_string(f'%temp%/Page {i}.png')
    '''
    os.chdir(curDir)
    print(os.getcwd())
    # Scripts for post-processing
    if isDoubleColumn:
        print("\n")
        print(f"{infile.rsplit('/', 1)[1]} is a double column PDF")
        text = text.replace("-\n", "")

    else:
        print("\n")
        print(f"{infile.rsplit('/', 1)[1]} is a single column PDF")


    with open(outfile, "w") as f:
        f.write(text)
    try:
        os.rmdir("%temp%")
    except:
        pass
    print(f"\nSuccessfully converted to {outfile}")
    print(f"\nTotal time elapsed {round(time.time()-start_time,0)} seconds\n")

if __name__ == "__main__":
    # Tkinter for gui file selector
    root = tkinter.Tk()
    infile = tkinter.filedialog.askopenfilename(initialdir=[""], filetypes=[("pdf files", "*.pdf")])
    root.destroy()
    outfile = infile.rsplit('/', 1)[1]
    outfile = f"{outfile.rsplit('.', 1)[0]}_text.txt"
    print()
    ocrConversion(infile, outfile)