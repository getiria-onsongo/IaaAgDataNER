#!/bin/env python3

from agParse import *
from tkinterColorList import  *
from datetime import datetime
from functools import partial
from json2py import *
import os.path
from py2json import *
import PyPDF2
import re
import random
import tkinter as tk
from tkinter import filedialog as fd
from collections import defaultdict
from tkinter.scrolledtext import ScrolledText
import os
import sys

# 1) WRITE A DOCUMENT AND PUT IT INTO GITHUB AND DOCUMENT SCHEMA
# DECISIONS AND VIEWS AND HOW WE WILL LIKELY IMPLEMENT APIs.

# 2) WE NEED TO RESOLVE IS STANDARDIZING THINGS SUCH AS
# ROUGH AWNS OR AWNS ARE ROUGH. NOTE: May be compoud traits
# do not make sense because we need to be able to know
# relationships. See item 3 below. We should look at co-reference resolution.
# It might help. (https://medium.com/huggingface/state-of-the-art-neural-coreference-resolution-for-chatbots-3302365dcf30)

# 3) WE NEED TO GROUP ANNOTATIONS SUCH AS TRAITS INTO CATEGORIES THAT
# MAKE SENSE TO THE USER. RIGHT KNOW WE HAVE "early maturity" AND "winter"
# AS TRAITS WHILE ACCORDING TO THE SPECS WE SHOULD BE RETURNING
# “Maturity” : “early maturity”, “Season”: “winter”

# create a NER GUI class
class CropNerGUI:
    def __init__(self):
        # Create a GUI window
        self.rootWin = tk.Tk()
        #self.rootWin.option_add('*Font', 'Times 24')
        self.rootWin.title("GEMS NER Annotation Tool")
        self.rootWin.geometry('1500x900')

        self.content=[""]

        self.tags=["highlight","default_color_tag","ALAS","CROP","CVAR","JRNL","PATH","PED","PLAN","PPTD","TRAT"]
        self.colors=["gray","black","violet","lawn green","deep sky blue","yellow","red","orange","pink","brown","MediumPurple1"]

        self.tag_colors_buttonID = {}
        self.crop_cnt = {}
        self.cvar_cnt = {}

        # allows default options for model and file for when the GUI is run, the first arg is the model path and the second arg is the file path
        if len(sys.argv) >= 2:
            self.model_dir = sys.argv[1]
        else:
            self.model_dir = None

        if len(sys.argv) >= 3:
            self.raw_file = sys.argv[2]
        else:
            self.raw_file = None


        self.annotation_file = None
        self.sentences = None
        self.annotation_dict = {}
        self.file_extension = None
        self.nlp_agdata = None
        self.nlp_pos = spacy.load("en_core_web_lg") # default spacy model to use for pos

        self.cust_ents_dict = {}

        self.output_file_name = "sample_p0_td.py"
        self.pageNumber=0
        self.line_num = 0
        self.font_size = "16"
        self.page_lines = len(self.content)

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
        self.pretagSelection_btn = tk.Button(self.topframe, text="Pre-Tag Selection", command=partial(self.pre_tag, "Selection"))
        self.pretagSelection_btn.pack(side=tk.LEFT)
        self.pretagPage_btn = tk.Button(self.topframe, text="Pre-Tag Page", command=partial(self.pre_tag, "Page"))
        self.pretagPage_btn.pack(side=tk.LEFT)

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
        self.text = ScrolledText(self.rootWin, height=25, width=140, font = "Times "+self.font_size)
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
        # this code updates colors
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
        self.continue_btn = tk.Button(self.msg_frame, text="Continue", width=10, command=self.continue_func)
        self.continue_btn.pack(side=tk.LEFT)
        self.continue_btn.pack_forget()

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

        self.fontLabel = tk.Label(self.open_frame, text="Font Size:", width=10)
        self.fontLabel.pack(side=tk.LEFT)
        self.fontEntry = tk.Entry(self.open_frame, width=5)
        self.fontEntry.pack(side=tk.LEFT)

        self.annotation_btn = tk.Button(self.open_frame, text="Select Annotation File(JSON)",width=20,command=partial(self.open_file,"json"))
        self.annotation_btn.pack(side=tk.LEFT)

        self.review_btn = tk.Button(self.open_frame, text="Review Annotations", command=self.ReviewAnnotations)
        self.review_btn.pack(side=tk.LEFT)

        # Model frame
        self.model_frame = tk.Frame(self.rootWin)
        self.model_frame.pack(side=tk.TOP,fill="x")

        self.blankLabel_six = tk.Label(self.model_frame, text="     ")
        self.blankLabel_six.pack(side=tk.LEFT)

        self.spacyModel = tk.Label(self.model_frame, text="Spacy Model e.g.,en_core_web_lg  (same model used for training):", width=50,anchor="w")
        self.spacyModel.pack(side=tk.LEFT)
        self.spacyModel = tk.Entry(self.model_frame, width=20)
        self.spacyModel.pack(side=tk.LEFT)

        # Annotation Data
        self.annotation_data_frame = tk.Frame(self.rootWin)
        self.annotation_data_frame.pack(side=tk.TOP,fill="x")

        self.blankLabel_seven = tk.Label(self.annotation_data_frame, text="     ")
        self.blankLabel_seven.pack(side=tk.LEFT)

        self.cropLabel = tk.Label(self.annotation_data_frame, text="Crop Label:", width=10, anchor="w")
        self.cropLabel.pack(side=tk.LEFT)
        self.cropEntry = tk.Entry(self.annotation_data_frame, width=15)
        self.cropEntry.pack(side=tk.LEFT)

        # Font +
        self.font_plus = tk.Button(self.annotation_data_frame, text="Font +",width=10,command=self.font_plus)
        self.font_plus.pack(side = tk.LEFT)

        # Font -
        self.font_minus = tk.Button(self.annotation_data_frame, text="Font -",width=10,command=self.font_minus)
        self.font_minus.pack(side = tk.LEFT)


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
        model = self.spacyModel.get()
        model_name = "en_core_web_lg"
        if len(model) == 0:
            self.spacyModel.delete(0, tk.END)
            self.spacyModel.insert(0, model_name)
        else:
            if(model.lower() == "en_core_web_sm"):
                model_name = "en_core_web_sm"
            elif(model.lower() == "en_core_web_md"):
                model_name = "en_core_web_md"
            self.spacyModel.delete(0, tk.END)
            self.spacyModel.insert(0, model_name)

        self.model_dir = fd.askdirectory()
        self.nlp_agdata = spacy.load(self.model_dir)


    def open_file(self, file_type):
        self.default_file = False
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

        if self.nlp_agdata is None:
            model = self.spacyModel.get()
            model_name = "en_core_web_lg"
            if len(model) == 0:
                self.spacyModel.delete(0, tk.END)
                self.spacyModel.insert(0, model_name)
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
        if self.default_file or type(self.raw_file) is str:
            pdf_file = open(self.raw_file, mode="rb")
        else:
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

            # Extract text from pdf while maintaining layout
            control = TextControl(mode="physical")

            page = self.pdf_document[self.page_number - 1]
            txt = page.text(control=control)
            self.text.insert("1.0",txt)



    def get_pos(self, ent, nlp):
        '''
        Proceses a given entity with rules that use pos tag data to expand the entity span if needed.

        :param ent: entity to possibly expand span of
        :param nlp: spacy model for pos tagging
        :returns: entity, with an expanded span if needed
        '''
        doc = nlp(ent.sent.text)
        if(len(doc[ent.start:ent.end]) > 0):
            current_index = doc[ent.start:ent.end][0].i
            label = ent.label_
            # functions that contain rules to expand the entity's span
            ent = self.adj_combine_noun_ent(doc, current_index, ent, label)
            ent = self.num_combine_ent(doc, current_index, ent, label)
        return ent


    def adj_combine_noun_ent(self, doc, current_index, ent, label):
        '''
        If the first token in an entity is a noun or proper noun, finds all adjectives proceeding the entity and expands the span to contain all of them.

        :param doc: sentence entity belongs to passed through spacy model
        :param current_index: index of first token in the doc
        :param ent: entity to possibly expand span of
        :param label: label of ent
        :returns: entity, which has been expanded if needed
        '''
        if current_index >= 1:
            current = doc[current_index]
            left = doc[current_index-1]
            pos_current = current.pos_
            pos_left = left.pos_

            if pos_current == "NOUN" or pos_current == "PROPN":
                if pos_left == "ADJ":
                        print("Adj expanding...")
                        print("entity: "+ str(ent))
                        i = current_index
                        start_index = ent.start
                        # keeps searching until all adjectives are found, for nouns described by mutiple entities
                        while i >= 1:
                            i = i - 1
                            if doc[i].pos_ == "ADJ":
                                start_index = i
                            else:
                                break
                        first_tok = doc[start_index]
                        ent = doc[first_tok.i:ent.end]
                        ent.label_ = label
                        print("new: " + str(ent))
                        print("label: " + str(ent.label_))
                        print()
        return ent

    def pre_tag(self, selection):
        """ Pre-tag selected content or all the text in text box with NER tags. """
        print("\n\nTagging new pdf...\n")

        # Clear warning message, if one exists
        self.msg.config(text="")
        if self.model_dir is None:
            self.msg.config(text="Warning!! Unable to pre-tag. No NER model selected.", foreground="red")
        # modified this so the error is not displayed when selection is eqaul to page in order for the pre-tag page feature to be able to work properly
        elif len(self.text.tag_ranges("sel")) == 0 and selection == "Selection":
            self.msg.config(text="Warning!! No text was selected.", foreground="red")
        else:
            # Reset annotation dictionary
            self.cust_ents_dict = {}

            # By default, start annotating the first line.
            firstLineNo = 1

            # Get the line number for the beginning and end of the text.
            if (selection == "Selection"):
                firstLineNo = int(self.text.index("sel.first").split(".")[0])
                lastLineIndex = int(self.text.index('sel.last').split(".")[0])
            else:
                # firstLineNo will remain the default value set above.
                lastLineIndex = int(self.text.index('end').split(".")[0])

            #print("firstLineNo,lastLineIndex",firstLineNo,lastLineIndex)
            # Check to see if we have any text. We do not expect a sentence to
            # be less than 5 characters. We will use 5 as the threshold.
            text = self.text.get(str(firstLineNo)+".0", self.text.index('end'))
            if(len(text) < 5):
                self.msg.config(text="Text field appears to be empty. Please load or enter text to Pre-Tag", foreground="red")
            else:
                # Start annotating the line before the selection.
                if(firstLineNo > 1):
                    firstLineNo = firstLineNo - 1
                # Loop through each of these line
                for lineIndex in range(firstLineNo, lastLineIndex, 1):
                    lineNo = lineIndex + 1
                    lineNo_str = str(lineNo)
                    input_text = self.text.get(lineNo_str + ".0", lineNo_str + ".end")
                    doc = self.tag_ner_with_spacy(input_text)
                    for ent in doc.ents:
                        if (ent.label_ in self.tags):
                            # does pos tagging and expaning the ent span if needed
                            ent = self.get_pos(ent, self.nlp_pos)
                            # Add tag to crop or cvar if it is one of the two.
                            ent_value = input_text[ent.start_char:ent.end_char].strip().lower()
                            if(ent.label_ == 'CROP'):
                                self.add_to_dict(self.crop_cnt,ent_value)

                            if (ent.label_ == 'CVAR'):
                                self.add_to_dict(self.cvar_cnt, ent_value)

                            self.text.tag_add(ent.label_, lineNo_str+"." + str(ent.start_char), lineNo_str+"." + str(ent.end_char))
                            if (self.cust_ents_dict.get(lineNo, False)):
                                self.cust_ents_dict[lineNo].append((ent.start_char, ent.end_char, ent.label_))
                            else:
                                self.cust_ents_dict[lineNo] = [(ent.start_char, ent.end_char, ent.label_)]

                    if (self.cust_ents_dict.get(lineNo, False)):
                        tags = self.cust_ents_dict[lineNo]
                        self.cust_ents_dict[lineNo] = [input_text,tags]

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

            # Currently, this tool is designed to do crop and variety based annotation.
            # Named entities will be linked to a crop and a variety. If multiple entries
            # exist, the most common term will be used. If there are ties, the first one
            # encountered will be used.

            # Add tag to crop or cvar if it is one of the two.
            ent_value = input_text[h_start:h_end].lower()
            # Remove leading and trailing spaces if the user selected spaces
            ent_value = ent_value.strip()
            if (tagLabel == 'CROP'):
                self.add_to_dict(self.crop_cnt, ent_value)

            if (tagLabel == 'CVAR'):
                self.add_to_dict(self.cvar_cnt, ent_value)

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

            # Update annotation to delete tag that was removed
            new_ents = []
            for (start, end, label) in self.cust_ents_dict[selection_line][1]:
                if(not self.overlap([selection_start,selection_end],[start, end])):
                    new_ents.append((start, end, label))
                else:
                    entValue = self.cust_ents_dict[selection_line][0][start:end]
                    entValue = entValue.strip().lower()
                    if (label == 'CROP'):
                        self.crop_cnt[entValue] = self.crop_cnt[entValue] - 1
                    if (label == 'CVAR'):
                        self.cvar_cnt[entValue] = self.cvar_cnt[entValue] - 1

            self.cust_ents_dict[selection_line][1] = new_ents

            for tag in self.tags:
                self.text.tag_remove(tag, "sel.first", "sel.last")
        except tk.TclError:
            self.msg.config(text="Warning!! No text was selected.", foreground="red")
        self.cust_ents_dict[selection_line][1].sort()


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
            # Update font size if it was entered
            font_size = self.fontEntry.get()
            if font_size.isdigit():
                self.text['font'] = "Times "+font_size
                self.font_size = font_size

            # Load annotation data
            data = json_2_dict(self.annotation_file.name)
            train_data = dict_2_mixed_type(data)

            # Delete contents and reset line number
            self.text.delete(1.0, tk.END)
            lineNo = 1

            # Review annotation
            for annotation in train_data:
                sentence = annotation[0]
                entities = annotation[1]['entities']
                self.text.insert(str(lineNo)+".0", sentence+'\n')
                for ent in entities:
                    start = ent[0]
                    end = ent[1]
                    label = ent[2]
                    if (label in self.tags):
                        self.text.tag_add(label, str(lineNo)+"." + str(start),str(lineNo)+"."+ str(end))
                    else:
                        self.text.tag_add("highlight", str(lineNo)+"." + str(start),str(lineNo)+"."+ str(end))
                lineNo = lineNo + 1

            # Below is code I had started writing to highlight a PDF file if it has an annotation. Code is not
            # working. Needs to be fixed.

            '''
            page_num = self.pageEntry.get()
            if not page_num.isdigit():
                self.msg.config(text="Page number not entered. Value initialized to 1",foreground="red")
                page_num = 1

            self.pageNumber = int(page_num)

            # Put annotations in a dictionary so we can easily O(1) find if a sentence has been annotated
            for annotation in train_data:
                sentence = annotation[0]
                entities = annotation[1]['entities']
                self.annotation_dict[sentence]= entities



            # Reset dictionary containing current annotations
            new_cust_ents_dict = {}

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
        '''

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

        # Clear cvar and crop entries
        self.cropEntry.delete(0, tk.END)
        self.cvarEntry.delete(0, tk.END)
        self.crop_cnt = {}
        self.cvar_cnt = {}

    def tag_ner_with_spacy(self, text):
        """ Use SpaCy to identify NER in text"""
        #print("Pipeline=",self.nlp_agdata.pipe_names)
        doc = self.nlp_agdata(text)
        return doc

    def continue_func(self):
        """" Add comment """

        # Hide continue button after it was pressed
        self.continue_btn.pack_forget()

        chunk = str(self.pageNumber)
        url = self.urlEntry.get()
        crop = self.cropEntry.get()
        cvar = self.cvarEntry.get()

        train_data = []
        file_prefix = self.raw_file.name.split(".")[0]
        pdf_name = self.raw_file.name.split("/")[-1]

        file_prefix = file_prefix+"_p"+chunk

        if(len(crop) > 0):
            file_prefix = file_prefix+"_crop_"+crop
        if(len(cvar) > 0):
            file_prefix = file_prefix+"_cvar_"+cvar
        output_filename = file_prefix + "_td.json"

        if(os.path.isfile(output_filename) and len(self.cust_ents_dict) != 0):
            now = datetime.now()
            date_time = now.strftime("%Y_%m_%d_%H_%M_%S")
            output_filename = file_prefix+"_"+date_time+"_td.json"
            self.msg.config(text="Warning!! Annotation file with the same name already exists. A copy created.", foreground="red")

        if (len(self.cust_ents_dict) == 0):
            self.msg.config(text="Warning!! No annotations to save.", foreground="red")
        else:
            for lineNo in self.cust_ents_dict:
                text_ents = self.cust_ents_dict[lineNo]
                text_value = text_ents[0].strip()
                ents_value = text_ents[1]
                ents_value.sort()
                ents = {'entities': ents_value}
                train_data.append((text_value, ents))
            train_dict = mixed_type_2_dict(train_data, chunk, pdf_name, url, crop, cvar)
            dict_2_json(train_dict, output_filename)

        # Clear data after saving
        self.remove_all_tags()

    def file_save(self):
        """ Save current annotation"""
        cropOrcvarUpdated = 0

        crop=self.cropEntry.get()
        cvar=self.cvarEntry.get()

        if len(crop) == 0:
            if(self.get_max_dict_value(self.crop_cnt) is not None):
                cropValue = self.get_max_dict_value(self.crop_cnt)
                self.cropEntry.delete(0, tk.END)
                self.cropEntry.insert(0, str(cropValue))
                cropOrcvarUpdated = 1
        if len(cvar) == 0:
            if(self.get_max_dict_value(self.cvar_cnt) is not None):
                cvarValue = self.get_max_dict_value(self.cvar_cnt)
                self.cvarEntry.delete(0, tk.END)
                self.cvarEntry.insert(0, str(cvarValue))
                cropOrcvarUpdated = 1

        if(cropOrcvarUpdated == 1):
            self.continue_btn.pack(side=tk.LEFT)
            self.msg.config(text="Warning!! 'Crop Label' or 'Crop Variety Label' automatically detected. \nMake corrections if necessary then press 'Continue' to Save file", foreground="red",anchor="w")
        else:
            self.continue_func()




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
