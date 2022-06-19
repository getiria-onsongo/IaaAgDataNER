#!/bin/env python3

from agParse import *
from tkinterColorList import  *
from datetime import datetime
from functools import partial
from json2py import *
import os.path
from py2json import *
from pyxpdf import Document, Page, Config
from pyxpdf.xpdf import TextControl
import re
import random
import tkinter as tk
from tkinter import filedialog as fd
from tkinter.scrolledtext import ScrolledText

# 1) WRITE A DOCUMENT AND PUT IT INTO GITHUB AND DOCUMENT SCHEMA
# DECISIONS AND VIEWS AND HOW WE WILL LIKELY IMPLEMENT APIs.

# 2) WE NEED TO RESOLVE IS STANDARDIZING THINGS SUCH AS
# ROUGH AWNS OR AWNS ARE ROUGH. NOTE: Maybe compound traits
# do not make sense because we need to be able to know
# relationships. See item 3 below. We should look at co-reference resolution.
# It might help. (https://medium.com/huggingface/state-of-the-art-neural-coreference-resolution-for-chatbots-3302365dcf30)

# 3) WE NEED TO GROUP ANNOTATIONS SUCH AS TRAITS INTO CATEGORIES THAT
# MAKE SENSE TO THE USER. RIGHT NOW WE HAVE "early maturity" AND "winter"
# AS TRAITS WHILE ACCORDING TO THE SPECS WE SHOULD BE RETURNING
# “Maturity” : “early maturity”, “Season”: “winter”

# 4) Need to start thinking about an ontology

# create a NER GUI class
class CropNerGUI:
    def __init__(self):
        # Create a GUI window.
        self.rootWin = tk.Tk()
        # self.rootWin.option_add('*Font', 'Times 24')
        self.rootWin.title("GEMS NER Annotation Tool")
        self.rootWin.geometry('1500x900')

        self.model_dir = None
        self.content=[""]
        self.tags=["highlight","default_color_tag","ALAS","CROP","CVAR","JRNL","PATH","PED","PLAN","PPTD","TRAT"]
        self.colors=["gray","black","violet","lawn green","deep sky blue","yellow","red","orange","pink","brown","MediumPurple1"]
        self.tag_colors_buttonID = {}

        self.cvar_cnt = {}

        self.raw_file = None
        self.annotation_file = None
        self.chunk = None
        self.pdf_document = None
        self.file_prefix = None
        self.pdf_name = None

        self.sentences = None
        self.annotation_dict = {}
        self.scrollText_line_content_index = {} # Store index of characters in this line
        self.file_extension = None
        self.nlp_agdata = None

        self.cust_ents_dict = {}

        self.output_file_name = "sample_p0_td.py"
        self.page_number=0
        self.line_num = 0
        self.font_size = "16"
        self.num_page_lines = len(self.content)

        self.topframe = tk.Frame(self.rootWin)
        self.topframe.pack(side=tk.TOP,fill="x")

        # NOTE: A partial function is created from another function, where some of the parameters are fixed.
        # In the instance below, we want to call the function self.get_ner (which takes a single input) several
        # times but each time we pass it a different value depending on the button that was clicked. If the ALAS
        # button is clicked, we want to pass the text "ALAS" but if the "CROP" button was clicked we want to pass the
        # text CROP. So, partial(self.get_ner, "ALAS") is the same as self.get_ner("ALAS")
        self.blankLabel_one = tk.Label(self.topframe, text="   ")
        self.blankLabel_one.pack(side=tk.LEFT)

        # Create a dictionary with a tag as key and [color, buttonID] as value.
        # This will make it easy to retrieve the color for a tag. The loop does the equivalent
        # of
        # self.tag_colors["highlight"] = ["gray", buttonID]
        # in an iteration
        for i in range(len(self.tags)):
            tagValue = self.tags[i]
            colorValue = self.colors[i]
            # We don't need to create a button for the first two tags
            if i < 2:
                self.tag_colors_buttonID[tagValue] = [colorValue, None]
            else:
                # Create button
                # self.alas_btn = tk.Button(self.topframe, highlightbackground="violet",text="ALAS", command=partial(self.get_ner, "ALAS"))
                btn = tk.Button(self.topframe, highlightbackground=colorValue,text=tagValue, command=partial(self.get_ner, tagValue))
                btn.pack(side=tk.LEFT)
                self.tag_colors_buttonID[tagValue] = [colorValue, btn]

        self.spaceLabel = tk.Label(self.topframe, text="    ", width=17)
        self.spaceLabel.pack(side=tk.LEFT)
        self.clearTag_btn = tk.Button(self.topframe, text="Remove-Tag", command=partial(self.remove_tag))
        self.clearTag_btn.pack(side=tk.LEFT)
        self.pretagPage_btn = tk.Button(self.topframe, text="Pre-Tag Page", command=partial(self.pre_tag, "page"))
        self.pretagPage_btn.pack(side=tk.LEFT)
        self.pretagSelection_btn = tk.Button(self.topframe, text="Pre-Tag Selection", command=partial(self.pre_tag, "selection"))
        self.pretagSelection_btn.pack(side=tk.LEFT)

        self.cust_ent_frame = tk.Frame(self.rootWin)
        self.cust_ent_frame.pack(side=tk.TOP,fill="x")
        self.blankLabel_two = tk.Label(self.cust_ent_frame, text="   ")
        self.blankLabel_two.pack(side=tk.LEFT)

        self.edit_ent_frame = tk.Frame(self.rootWin)
        self.edit_ent_frame.pack(side=tk.TOP,fill="x")
        self.traitLabel = tk.Label(self.edit_ent_frame, text="Enter Entity Label:", width=20)
        self.traitLabel.pack(side=tk.LEFT)
        self.traitEntry = tk.Entry(self.edit_ent_frame, width=10)
        self.traitEntry.pack(side=tk.LEFT)

        # Add entity button
        self.add_ent_btn = tk.Button(self.edit_ent_frame, text="Add Entity", width=10, command=self.add_ent)
        self.add_ent_btn.pack(side=tk.LEFT)

        # Remove entity button
        self.remove_ent_btn = tk.Button(self.edit_ent_frame, text="Remove Entity", width=10, command=self.remove_ent)
        self.remove_ent_btn.pack(side=tk.LEFT)

        # adding the text: Note, height defines height if widget in lines based in font size
        self.text = ScrolledText(self.rootWin, height=25, width=140, font = "Times "+self.font_size, wrap='word')
        self.text.insert(tk.END, self.content[self.line_num])
        self.text.focus_force()
        self.text.pack(side=tk.TOP)

        self.text.tag_configure("highlight", foreground="black", background="gray")
        # We need to repeat the configuration on the line above for all the tags. Except we will
        # not change the foreground. It is the equivalent of
        #
        # self.text.tag_configure("ALAS", background="violet")
        #
        # in one iteration but instead of 10 statements we will use a loop
        for tag, color_buttonID in self.tag_colors_buttonID.items():
            color = color_buttonID[0]
            if(tag != "highlight"):
                # One iteration does the equivalent of:
                # self.text.tag_configure("ALAS", background="violet")
                self.text.tag_configure(tag, background=color)

        self.bottom_frame = tk.Frame(self.rootWin)
        self.bottom_frame.pack(side=tk.TOP,fill="x")

        self.blankLabel_three = tk.Label(self.bottom_frame, text="   ")
        self.blankLabel_three.pack(side=tk.LEFT)
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
        self.clear_btn = tk.Button(self.bottom_frame, text="Remove All Tags",width=20, command=self.remove_all_tags)
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
        self.msg_frame.pack(side=tk.TOP)

        # Label to display messages
        self.msg = tk.Label(self.msg_frame, text="", padx=5, pady=5)
        self.msg.pack(side=tk.LEFT)

        # Continue button
        self.continue_btn = tk.Button(self.msg_frame, text="Continue", width=10, command=partial(self.continue_func, "save"))
        self.continue_btn.pack(side=tk.LEFT)
        self.continue_btn.pack_forget()

        # Continue button
        self.overwrite_btn = tk.Button(self.msg_frame, text="Overwrite", width=10,command=partial(self.continue_func, "save"))
        self.overwrite_btn.pack(side=tk.LEFT)
        self.overwrite_btn.pack_forget()

        self.copy_btn = tk.Button(self.msg_frame, text="Create Copy", width=10, command=partial(self.continue_func, "copy"))
        self.copy_btn.pack(side=tk.LEFT)
        self.copy_btn.pack_forget()

        # Meta Data Frame
        self.metadata_frame = tk.Frame(self.rootWin)
        self.metadata_frame.pack(side=tk.TOP)

        self.ann_file_label = tk.Label(self.metadata_frame, text="Annotation File Name (json):", width=20, anchor="w")
        self.ann_file_label.pack(side=tk.LEFT)
        self.ann_file_label.pack_forget()
        self.ann_file_entry = tk.Entry(self.metadata_frame, width=30)
        self.ann_file_entry.pack(side=tk.LEFT)
        self.ann_file_entry.pack_forget()

        self.source_label = tk.Label(self.metadata_frame, text="PDF/Text URL (source):", width=15, anchor="w")
        self.source_label.pack(side=tk.LEFT)
        self.source_label.pack_forget()
        self.source_entry = tk.Entry(self.metadata_frame, width=30)
        self.source_entry.pack(side=tk.LEFT)
        self.source_entry.pack_forget()

        # Frame for selecting
        self.open_frame = tk.Frame(self.rootWin)
        self.open_frame.pack(side=tk.TOP,fill="x")

        self.blankLabel_five = tk.Label(self.open_frame, text="   ")
        self.blankLabel_five.pack(side=tk.LEFT)
        # open file button
        self.open_button = tk.Button(self.open_frame,text='Select Raw Data File(PDF)',width=18,command=partial(self.open_file,"pdf"))
        self.open_button.pack(side=tk.LEFT)

        self.nermodel_button = tk.Button(self.open_frame, text='Select NER model folder', width=18,command=self.get_nermodel_dir)
        self.nermodel_button.pack(side=tk.LEFT)

        self.pageLabel = tk.Label(self.open_frame, text="Raw Data File Page Num:",width=18)
        self.pageLabel.pack(side=tk.LEFT)
        self.pageEntry = tk.Entry(self.open_frame, width=5)
        self.pageEntry.pack(side=tk.LEFT)

        self.annotation_btn = tk.Button(self.open_frame, text="Select Annotation File(JSON)",width=20,command=partial(self.open_file,"json"))
        self.annotation_btn.pack(side=tk.LEFT)

        # Font +
        self.font_plus = tk.Button(self.open_frame, text="Font +", width=10, command=self.font_plus)
        self.font_plus.pack(side=tk.LEFT)

        # Font -
        self.font_minus = tk.Button(self.open_frame, text="Font -", width=10, command=self.font_minus)
        self.font_minus.pack(side=tk.LEFT)

        # Model frame
        self.model_frame = tk.Frame(self.rootWin)
        self.model_frame.pack(side=tk.TOP,fill="x")

        self.blankLabel_six = tk.Label(self.model_frame, text="     ")
        self.blankLabel_six.pack(side=tk.LEFT)

        self.spacyModel_label = tk.Label(self.model_frame, text="Spacy Model e.g.,en_core_web_lg:", width=25,anchor="w")
        self.spacyModel_label.pack(side=tk.LEFT)
        self.spacyModel_entry = tk.Entry(self.model_frame, width=20)
        self.spacyModel_entry.pack(side=tk.LEFT)


    def font_plus(self):
        """ Add documentation"""
        self.font_size = str(int(self.font_size) + 1)
        self.text['font'] = "Times "+self.font_size
        

    def font_minus(self):
        """ Add documentation"""
        self.font_size = str(int(self.font_size) - 1)
        self.text['font'] = "Times "+self.font_size

    def get_max_dict_value(self, dictionary):
        """ Add documentation"""
        maxKey = None
        maxValue = 0
        for key, value in dictionary.items():
            if value > maxValue:
                maxKey = key
                maxValue = value
        return maxKey

    def add_to_dict(self, dictionary, ent_value):
        """ Add documentation"""
        if (dictionary.get(ent_value, False)):
            dictionary[ent_value] = dictionary[ent_value] + 1
        else:
            dictionary[ent_value] = 1

    def remove_ent(self):
        """ Add documentation"""
        ent_label = self.traitEntry.get().upper()
        color = self.tag_colors_buttonID[ent_label][0]
        ent_btn = self.tag_colors_buttonID[ent_label][1]
        ent_btn.pack_forget()
        # Remove elements from dictionary and arrays
        self.tag_colors_buttonID.pop(ent_label)
        self.colors.remove(color)
        self.tags.remove(ent_label)

    def add_ent(self):
        """ Add documentation"""
        ent_label = self.traitEntry.get().upper()
        if ent_label in self.tags:
            self.msg.config(text="Warning!! Cannot add entity. Another entity with the same label already exists!", foreground="red")
        else:
            # The code below select a color from color_list which is defined in tkinterColorList.py
            # If it loops through the lenth of the colors in color_list and does not find a color
            # that has not already been used, it generates a random color.
            color = None
            n = len(color_list)
            for i in range(n):
                # Randomly pick a color. This will hopefully get one that contrasts well with existing colors.
                i_color = color_list[random.randint(0, n)]
                # Check to see of the color selected has not been used
                if i_color not in self.colors:
                    color = i_color
                    break
            # Note, because we are selecting colors randomly from color_list, there is a chance we will not
            # find a color that has not already been used. This can happen if by chance we keep randomnly
            # selecting colors that have been used. If this happens, just create a random color.
            if(color is None):
                color = "#" + ("%06x" % random.randint(0, 16777215))
            self.colors.append(color)
            self.tags.append(ent_label)
            btn = tk.Button(self.cust_ent_frame, highlightbackground=color, text=ent_label,command=partial(self.get_ner, ent_label))
            btn.pack(side=tk.LEFT)
            self.text.tag_configure(ent_label, background=color)
            self.tag_colors_buttonID[ent_label] = [color, btn]


    def get_nermodel_dir(self):
        """ Add documentation"""
        model = self.spacyModel_entry.get()
        model_name = "en_core_web_lg"
        if len(model) == 0:
            self.spacyModel_entry.delete(0, tk.END)
            self.spacyModel_entry.insert(0, model_name)
        else:
            if(model.lower() == "en_core_web_sm"):
                model_name = "en_core_web_sm"
            elif(model.lower() == "en_core_web_md"):
                model_name = "en_core_web_md"
            self.spacyModel_entry.delete(0, tk.END)
            self.spacyModel_entry.insert(0, model_name)
        self.model_dir = fd.askdirectory()
        self.nlp_agdata = spacy.load(self.model_dir)


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
            self.ReviewAnnotations()
        elif file_type == "pdf":
            self.raw_file=f
            self.LoadPage()

        else:
            self.msg.config(text="Warning!! Please select a valid (pdf or json) file.", foreground="red")

    def LoadModel(self):
        """
        Load spacy model
        """
        if self.nlp_agdata is None:
            model = self.spacyModel_entry.get()
            model_name = "en_core_web_lg"
            if len(model) == 0:
                self.spacyModel_entry.delete(0, tk.END)
                self.spacyModel_entry.insert(0, model_name)
            else:
                if (model.lower() == "en_core_web_sm"):
                    model_name = "en_core_web_sm"
                elif (model.lower() == "en_core_web_md"):
                    model_name = "en_core_web_md"

            if self.model_dir is not None:
                self.nlp_agdata = spacy.load(self.model_dir)
            else:
                self.nlp_agdata = spacy.load(model_name)


            self.nlp_agdata.add_pipe("compound_trait_entities", after='ner')


    def LoadPDF(self):
        """ Get data from PDF file"""
        if self.raw_file is None:
            self.msg.config(text="No raw data file has been selected. Please select a file to load.", foreground="red")

        self.file_prefix = self.raw_file.name.split(".")[0]
        self.pdf_name = self.raw_file.name.split("/")[-1]
        self.pdf_document = Document(self.raw_file.name)

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

            page_num = self.pageEntry.get()
            if not page_num.isdigit():
                self.msg.config(text="Page number not entered. Value initialized to 1", foreground="red")
                self.page_number = 1
                self.pageEntry.delete(0,tk.END)
                self.pageEntry.insert(0, str(self.page_number))
            else:
                self.page_number = int(page_num)

            self.chunk=self.page_number
            # Delete contents
            self.text.delete(1.0, tk.END)

            # Load PDF file
            if self.pdf_document is None:
                self.LoadPDF()

            # Extract text from pdf while maintaining layout
            control = TextControl(mode="physical")

            page = self.pdf_document[self.page_number - 1]
            txt = page.text(control=control)
            self.text.insert("1.0",txt)



    def update_scrollText_line_content_index(self):
        """ Add documentation"""
        # Trying to figure out where entities are on scrollTextbox is a little tricky because tKinter uses newline
        # characters to split text. Here we are keeping track of how many characters appear before a line in the
        # GUI. This should make it easier to figure out where a token is given its
        # start and end indices. Given (Steveland/Luther//Wintermalt 1001 1029 PED)  named entity, it is 1001, 1029
        input_text = self.text.get(1.0, "end")
        lines = input_text.splitlines()
        self.num_page_lines = len(lines)
        line_no = 1
        num_char = 0
        for line in lines:
            line_len = len(line)
            interval = (num_char, num_char + line_len)
            self.scrollText_line_content_index[line_no] = interval
            num_char = num_char + line_len + 1  # The 1 we are adding is for newline character
            line_no = line_no + 1

    def highlight_ent(self, start_char, end_char, label):
        """ Add documentation """
        line_start = -1
        char_start = -1
        line_end = -1
        char_end = -1
        # Loop through lines in the text field and find where this tag is.
        for key, value in self.scrollText_line_content_index.items():
            (start, end) = value
            if start_char >= start:
                line_start = key
                char_start = start_char - start
            if end_char <= end and line_start > 0:
                line_end = key
                ent_num_char = end_char - start_char
                if line_start == line_end:
                    char_end = char_start + ent_num_char
                else:
                    char_end = end_char - start
                break

        self.text.tag_add(label, str(line_start) + "." + str(char_start), str(line_end) + "." + str(char_end))

    def pre_tag(self,selection):
        """ Pre-tag selected content or all the text in text box with NER tags. """
        input_text = None
        # Clear warning message, if one exists
        self.msg.config(text="")
        if self.model_dir is None:
            self.msg.config(text="Warning!! Unable to pre-tag. No NER model selected.", foreground="red")
        else:
            input_text = None
            # Get page number
            page_num = self.pageEntry.get()
            if not page_num.isdigit():
                self.msg.config(text="Page number not entered. Page 1 in PDF loaded", foreground="red")
                page_num = 1
            self.page_number = int(page_num)
            self.chunk = self.page_number

            if (selection == "selection"):
                input_text =  self.text.get("sel.first", "sel.last")
            else:
                if self.pdf_document is None:
                    self.msg.config(text="Warning!! No PDF was detected. Will attempt to load PDF ", foreground="red")
                    self.LoadPDF()

                # Extract text from pdf while maintaining layout
                control = TextControl(mode="physical")

                page = self.pdf_document[self.page_number - 1]
                input_text = page.text(control=control)

            self.text.delete(1.0, tk.END)
            self.text.insert("1.0", input_text)

            # Reset annotation dictionary
            self.cust_ents_dict = {}

            # Update variable that holds number of lines in textbox. You need this for
            # the function highlight_ent to work
            self.update_scrollText_line_content_index()
            #for key, value in self.scrollText_line_content_index.items():
            #    print(key,":",value)

            doc = self.tag_ner_with_spacy(input_text)

            for ent in doc.ents:
                if (ent.label_ in self.tags): # NER is in our list of custom tags
                    # index = self.tags.index(ent.label_) # Find index for an element in a list
                    self.highlight_ent(ent.start_char, ent.end_char, ent.label_)
                    if self.cust_ents_dict.get(self.page_number, False):
                        self.cust_ents_dict[self.page_number].append((ent.start_char, ent.end_char, ent.label_))
                    else:
                        self.cust_ents_dict[self.page_number] = [(ent.start_char, ent.end_char, ent.label_)]
                

            if (self.cust_ents_dict.get(self.page_number, False)):
                tags = self.cust_ents_dict[self.page_number]
                self.cust_ents_dict[self.page_number] = [input_text, tags]

    def overlap(self, interva1, interval2):
        """ Check to see if two intervals overlap. """
        overlap = False
        interva1start = interva1[0]
        interva1end = interva1[1]

        interval2start = interval2[0]
        interval2end = interval2[1]

        if (interval2start >= interva1start and interval2start <= interva1end):
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
            # Get text
            input_text = input_text = self.text.get(1.0, "end")

            # Update variable that holds number of lines in textbox.
            self.update_scrollText_line_content_index()

            # Get start and end char positions
            h_start = int(self.text.index("sel.first").split(".")[1])
            h_end = int(self.text.index("sel.last").split(".")[1])

            line_no = int(self.text.index("sel.first").split(".")[0])
            ent_char_start = self.scrollText_line_content_index[line_no][0] + h_start
            ent_char_end = self.scrollText_line_content_index[line_no][0] + h_end

            print("self.scrollText_line_content_index[line_no]=", self.scrollText_line_content_index[line_no])
            print("h_start,h_end=",h_start,h_end)
            print("ent_char_start,ent_char_end",ent_char_start,ent_char_end)


            if self.cust_ents_dict.get(self.chunk,False):
                # Check to see if the current text matches the one we have in the annotation dictionary.
                # If not, warn the user about the conflict and make the update
                if input_text != self.cust_ents_dict[self.chunk][0]:
                    self.msg.config(text="Warning!! Text in annotation dictionary was different. It has been updated",
                                    foreground="red")
                    self.cust_ents_dict[self.chunk][0] = input_text

                # Check if selected area overlaps with another NER tag. If it does,
                # delete the existing tag. SpaCy does not allow NER tags to overlap.
                new_ents = []
                for (start, end, label) in self.cust_ents_dict[self.chunk][1]:
                    if not self.overlap([ent_char_start, ent_char_end], [start, end]):
                        new_ents.append((start, end, label))
                self.cust_ents_dict[self.chunk][1] = new_ents

                # Add the new NER tag into the dictionary
                self.cust_ents_dict[self.chunk][1].append((ent_char_start,ent_char_end, tagLabel))
            else:
                self.cust_ents_dict[self.chunk] = [input_text, [(ent_char_start,ent_char_end, tagLabel)]]

            # Highlight the new NER  tag
            self.text.tag_add(tagLabel, "sel.first", "sel.last")

        except tk.TclError:
            self.msg.config(text="Warning!! get_ner error.", foreground="red")
        print("ENTs=",self.cust_ents_dict[self.chunk][1])

    def remove_tag(self):
        """ Delete selection from annotations. """
        # Clear warning message, if one exists
        self.msg.config(text="")

        selection_line = int(self.text.index("sel.first").split(".")[0])
        tmp_selection_start = int(self.text.index("sel.first").split(".")[1])
        tmp_selection_end = int(self.text.index("sel.last").split(".")[1])
        selection_start =  self.scrollText_line_content_index[selection_line][0] + tmp_selection_start
        selection_end = self.scrollText_line_content_index[selection_line][0] + tmp_selection_end

        new_ents = []
        overlapping_tags = []
        input_text = self.cust_ents_dict[self.chunk][0]
        entities = self.cust_ents_dict[self.chunk][1]

        # Loop through tags and find ones that overlap with selected region and remove them.
        for (start, end, label) in entities:
            if not self.overlap([selection_start,selection_end],[start, end]):
                new_ents.append((start, end, label))
            else:
                overlapping_tags.append(label)
        if len(overlapping_tags) == 0:
            self.msg.config(text="Warning!! It appears the region you selected ("+str(selection_start)+
                                 "-"+str(selection_end)+" did not overlap with a tag.", foreground="red")
        else:
            for tag in overlapping_tags:
                self.text.tag_remove(tag, "sel.first", "sel.last")

        new_ents.sort()
        self.cust_ents_dict[self.chunk] = [input_text, new_ents]


    def show_ents(doc):
        if doc.ents:
            for ent in doc.ents:
                print(ent.text + ' - ' + str(ent.start_char) + ' - ' + str(ent.end_char) + ' - ' + ent.label_ + ' - ' +
                      str(spacy.explain(ent.label_)))
            else:
                 print('No named entities found.')

    def ReviewAnnotations(self):
        """
        Review annotations
        """
        # Clear warning message, if one exists
        self.msg.config(text="")
        # self.raw_file is None or self.annotation_file is None:
        if self.annotation_file is None:
            self.msg.config(text="Please select an annotations file (json)", foreground="red")
        else:
            # Load annotation data
            data = json_2_dict(self.annotation_file.name)
            train_data = dict_2_mixed_type(data)
            """
            doc = data['doc']
            url = data['url']
            """
            self.chunk = int(data['chunk'])
            self.page_number = self.chunk

            # Empty text box so we can load annotations
            self.text.delete(1.0, tk.END)

            # Load  annotation
            print("size=",len(train_data))
            annotation = train_data[0]
            self.cust_ents_dict[self.chunk] = [annotation[0],annotation[1]['entities']]
            sentence = annotation[0]
            entities = annotation[1]['entities']

            self.text.insert("1.0", sentence + '\n')

            # Update variable that holds number of lines in textbox. You need this update
            # for highlight_ent to work
            self.update_scrollText_line_content_index()

            for ent_val in entities:
                self.highlight_ent(ent_val[0],ent_val[1], ent_val[2])

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

    def remove_all_tags(self):
        """ Highlight text"""
        for tag in self.tags:
            self.text.tag_remove(tag, "1.0", "end")

        # Clear annotations
        self.cust_ents_dict = {}

        # Clear warning message
        self.msg.config(text="")

    def tag_ner_with_spacy(self, text):
        """ Use SpaCy to identify NER in text"""
        #print("Pipeline=",self.nlp_agdata.pipe_names)
        doc = self.nlp_agdata(text)
        return doc

    def continue_func(self, save_choice):
        """" Add comment """
        filename = None
        if save_choice == 'copy':
            file_prefix = self.raw_file.name.split(".")[0]
            now = datetime.now()  # current date and time
            date_time = now.strftime("%m_%d_%Y_%H_%M_%S")
            filename = file_prefix + "_" + date_time + ".json"
        else:
            if isinstance(self.annotation_file, str):
                filename = self.annotation_file
            else:
                filename = self.annotation_file.name

        url = self.source_entry.get()

        if len(self.cust_ents_dict) == 0:
            self.msg.config(text="Warning!! No annotations to save.", foreground="red")
        else:
            input_text = self.cust_ents_dict[self.chunk][0]
            entities = self.cust_ents_dict[self.chunk][1]

            ann_train_dict = mixed_type_2_dict([(input_text,{'entities': entities})], self.chunk, self.pdf_name, url)
            dict_2_json(ann_train_dict, filename)

        # Hide buttons
        self.overwrite_btn.pack_forget()
        self.continue_btn.pack_forget()
        self.copy_btn.pack_forget()
        self.ann_file_label.pack_forget()
        self.ann_file_entry.pack_forget()
        self.source_label.pack_forget()
        self.source_entry.pack_forget()

        # Clear data after saving
        self.remove_all_tags()

    def file_save(self):
        """ Save current annotation"""
        # Check to see if user is trying to overwrite a file
        if self.annotation_file is None:
            # Check to make sure value has been initialized
            if self.file_prefix is None:
                self.file_prefix = "annotation_file"
            self.annotation_file = self.file_prefix + "_pg" + str(self.page_number) + ".json"
            if os.path.isfile(self.annotation_file):
                self.msg.config( text="WARNING!! You are about to overwrite your annotation file. Click 'Overwrite' to overwite or 'Create Copy' \n and optionally enter meta-data in the fields provided.",foreground="red", anchor="w")
                self.overwrite_btn.pack(side=tk.LEFT)
                self.copy_btn.pack(side=tk.LEFT)
            else:
                self.msg.config(text="The file name shown in the text box will be used. Edit the name and optionally enter meta-data in the fields provided and click 'Continue' to Save.", foreground="red",anchor="w")
                self.continue_btn.pack(side=tk.LEFT)

        else:
            self.msg.config(text="WARNING!! You are about to overwrite your annotation file. Click 'Overwrite' to overwite or 'Create Copy' \n and optionally enter meta-data in the fields provided.",foreground="red", anchor="w")
            self.overwrite_btn.pack(side=tk.LEFT)
            self.copy_btn.pack(side=tk.LEFT)

        self.ann_file_entry.delete(0, tk.END)
        if isinstance(self.annotation_file, str):
            self.ann_file_entry.insert(0, self.annotation_file)
        else:
            self.ann_file_entry.insert(0, self.annotation_file.name)

        self.ann_file_label.pack(side=tk.LEFT)
        self.ann_file_entry.pack(side=tk.LEFT)
        self.source_label.pack(side=tk.LEFT)
        self.source_entry.pack(side=tk.LEFT)

    def nextPage(self):
        """ Load the next page"""
        if (len(self.cust_ents_dict) == 0):
            self.msg.config(text="Warning!! No annotations to save.", foreground="red")
        else:
            self.msg.config(text="")
            # Save current annotation
            # Uncomment this for now. Initially it seemed like a good idea but there are a lot of
            # Instances where a user might not want to save annotations when they click next page
            # self.file_save()

        # Increment page number
        self.page_number = self.page_number + 1
        self.pageEntry.delete(0, tk.END)
        self.pageEntry.insert(0, str(self.page_number))

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

        '''
        # This seemed like a good idea to save the annotation file everytime 
        # the application quit, just in case the user forgot to save. However, 
        # when testing a ton of unnecessary files were being generated. We will comment
        # this out for now and if this features becomes necessary in the future, we can 
        # just uncomment.  
        if(self.raw_file is not None):
            # Save current annotation
            self.file_save()
        '''

        self.rootWin.destroy()

# Driver code
if __name__ == "__main__":
    myGui = CropNerGUI()
    myGui.go()
