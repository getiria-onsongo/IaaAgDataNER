from agParse import *
from datetime import datetime
from functools import partial
from json2py import *
import os.path
from py2json import *
import PyPDF2
import re
import tkinter as tk
from tkinter import filedialog as fd

from tkinter.scrolledtext import ScrolledText

# create a NER GUI class
class CropNerGUI:
    def __init__(self):
        # Create a GUI window
        self.rootWin = tk.Tk()
        #self.rootWin.option_add('*Font', 'Times 24')
        self.rootWin.title("GEMS NER Annotation Tool")

        self.rootWin.geometry('1500x900')

        self.model_dir = None
        self.content=[""]
        self.raw_file = None
        self.annotation_file = None
        self.sentences = None
        self.annotation_dict = {}
        self.file_extension = None
        self.nlp_agdata = None

        self.cust_ents_dict = {}

        self.output_file_name = "sample_p0_td.py"
        self.pageNumber=0
        self.line_num = 0
        self.font_size = "20"
        self.page_lines = len(self.content)

        self.topframe = tk.Frame(self.rootWin)
        self.topframe.grid(row=0, column=0)

        # NOTE: A partial function is created from another function, where some of the parameters are fixed.
        # In the instance below, we want to call the function self.get_ner (which takes a single input) several
        # times but each time we pass it a different value depending on the button that was clicked. If the ALAS
        # button is clicked, we want to pass the text "ALAS" but if the "CROP" button was clicked we want to pass the
        # text CROP. So, partial(self.get_ner, "ALAS") is the same as self.get_ner("ALAS")

        # Named entity buttons
        self.alas_btn = tk.Button(self.topframe, highlightbackground="violet",text="ALAS", command=partial(self.get_ner, "ALAS"))
        self.alas_btn.pack(side = tk.LEFT)
        self.crop_btn = tk.Button(self.topframe, highlightbackground="lawn green",text="CROP", command=partial(self.get_ner, "CROP"))
        self.crop_btn.pack(side = tk.LEFT)
        self.cvar_btn = tk.Button(self.topframe, highlightbackground="deep sky blue",text="CVAR", command=partial(self.get_ner, "CVAR"))
        self.cvar_btn.pack(side = tk.LEFT)
        self.jrnl_btn = tk.Button(self.topframe, highlightbackground="yellow",text="JRNL", command=partial(self.get_ner, "JRNL"))
        self.jrnl_btn.pack(side = tk.LEFT)
        self.path_btn = tk.Button(self.topframe, highlightbackground="red",text="PATH", command=partial(self.get_ner, "PATH"))
        self.path_btn.pack(side = tk.LEFT)
        self.ped_btn = tk.Button(self.topframe, highlightbackground="orange",text="PED", command=partial(self.get_ner, "PED"))
        self.ped_btn.pack(side = tk.LEFT)
        self.plan_btn = tk.Button(self.topframe, highlightbackground="pink",text="PLAN", command=partial(self.get_ner, "PLAN"))
        self.plan_btn.pack(side = tk.LEFT)
        self.pptd_btn = tk.Button(self.topframe, highlightbackground="brown",text="PPTD", command=partial(self.get_ner, "PPTD"))
        self.pptd_btn.pack(side = tk.LEFT)
        self.trat_btn = tk.Button(self.topframe, highlightbackground="MediumPurple1",text="TRAT", command=partial(self.get_ner, "TRAT"))
        self.trat_btn.pack(side = tk.LEFT)

        self.spaceLabel = tk.Label(self.topframe, text="    ", width=17)
        self.spaceLabel.pack(side=tk.LEFT)

        self.clearTag_btn = tk.Button(self.topframe, text="Remove-Tag", command=partial(self.remove_tag))
        self.clearTag_btn.pack(side=tk.LEFT)
        self.pretag_btn = tk.Button(self.topframe, text="Pre-Tag", command=partial(self.pre_tag))
        self.pretag_btn.pack(side=tk.LEFT)

        # adding the text: Note, height defines height if widget in lines based in font size
        self.text = ScrolledText(self.rootWin, height=25, width=140, font = "Times "+self.font_size)
        self.text.insert(tk.END, self.content[self.line_num])
        self.text.focus_force()
        self.text.grid(row=1, column=0, columnspan=4, padx=5, pady=5)

        # Create a scrollbar
        #self.scroll_bar = tk.Scrollbar(self.rootWin)
        #self.scroll_bar.grid(row=1, column=1,rowspan=5,  sticky='NSW')

        #self.text.tag_configure("test", background="yellow", foreground="red")
        #self.text.tag_add("test", "1.1", "1.5")



        # configuring a tag called start which will be used to highlight the text
        self.text.tag_configure("highlight", foreground="black", background="gray")

        self.text.tag_configure("default_color_tag", background="black")
        self.text.tag_configure("ALAS", background="violet")
        self.text.tag_configure("CROP", background="lawn green")
        self.text.tag_configure("CVAR", background="deep sky blue")
        self.text.tag_configure("JRNL", background="yellow")
        self.text.tag_configure("PATH", background="red")
        self.text.tag_configure("PED", background="orange")
        self.text.tag_configure("PLAN", background="pink")
        self.text.tag_configure("PPTD", background="brown")
        self.text.tag_configure("TRAT", background="MediumPurple1")

        self.tags=["highlight","default_color_tag","ALA","CROP","CVAR","JRNL","PATH","PED","PLAN","PPTD","TRAT"]

        self.bottom_frame = tk.Frame(self.rootWin)
        self.bottom_frame.grid(row=2, column=0)

        # Exit button
        self.exit_btn = tk.Button(self.bottom_frame, text="Exit",width=10,command=self.quit)
        self.exit_btn.pack(side = tk.LEFT)

        # Load button
        self.load_btn = tk.Button(self.bottom_frame, text="Load Data", width=10, command=self.LoadPage)
        self.load_btn.pack(side=tk.LEFT)



        # Highlight button
        self.bold_btn = tk.Button(self.bottom_frame, text="Highlight Text",width=10, command=self.highlight_text)
        self.bold_btn.pack(side = tk.LEFT)

        # Clear button
        self.clear_btn = tk.Button(self.bottom_frame, text="Clear All Tags",width=10, command=self.clear_highlight)
        self.clear_btn.pack(side = tk.LEFT)

        # Clear data button
        self.clear_data_btn = tk.Button(self.bottom_frame, text="Clear Data", width=10, command=self.clear_data)
        self.clear_data_btn.pack(side=tk.LEFT)

        # Clear message button
        self.msg_btn = tk.Button(self.bottom_frame, text="Clear Warning Message", width=20, command=self.clear_message)
        self.msg_btn.pack(side=tk.LEFT)

        # Next page button
        self.next_btn = tk.Button(self.bottom_frame, text="Next Page", command=self.nextPage)
        self.next_btn.pack(side = tk.LEFT)

        # Save button
        self.save_btn = tk.Button(self.bottom_frame, text="Save", width=10, command=self.file_save)
        self.save_btn.pack(side=tk.LEFT)

        self.msg_frame = tk.Frame(self.rootWin)
        self.msg_frame.grid(row=3, column=0)

        # Label to display messages
        self.msg = tk.Label(self.msg_frame, text="", padx=5, pady=5)
        self.msg.pack(side=tk.LEFT)

        # Frame for selecting
        self.open_frame = tk.Frame(self.rootWin)
        self.open_frame.grid(row=4, column=0)

        # open file button
        self.open_button = tk.Button(self.open_frame,text='Select Raw Data File(PDF)',width=18,command=partial(self.open_file,"pdf"))
        self.open_button.pack(side=tk.LEFT)

        self.nermodel_button = tk.Button(self.open_frame, text='Select NER model folder', width=18,command=self.get_nermodel_dir)
        self.nermodel_button.pack(side=tk.LEFT)



        self.pageLabel = tk.Label(self.open_frame, text="Raw Data File Page Num:",width=18)
        self.pageLabel.pack(side=tk.LEFT)
        self.pageEntry = tk.Entry(self.open_frame, width=5)
        self.pageEntry.pack(side=tk.LEFT)

        self.fontLabel = tk.Label(self.open_frame, text="Font Size:", width=10)
        self.fontLabel.pack(side=tk.LEFT)
        self.fontEntry = tk.Entry(self.open_frame, width=5)
        self.fontEntry.pack(side=tk.LEFT)

        self.annotation_btn = tk.Button(self.open_frame, text="Select Annotation File(JSON)",width=20,command=partial(self.open_file,"json"))
        self.annotation_btn.pack(side=tk.LEFT)

        self.review_btn = tk.Button(self.open_frame, text="Review Annotations", command=self.ReviewAnnotations)
        self.review_btn.pack(side=tk.LEFT)

        # URL frame
        self.url_frame = tk.Frame(self.rootWin)
        self.url_frame.grid(row=5, column=0)

        self.urlLabel = tk.Label(self.url_frame, text="Paste PDF URL (if known):", width=20)
        self.urlLabel.pack(side=tk.LEFT)
        self.urlEntry = tk.Entry(self.url_frame, width=40)
        self.urlEntry.pack(side=tk.LEFT)

    def get_nermodel_dir(self):
        self.model_dir = fd.askdirectory()
        source_nlp = spacy.load("en_core_web_sm")
        self.nlp_agdata = spacy.load(self.model_dir)
        self.nlp_agdata.add_pipe("parser", before="ner", source=source_nlp)
        self.nlp_agdata.add_pipe("tagger", before="parser", source=source_nlp)

    def open_file(self, file_type):
        """ Get file from user. """

        # Clear warning message, if one exists
        self.msg.config(text="")

        # file type
        filetypes = (
            ('json files', '*.json'),
            ('PDF files', '*.pdf')
        )
        # show the open file dialog
        f = fd.askopenfile(filetypes=filetypes)
        #self.file_extension = pathlib.Path(f.name).suffix

        if file_type == "json":
            self.annotation_file = f
        elif file_type == "pdf":
            self.raw_file=f
        else:
            self.msg.config(text="Warning!! Please select a valid (pdf or json) file.", foreground="red")

    def LoadModel(self):
        """
        Load spacy model
        """
        # model_dir = "/Users/gonsongo/Desktop/research/iaa/Projects/python/IaaAgDataNER/NerModel/model-best"

        if self.nlp_agdata is None:
            source_nlp = spacy.load("en_core_web_md")
            if self.model_dir is not None:
                self.nlp_agdata = spacy.load(self.model_dir)
                self.nlp_agdata.add_pipe("parser", before="ner", source=source_nlp)
                self.nlp_agdata.add_pipe("tagger", before="parser", source=source_nlp)
                # self.nlp_agdata.add_pipe("compound_trait_entities", after='ner')
            else:
                self.nlp_agdata = spacy.load("en_core_web_sm")



    def LoadPDF(self):
        """ Get data from PDF file"""
        pdf_file = open(self.raw_file.name, mode="rb")
        pdfReader = PyPDF2.PdfFileReader(pdf_file)
        # num_pages = pdfReader.numPages
        # Get  page. NOTE, page number for PDF reader start with 0
        OnePage = pdfReader.getPage(self.pageNumber - 1)
        # Get text
        OnePageText = OnePage.extractText()
        # Close PDF file
        pdf_file.close()

        OnePageText = re.sub('\n', '', OnePageText)
        OnePageText = re.sub('\.\s', '.\n', OnePageText)
        OnePageText = re.sub('\s\s', '\n', OnePageText)
        sentences = OnePageText.split("\n")
        return sentences

    def LoadPage(self):
        """
        Load content into text box
        """
        if self.raw_file is None:
            self.msg.config(text="No raw data file has been selected. Please select a file to load.", foreground="red")
        else:
            # Load Spacy Model
            self.LoadModel()

            # Reset annotation dictionary
            self.cust_ents_dict = {}

            # Update font size if it was entered
            font_size = self.fontEntry.get()
            if font_size.isdigit():
                self.text['font'] = "Times "+font_size
                self.font_size = font_size
            else:
                self.fontEntry.delete(0, tk.END)
                self.fontEntry.insert(0, self.font_size)

            page_num = self.pageEntry.get()
            if not page_num.isdigit():
                self.msg.config(text="Page number not entered. Value initialized to 1", foreground="red")
                self.pageNumber = 1
                self.pageEntry.delete(0,tk.END)
                self.pageEntry.insert(0, str(self.pageNumber))
            else:
                self.pageNumber = int(page_num)

            # Delete contents
            self.text.delete(1.0, tk.END)

            # Load PDF file
            self.sentences = self.LoadPDF()
            lineNo = 1
            for sent in self.sentences:
                if len(sent) > 0:
                    self.text.insert(str(lineNo) + ".0", sent + '\n')
                    lineNo = lineNo + 1


    def pre_tag(self):
        """ Pre-tag content in text box with NER tags. """

        # Clear warning message, if one exists
        self.msg.config(text="")
        if self.model_dir is None:
            self.msg.config(text="Warning!! Unable to pre-tag. No NER model selected.", foreground="red")
        else:
            # Reset annotation dictionary
            self.cust_ents_dict = {}

            # Get the line number for the end of the text. This will tell us
            # how many total lines we have loaded
            lastLineIndex = int(self.text.index('end').split(".")[0])

            # Check to see if we have any text. We do not expect a sentence to
            # be less than 5 characters. We will use 5 as the threshold. tk.Text
            # does not appear to have a method for checking if tk.Text is empty
            text = self.text.get("1.0", self.text.index('end'))
            if(len(text) < 5):
                self.msg.config(text="Text field appears to be empty. Please load or enter text to Pre-Tag", foreground="red")
            else:
                # Loop through each of these line
                for lineIndex in range(lastLineIndex):
                    lineNo = lineIndex + 1
                    lineNo_str = str(lineNo)
                    input_text = self.text.get(lineNo_str + ".0", lineNo_str + ".end")
                    doc = self.tag_ner_with_spacy(input_text)

                    for ent in doc.ents:
                        if (ent.label_ in self.tags):
                            self.text.tag_add(ent.label_, lineNo_str+"." + str(ent.start_char), lineNo_str+"." + str(ent.end_char))
                            if (self.cust_ents_dict.get(lineNo, False)):
                                self.cust_ents_dict[lineNo].append((ent.start_char, ent.end_char, ent.label_))
                            else:
                                self.cust_ents_dict[lineNo] = [(ent.start_char, ent.end_char, ent.label_)]

                    if (self.cust_ents_dict.get(lineNo, False)):
                        tags = self.cust_ents_dict[lineNo]
                        self.cust_ents_dict[lineNo] = [input_text,tags]

            #for x in self.cust_ents_dict:
            #    print(self.cust_ents_dict[x])

    def overlap(self, interva1, interval2):
        """ Check to see if two intervals overlap. """
        overlap = False
        interva1start = interva1[0]
        interva1end = interva1[1]

        interval2start = interval2[0]
        interval2end = interval2[1]

        if(interval2start >= interva1start and interval2start <= interva1end):
            overlap = True
        elif (interval2end >= interva1start and interval2end <= interva1end):
            overlap = True
        elif (interval2start <= interva1start and interval2end >= interva1end):
            overlap = True
        return overlap

    def get_ner(self,tagLabel):
        """ Extract NER tag"""
        # Clear warning message, if one exists
        self.msg.config(text="")
        try:
            # Get start and end char positions

            lineNo = int(self.text.index("sel.first").split(".")[0])
            lineNo_str = str(lineNo)
            input_text = self.text.get(lineNo_str + ".0", lineNo_str + ".end")

            h_start = int(self.text.index("sel.first").split(".")[1])
            h_end = int(self.text.index("sel.last").split(".")[1])

            if (self.cust_ents_dict.get(lineNo,False)):
                # Check to see if the current line of text matches the one we have in the annotation dictionary.
                # If not, warn the user about the conflict and make the update
                if(input_text != self.cust_ents_dict[lineNo][0]):
                    self.msg.config(text="Warning!! Text in annotation dictionary was different. It has been updated", foreground="red")
                    self.cust_ents_dict[lineNo][0] = input_text

                # Check if selected area overlaps with another NER tag. If it does,
                # delete the existing tag. SpaCy does not allow NER tags to overlap.
                new_ents = []
                for (start, end, label) in self.cust_ents_dict[lineNo][1]:
                    if (not self.overlap([h_start, h_end], [start, end])):
                        new_ents.append((start, end, label))
                self.cust_ents_dict[lineNo][1] = new_ents

                # Add the new NER tag into the dictionary
                self.cust_ents_dict[lineNo][1].append((h_start, h_end, tagLabel))
            else:
                self.cust_ents_dict[lineNo] = [input_text,[(h_start,h_end,tagLabel)]]

            # Highlight the new NER  tag
            self.text.tag_add(tagLabel, "sel.first", "sel.last")
            #self.cust_ents.append((h_start,h_end,tagLabel))

            # Print to make sure it worked. This code needs to be removed after
            # code has been tested.
            self.cust_ents_dict[lineNo][1].sort()
            print(self.cust_ents_dict[lineNo])

        except tk.TclError:
            self.msg.config(text="Warning!! get_ner error.", foreground="red")

    def remove_tag(self):
        """ Delete selection from annotations. """
        # Clear warning message, if one exists
        self.msg.config(text="")
        # if no text is selected then tk.TclError exception occurs
        try:
            selection_line = int(self.text.index("sel.first").split(".")[0])
            selection_start = int(self.text.index("sel.first").split(".")[1])
            selection_end= int(self.text.index("sel.last").split(".")[1])

            #print("selection=",selection_line,selection_start,selection_end)
            #print(self.cust_ents_dict[selection_line])

            # Update annotation to delete tag that was removed
            new_ents = []
            for (start, end, label) in self.cust_ents_dict[selection_line][1]:
                if(not self.overlap([selection_start,selection_end],[start, end])):
                    #print("(start, end, label)=", start, end, label, "Did not overlap")
                    new_ents.append((start, end, label))
            self.cust_ents_dict[selection_line][1] = new_ents

            for tag in self.tags:
                self.text.tag_remove(tag, "sel.first", "sel.last")
        except tk.TclError:
            self.msg.config(text="Warning!! No text was selected.", foreground="red")

        self.cust_ents_dict[selection_line][1].sort()
        print(self.cust_ents_dict[selection_line])

    def ReviewAnnotations(self):
        """
        Review annotations
        """
        # Clear warning message, if one exists
        self.msg.config(text="")

        if self.raw_file is None or self.annotation_file is None:
            self.msg.config(text="Please select both a raw (pdf) file and annotations file (json)", foreground="red")
        else:

                page_num = self.pageEntry.get()
                if not page_num.isdigit():
                    self.msg.config(text="Page number not entered. Value initialized to 1",foreground="red")
                    page_num = 1

                #print("Pg=",page_num)
                #print("Annotation=",self.annotation_file.name)
                #print("Raw file =", self.raw_file.name)
                self.pageNumber = int(page_num)

                # Reset dictionary containing current annotations
                new_cust_ents_dict = {}

                # Load annotation data
                data = json_2_dict(self.annotation_file.name)
                train_data = dict_2_mixed_type(data)
                # Put annotations in a dictionary so we can easily O(1) find if a sentence has been annotated
                for annotation in train_data:
                    sentence = annotation[0]
                    entities = annotation[1]['entities']
                    self.annotation_dict[sentence]= entities

                # Load PDF file
                self.sentences = self.LoadPDF()

                self.text.delete(1.0, tk.END)
                lineNo = 1
                for sent in self.sentences:
                    annotation_exists = self.annotation_dict.get(sent,False)
                    if annotation_exists:
                        # Add sentence to text box
                        self.text.insert(str(lineNo)+".0", sent+'\n')

                        # Update dictionary containing current annotations
                        annot_entry = [sent,annotation_exists]
                        new_cust_ents_dict[lineNo] = annot_entry
                        #self.cust_ents_dict[lineNo][1] = annotation_exists

                        for ent in annotation_exists:
                            start = ent[0]
                            end = ent[1]
                            label = ent[2]
                            if (label in self.tags):
                                self.text.tag_add(label, str(lineNo)+"." + str(start),str(lineNo)+"."+ str(end))
                            else:
                                self.text.tag_add("highlight", str(lineNo)+"." + str(start),str(lineNo)+"."+ str(end))
                    else:
                        self.text.insert(str(lineNo)+".0", sent+'\n')
                    lineNo = lineNo + 1
        self.cust_ents_dict = new_cust_ents_dict

    def highlight_text(self):
        """ Highlight selected text """
        try:
            self.text.tag_add("highlight", "sel.first", "sel.last")
            print(self.text.index("sel.first"), self.text.index("sel.last"))
        except tk.TclError:
            # if no text is selected then tk.TclError exception occurs
            self.msg.config(text="Warning!! No text was selected.",foreground="red")

    def clear_message(self):
        """ Clear warning message"""
        self.msg.config(text="")

    def clear_data(self):
        """ Clear data in text box"""
        # Clear annotations
        self.cust_ents_dict = {}

        # Clear warning message
        self.msg.config(text="")

        # Clear content
        self.text.delete(1.0, tk.END)

    def clear_highlight(self):
        """ Highlight text"""
        for tag in self.tags:
            self.text.tag_remove(tag, "1.0", "end")

        self.msg.config(text="")

    def tag_ner_with_spacy(self, text):
        """ Use SpaCy to identify NER in text"""
        doc = self.nlp_agdata(text)
        return doc

    def file_save(self):
        """ Save current annotation"""
        train_data = []
        file_prefix = self.raw_file.name.split(".")[0]
        pdf_name = self.raw_file.name.split("/")[-1]
        chunk = str(self.pageNumber)
        output_filename = file_prefix+"_p"+chunk+"_td.json"

        if(os.path.isfile(output_filename) and len(self.cust_ents_dict) != 0):
            now = datetime.now()
            date_time = now.strftime("%Y_%m_%d_%H_%M_%S")
            output_filename = file_prefix+"_"+date_time+"_p"+chunk+"_td.json"
            self.msg.config(text="Warning!! Annotation file for this page already exists. A copy created.", foreground="red")

        url = self.urlEntry.get()
        #print("len(self.cust_ents_dict)=",len(self.cust_ents_dict))

        if (len(self.cust_ents_dict) == 0):
            self.msg.config(text="Warning!! No annotations to save.", foreground="red")
        else:
            for lineNo in self.cust_ents_dict:
                text_ents = self.cust_ents_dict[lineNo]
                text_value = text_ents[0].strip()
                ents_value = text_ents[1]
                ents_value.sort()
                ents = {'entities': ents_value}
                #print((text_value, ents))
                train_data.append((text_value, ents))
            train_dict = mixed_type_2_dict(train_data, chunk, pdf_name, url)
            dict_2_json(train_dict, output_filename)


    def nextPage(self):
        """ Load the next page"""
        if (len(self.cust_ents_dict) == 0):
            self.msg.config(text="Warning!! No annotations to save.", foreground="red")
        else:
            self.msg.config(text="")
            # Save current annotation
            self.file_save()

        # Increment page number
        self.pageNumber = self.pageNumber + 1
        self.pageEntry.delete(0, tk.END)
        self.pageEntry.insert(0, str(self.pageNumber))

        # Reset annotation data
        self.annotation_file = None

        # Load data
        self.LoadPage()

    def go(self):
        """This takes no inputs, and sets the GUI running"""
        self.rootWin.mainloop()

    def quit(self):
        """This is a callback method attached to the quit button.
        It destroys the main window, which ends the program"""

        if(self.raw_file is not None):
            # Save current annotation
            self.file_save()

        self.rootWin.destroy()

# Driver code
if __name__ == "__main__":
    myGui = CropNerGUI()
    myGui.go()