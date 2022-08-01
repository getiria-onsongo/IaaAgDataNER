import os
import shutil
import sys
import tkinter.filedialog
import fitz
from Postprocess import fitzPostProcess


def imageextraction(file_path):
    pdf_file = fitz.open(file_path)
    location = f"{os.getcwd()}_output"
    if not (os.path.exists(location)):
        os.mkdir(location)
    else:
        shouldDelete = input(f"\nThe output folder already exists, do you want the program to delete the folder again y/n?: ")
        print()
        if shouldDelete.lower() == "y":
            shutil.rmtree(location)
            os.mkdir(location)
        else:
            print("Program Aborted")
            sys.exit(0)

    # Finding the number of pages in the pdf
    number_of_pages = len(pdf_file)
    print("Converting the images")
    # Iterating through each page in the pdf

    print("\n        Images converted to RGB           ")
    print("--------------------------------------------")
    for current_page_index in range(number_of_pages):
        count = -1
        # iterating through each image in every page of PDF
        for img_index, img in enumerate(pdf_file.get_page_images(current_page_index)):
            count += 1
            xref = img[0]
            image = fitz.Pixmap(pdf_file, xref)
            try:

                # If Image colorspace is unspecified or unrecognized
                if image.colorspace is None:
                    image.save("{}/image{}-{}.png".format(location, current_page_index, img_index))

                # If the image colorspace is different than GRAY or RGB image

                elif image.colorspace not in (fitz.csGRAY.name, fitz.csRGB.name):

                    image = fitz.Pixmap(fitz.csRGB, image)

                    image.save("{}/image{}-{}.png".format(location, current_page_index, img_index))

                    print(f"image{current_page_index}-{img_index}", end="\t" )


                # if it is a is GRAY or RGB image
                elif image.n < 5:
                    image = fitz.Pixmap(fitz.csRGB, image)
                    image.save("{}/image{}-{}.png".format(location, current_page_index, img_index))


                # Convert to RGB first
                else:

                    new_image = fitz.Pixmap(fitz.csRGB, image)
                    new_image.save("{}/image{}-{}.png".foramt(location, current_page_index, img_index))
            except:
                print(f"image{current_page_index}-{img_index} has invalid color space")
    # All the above is for image processing
    print("\n--------------------------------------------\n")
    print(f"Images extracted to {file_path}_output folder")
    # This is for text processing
    out = open(location + "/text_notFinal.txt", "wb")  # open text output
    for page in pdf_file:  # iterate the document pages
        text = page.get_text().encode("utf8")  # get plain text (is in UTF-8)
        out.write(text)  # write text of page
        out.write(bytes((12,)))  # write page delimiter (form feed 0x0C)
    pdf_file.close()


if __name__ == "__main__":
    root = tkinter.Tk()
    file = tkinter.filedialog.askopenfilename(filetypes=[("pdf files", "*.pdf")])
    root.destroy()
    imageextraction(file)
