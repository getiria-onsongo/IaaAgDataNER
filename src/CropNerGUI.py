#!/bin/env python3
import spacy.tokens

from agParse import *
from tkinterColorList import *
from datetime import datetime
from functools import partial
from json2py import *
import os.path
from py2json import *
from pyxpdf import Document, Page, Config
from pyxpdf.xpdf import TextControl
import random
import tkinter as tk
from tkinter import filedialog as fd
from tkinter.scrolledtext import ScrolledText

# TODO: Even though users can add their own named entities, the tool does not recognize these user
# defined named entities once they've quit the application. Basically, when a user customizes the GUI
# the changes do not persist across sessions. Make customized additions to the GUI persistent across sessions.
# One approach to implementing this would be to add a starting prompt that asks a user if they want to
# 1) Annotate crop data 2) Annotate user data or 3) Review annotations. If they choose 2 or 3, build the GUI by
# first scanning their annotations to determine what Named Entity tags (e.g., ALAS) to include in the GUI

# 1) WE NEED TO RESOLVE STANDARDIZING THINGS SUCH AS
# ROUGH AWNS OR AWNS ARE ROUGH. NOTE: Maybe compound traits
# do not make sense because we need to be able to know
# relationships. We should look at co-reference resolution.
# See: https://medium.com/huggingface/state-of-the-art-neural-coreference-resolution-for-chatbots-3302365dcf30
#
# 2) WE NEED TO GROUP ANNOTATIONS SUCH AS TRAITS INTO CATEGORIES THAT
# MAKE SENSE TO THE USER. RIGHT NOW WE HAVE "early maturity" AND "winter"
# AS TRAITS WHILE ACCORDING TO THE SPECS WE SHOULD BE RETURNING
# “Maturity” : “early maturity”, “Season”: “winter”

# 3) Need to start thinking about an ontology


# Create NER GUI class
class CropNerGUI:
    """ A class used to represent NER tagging GUI window.


    ...
    Attributes
    ----------
    self.rootWin : tk.Tk()
        tKinter class that represents the main window
    self.rootWin.title : self.rootWin.title()
        Title for the GUI
    self.rootWin.geometry : self.rootWin.geometry()
        Size for the main window
    self.model_dir : str
        Path to language model directory
    self.tags : list
        Agricultural data NER tags.
    self.colors : list
        Colors used to highlight tags in self.tags. Should have the same number of entries as self.tags. NER tag in
        self.tags[i] will be highlighted using color self.colors[i]
    self.self.tag_colors_buttonID : dict
        Dictionary with a tag as key and [color, buttonID] as value
    self.raw_file : _io.TextIOWrapper
        PDF or text file selected by user using the GUI
    self.annotation_file : _io.TextIOWrapper
        Annotation file selected by user using the GUI
    self.chunk : int
        Current logical partition of the document being annotated. By default, this is the page number because it is
        natural to annotate a document in page increments.
    self.pdf_document : pyxpdf.Document
        PDF to be annotated that was selected using GUI
    self.pdf_name : str
        Name of the pdf/text file being annotated. e.g., BarCvDescLJ11.pdf
    self.file_prefix : str
        File path prefix (minus file type) e.g., for BarCvDescLJ11.pdf path prefix is Data/DavisLJ11/BarCvDescLJ11
    self.scrolled_text_line_content_index : dict
        Contains index position of characters in a given line. Key = line number tuple is index of first and last
        characters respectively. {2: (114, 228)} = line 2 has characters from index 114 to index 228
    self.nlp_agdata : class (spacy.lang)
        spaCy language model. Defaults to en_core_web_lg if not specified
    self.cust_ents_dict : dict
        Contains NER tag annotations. key = chunk number, values = entities
    self.page_number : int
        Current page number

    NOTE: Though the widgets are global variables, we will not document them here. Most are self-evident. We have
    added inline comments in the code itself.

    Methods
    -------
    font_plus(self)
        Increase font size for text in ScrolledText (text box).
    font_minus(self)
        Decrease font size for text in ScrolledText (text box).
    add_ent(self)
        Add a user defined named entity to the application.
    remove_ent(self)
        Remove a user defined named entity from the application.
    get_ner_model_dir(self)
        Select a folder containing spaCy nlp pipeline.
    open_file(self, file_type: str)
        Open a file (pdf/text) to be annotated or an annotation file (json) to be reviewed. selected using the GUI.
    load_pdf(self)
        Load  PDF file.
    load_page(self)
        Load contents of a PDF or text file into text box.
    update_scrolled_text_line_content_index(self)
        Populate the dictionary self.scrolled_text_line_content_index with position indices for the first and
        last characters in each line in the text box.
    highlight_ent(self, start_char: int, end_char: int, label: str)
        Given the start index and end index of a named entity, highlight it in the text box.
    pre_tag(self, selection: str)
         Pre-tag selected content or all the text in text box with NER tags.
    overlap(self, interval_one: list, interval_two: list) -> bool
        Check to see if two intervals overlap.
    get_selected_interval(self) -> tuple
        Determines the index of the first and last characters (char_start, char_end) selected by the user.
    get_ner(self, tag_label: str)
        Tag a piece of text that has been selected as a named entity.
    remove_tag(self)
        Untag a piece of text that was classified as a named entity.
    review_annotations(self)
        Load a json file containing annotations and review it.
    clear_message(self)
        Clear warning message
    clear_data(self)
        Clear data in text box and dictionary containing annotations.
    remove_all_tags(self)
        Remove all the NER tags on text loaded in the text box.
    tag_ner_with_spacy(self, text: str) -> spacy.tokens.Doc
        Use NLP pipeline to identify named entities in the text.
    continue_func(self, save_choice: str)
        Continue the process of either saving annotation in a new file or overwriting an existing file.
    file_save(self)
        Save current annotation.
    next_page(self)
        Load the next page.
    go(self)
        Start running the GUI running.
    quit(self)
        Callback method attached to the quit button.
    """

    def __init__(self):
        """ Initialize  CropNerGU object"""

        self.rootWin = tk.Tk()
        self.rootWin.title("GEMS NER Annotation Tool")
        self.rootWin.geometry('1250x700')
        self.model_dir = None
        self.tags=["ALAS", "CROP", "CVAR", "JRNL", "PATH", "PED", "PLAN", "PPTD", "TRAT"]
        self.colors=["violet", "lawn green", "deep sky blue", "yellow", "red", "orange","pink", "brown",
                     "MediumPurple1"]
        self.tag_colors_buttonID = {}
        self.raw_file = None
        self.annotation_file = None
        self.chunk = None
        self.pdf_document = None
        self.pdf_name = None
        self.file_prefix = None
        self.scrolled_text_line_content_index = {}
        self.nlp_agdata = None
        self.cust_ents_dict = {}
        self.page_number = 0

        # ----------------------- Widgets for GUI start here.
        # Default font size for text in ScrolledText. Should be a string format
        # for a number e.g., '16'
        self.font_size = "16"

        # Top level frame for GUI
        self.top_frame = tk.Frame(self.rootWin)
        self.top_frame.pack(side=tk.TOP, fill="x")

        # Blank label with 3 empty spaces used for formatting. Ensures there is some
        # space between the edge and first widget e.g., button
        self.blank_label_one = tk.Label(self.top_frame, text="   ")
        self.blank_label_one.pack(side=tk.LEFT)

        # The loops below is used to create buttons the user will click to tag words/phrases
        #
        # Just inside the for loop, populate a dictionary with a tag as key and [color, buttonID] as value. This will
        # make it easy to retrieve the color for a tag when a user selects a word/phrase and clicks on a button to
        # tag the word/phrase. When the user tags the word/phrase, it will be highlighted in the GUI.
        # This dictionary helps us retrieve the color for that particular tag. The loop does the equivalent
        # of self.tag_colors["highlight"] = ["gray", buttonID] in an iteration
        #
        # After populating the dictionary, we will create a button for the different NER tags.
        #
        # NOTE: partial is used to pass a function to a widget e.g., button where the input changes for different
        # buttons. Below, we want to call the function self.get_ner (which takes a single input) several
        # times but each time we pass it a different value depending on the button that was clicked. If the ALAS
        # button is clicked, we want to pass the text "ALAS" but if the "CROP" button was clicked we want to pass the
        # text CROP. So, partial(self.get_ner, "ALAS") is the same as self.get_ner("ALAS")
        #
        for i in range(len(self.tags)):
            tag_value = self.tags[i]
            color_value = self.colors[i]

            # Create button
            btn = tk.Button(self.top_frame, highlightbackground=color_value,text=tag_value,
                            command=partial(self.get_ner, tag_value))
            btn.pack(side=tk.LEFT)
            self.tag_colors_buttonID[tag_value] = [color_value, btn]

        # Blank label with empty spaces used for formatting.
        self.space_label = tk.Label(self.top_frame, text=" ", width=3)
        self.space_label.pack(side=tk.LEFT)

        # Button user will click to tag selected text
        self.pre_tag_selection_btn = tk.Button(self.top_frame, text="Pre-Tag Selection",
                                               command=partial(self.pre_tag, "selection"))
        self.pre_tag_selection_btn.pack(side=tk.LEFT)

        # Button user will click to remove tags
        self.clear_tag_btn = tk.Button(self.top_frame, text="Remove-Tag(s)", command=self.remove_tag)
        self.clear_tag_btn.pack(side=tk.LEFT)

        # Button user will click to tag all the text in the text box
        self.pre_tag_page_btn = tk.Button(self.top_frame, text="Pre-Tag Page(s)", command=partial(self.pre_tag, "page"))
        self.pre_tag_page_btn.pack(side=tk.LEFT)

        # Remove all tags button
        self.clear_btn = tk.Button(self.top_frame, text="Remove All Tags", width=15, command=self.remove_all_tags)
        self.clear_btn.pack(side = tk.LEFT)

        # Frame with buttons that will contain user defined NER tags. Button with NER tags added by users will
        # be added to this frame. This is done in the function add_ent
        self.cust_ent_frame = tk.Frame(self.rootWin)
        self.cust_ent_frame.pack(side=tk.TOP, fill="x")

        # Blank label for formatting
        self.blank_label_two = tk.Label(self.cust_ent_frame, text="   ")
        self.blank_label_two.pack(side=tk.LEFT)

        # Frame containing options for users to add their own NER tags
        self.edit_ent_frame = tk.Frame(self.rootWin)
        self.edit_ent_frame.pack(side=tk.TOP, fill="x")

        # Label for text entry for a new NER tag defined by the user
        self.trait_label = tk.Label(self.edit_ent_frame, text="Enter Entity Label:", width=20)
        self.trait_label.pack(side=tk.LEFT)

        # Text entry widget for user to type the name of a user defined NER tag they want to add
        self.trait_entry = tk.Entry(self.edit_ent_frame, width=10)
        self.trait_entry.pack(side=tk.LEFT)

        # Button to add new NER tag
        self.add_ent_btn = tk.Button(self.edit_ent_frame, text="Add Entity", width=10, command=self.add_ent)
        self.add_ent_btn.pack(side=tk.LEFT)

        # Button to remove NER tag added by the user
        self.remove_ent_btn = tk.Button(self.edit_ent_frame, text="Remove Entity", width=10, command=self.remove_ent)
        self.remove_ent_btn.pack(side=tk.LEFT)

        # Text box. Note, height defines height in widget in lines based on font size. If the font size is bigger,
        # you end up with a bigger textbox because each line will occupy more space.
        self.text = ScrolledText(self.rootWin, height=20, width=140, font="Times "+self.font_size, wrap='word')
        self.text.focus_force()
        self.text.pack(side=tk.TOP)

        # Specify how text will be highlighted in the textbox when a user selects it and click on a button to
        # tag the text. If we only had one button (ALAS), we would have done this using the command
        # self.text.tag_configure("ALAS", background="violet") but we need to do this for all the NER tag buttons
        # hence the for loop
        for tag, color_buttonID in self.tag_colors_buttonID.items():
            color = color_buttonID[0]
            self.text.tag_configure(tag, background=color)

        # Frame just below the text box. It contains buttons in the "Exit" button row
        self.bottom_frame = tk.Frame(self.rootWin)
        self.bottom_frame.pack(side=tk.TOP, fill="x")
        # Blank label for formatting
        self.blank_label_three = tk.Label(self.bottom_frame, text="   ")
        self.blank_label_three.pack(side=tk.LEFT)
        # Exit button
        self.exit_btn = tk.Button(self.bottom_frame, text="Exit",width=10,command=self.quit)
        self.exit_btn.pack(side = tk.LEFT)
        # Load button
        self.load_btn = tk.Button(self.bottom_frame, text="Load Data", width=10, command=self.load_page_from_button)
        self.load_btn.pack(side=tk.LEFT)
        # Clear data button
        self.clear_data_btn = tk.Button(self.bottom_frame, text="Clear Data", width=10, command=self.clear_data)
        self.clear_data_btn.pack(side=tk.LEFT)
        # Clear message button
        self.msg_btn = tk.Button(self.bottom_frame, text="Clear Warning Message", width=20, command=self.clear_message)
        self.msg_btn.pack(side=tk.LEFT)
        # Next page button
        self.next_btn = tk.Button(self.bottom_frame, text="Next Page", command=self.next_page)
        self.next_btn.pack(side = tk.LEFT)
        # Save button
        self.save_btn = tk.Button(self.bottom_frame, text="Save", width=10, command=self.file_save)
        self.save_btn.pack(side=tk.LEFT)

        # Frame that will contain messages being displayed to the user
        self.msg_frame = tk.Frame(self.rootWin)
        self.msg_frame.pack(side=tk.TOP)
        # Label to display messages
        self.msg = tk.Label(self.msg_frame, text="", padx=5, pady=5)
        self.msg.pack(side=tk.LEFT)
        # Continue button
        self.continue_btn = tk.Button(self.msg_frame, text="Continue", width=10,
                                      command=partial(self.continue_func, "save"))
        self.continue_btn.pack(side=tk.LEFT)
        self.continue_btn.pack_forget()
        # Button to overwrite a file when saving
        self.overwrite_btn = tk.Button(self.msg_frame, text="Overwrite", width=10,
                                       command=partial(self.continue_func, "save"))
        self.overwrite_btn.pack(side=tk.LEFT)
        self.overwrite_btn.pack_forget()
        # Button to create a copy as opposed to overwriting a file
        self.copy_btn = tk.Button(self.msg_frame, text="Create Copy", width=10,
                                  command=partial(self.continue_func, "copy"))
        self.copy_btn.pack(side=tk.LEFT)
        self.copy_btn.pack_forget()

        # Metadata Frame. When a user is about to save a file, two text entry options will appear giving users
        # an option to enter meta-data for the annotation such as source of the PDF/text
        self.metadata_frame = tk.Frame(self.rootWin)
        self.metadata_frame.pack(side=tk.TOP)
        # Shows the name that will be used for the annotation file
        self.ann_file_label = tk.Label(self.metadata_frame, text="Annotation File Name (json):", width=20, anchor="w")
        self.ann_file_label.pack(side=tk.LEFT)
        self.ann_file_label.pack_forget()
        self.ann_file_entry = tk.Entry(self.metadata_frame, width=30)
        self.ann_file_entry.pack(side=tk.LEFT)
        self.ann_file_entry.pack_forget()
        # Users can specify the source of the annotation. This source will be embedded in the annotation json file
        self.source_label = tk.Label(self.metadata_frame, text="PDF/Text URL (source):", width=15, anchor="w")
        self.source_label.pack(side=tk.LEFT)
        self.source_label.pack_forget()
        self.source_entry = tk.Entry(self.metadata_frame, width=30)
        self.source_entry.pack(side=tk.LEFT)
        self.source_entry.pack_forget()

        # Frame for selecting files and folders
        self.open_frame = tk.Frame(self.rootWin)
        self.open_frame.pack(side=tk.TOP,fill="x")
        # Blank label for formatting
        self.blank_label_five = tk.Label(self.open_frame, text="   ")
        self.blank_label_five.pack(side=tk.LEFT)
        # Select file to be annotated button
        self.open_button = tk.Button(self.open_frame,text='Select Raw Data File(PDF/txt)', width=18,
                                     command=partial(self.open_file, "pdf_or_text"))
        self.open_button.pack(side=tk.LEFT)
        # Select folder with language model
        self.ner_model_button = tk.Button(self.open_frame, text='Select NER model folder', width=18,
                                          command=self.get_ner_model_dir)
        self.ner_model_button.pack(side=tk.LEFT)
        # Enter page you would like to load. Start with 1 as opposed to the conventional 0 numbering in CS
        self.page_label = tk.Label(self.open_frame, text="Raw Data File Page Num:", width=18)
        self.page_label.pack(side=tk.LEFT)
        self.page_entry = tk.Entry(self.open_frame, width=5)
        self.page_entry.pack(side=tk.LEFT)
        # Select annotation file
        self.annotation_btn = tk.Button(self.open_frame, text="Select Annotation File(JSON)",width=20,
                                        command=partial(self.open_file, "json"))
        self.annotation_btn.pack(side=tk.LEFT)
        # Button to increase font in the text box (Font +)
        self.font_plus = tk.Button(self.open_frame, text="Font +", width=10, command=self.font_plus)
        self.font_plus.pack(side=tk.LEFT)
        # Button to decrease font in the text box (Font +)
        self.font_minus = tk.Button(self.open_frame, text="Font -", width=10, command=self.font_minus)
        self.font_minus.pack(side=tk.LEFT)

    def font_plus(self):
        """
        Increase font size for text in ScrolledText (text box).

        Expects the global variable self.font_size which is of type string to be set. The default value is "16".
        This function increments self.font_size by 1 and then updates font size in self.text.
        """
        self.font_size = str(int(self.font_size) + 1)
        self.text['font'] = "Times "+self.font_size

    def font_minus(self):
        """
        Decrease font size for text in ScrolledText (text box).

        Expects the global variable self.font_size which is of type string to be set. The default value is "16".
        This function decreases self.font_size by 1 and then updates font size in self.text.
        """
        self.font_size = str(int(self.font_size) - 1)
        self.text['font'] = "Times "+self.font_size

    def add_ent(self):
        """
        Add a user defined named entity to the application.

        Expects the text entry for specifying a user defined entity tag to have the name of a user defined named
        entity. It then adds this new named entity to the application.
        """
        ent_label = self.trait_entry.get().upper()
        if ent_label in self.tags:
            self.msg.config(text="Warning!! Cannot add entity. Another entity with the same label already exists!",
                            foreground="red")
        else:
            # The code below select a color from color_list which is defined in tkinterColorList.py
            # If it loops through the length of the colors in color_list and does not find a color
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
            # find a color that has not already been used. This can happen if by chance we keep
            # selecting colors that have been used. If this happens, just create a random color.
            if color is None:
                color = "#" + ("%06x" % random.randint(0, 16777215))
            self.colors.append(color)
            self.tags.append(ent_label)
            btn = tk.Button(self.cust_ent_frame, highlightbackground=color, text=ent_label,
                            command=partial(self.get_ner, ent_label))
            btn.pack(side=tk.LEFT)
            self.text.tag_configure(ent_label, background=color)
            self.tag_colors_buttonID[ent_label] = [color, btn]

    def remove_ent(self):
        """
        Remove a user defined named entity from the application.

        Expects the text entry for specifying a user defined entity tag to have the name of a user defined named
        entity. It then removes this named entity from the application.
        """
        ent_label = self.trait_entry.get().upper()
        color = self.tag_colors_buttonID[ent_label][0]
        ent_btn = self.tag_colors_buttonID[ent_label][1]
        ent_btn.pack_forget()
        # Remove elements from dictionary and arrays
        self.tag_colors_buttonID.pop(ent_label)
        self.colors.remove(color)
        self.tags.remove(ent_label)

    def get_ner_model_dir(self):
        """
        Select a folder containing spaCy nlp pipeline.

        Loads the nlp pipeline that will be used for tagging.

        Raises
        ------
        OSError
            If the selected folder does not contain a valid spaCy pipeline, an OSError will be thrown and
        a default language model is used instead.
        """
        self.model_dir = fd.askdirectory()
        try:
            self.nlp_agdata = spacy.load(self.model_dir)
            lang = self.nlp_agdata.lang # Attribute error thrown if valid language model is not selected
            self.msg.config(text="NOTE: Model for "+lang+" language identified", foreground="orange")
        except OSError:
            self.msg.config(text="WARNING!!: Selected folder does not contain valid language model \n"
                                 "Default model 'en_core_web_lg' will be used.", foreground="red")
            self.nlp_agdata = spacy.load("en_core_web_lg")
        # NOTE: Commenting the line below for now. We will try using spaCy noun phrases instead
        # to capture tags such as 'rough owns'
        # self.nlp_agdata.add_pipe("compound_trait_entities", after='ner')

    def open_file(self, file_type: str):
        """
        Open a file (pdf/text) to be annotated or an annotation file (json) to be reviewed. selected using the GUI.

        Parameters
        ----------
        file_type : str
            Type of file that was selected. This is either 'json' or 'pdf_or_text'

        If a user selects a pdf ot text file, it will be loaded into the text box for annotation. If a json file
        containing annotation is selected, it will bo loaded with the annotations highlighted.
        """
        # TODO: Make it possible for users to select text files

        # Clear warning message, if one exists
        self.msg.config(text="")

        # file type
        filetypes = (
            ('json files', '*.json'),
            ('PDF files', '*.pdf')
        )
        # show the open file dialog
        f = fd.askopenfile(filetypes=filetypes)

        if file_type == "json":
            self.annotation_file = f
            self.review_annotations()
        elif file_type == "pdf_or_text":
            self.raw_file=f
            self.load_page()
        else:
            self.msg.config(text="Warning!! Please select a valid (pdf or json) file.", foreground="red")

    def load_pdf(self):
        """
        Load  PDF file.

        Expects the self.raw_file global variable to be set. If not, a warning message is displayed.
        """

        if self.raw_file is None:
            self.msg.config(text="No raw data file has been selected. Please select a file to load.", foreground="red")

        self.file_prefix = self.raw_file.name.split(".")[0]
        self.pdf_name = self.raw_file.name.split("/")[-1]
        self.pdf_document = Document(self.raw_file.name)

    def page_num_is_valid(self, page_num):
        """
        Returns True if page_num is a number, False if page_num is completely invalid, and -1 if it's a range.
        Note that the function expects spacing to have already been cleaned out of it prior to being called.
        In other words, it won't necessarily recognize something like "1 - 5" as a range.
        """
        if page_num.isdigit():
            return True
        dash_index = page_num.find("-")
        if(dash_index == -1):
            return False
        pg1 = page_num[0 : dash_index]
        if not pg1.isdigit():
            return False
        pg2 = page_num[dash_index + 1:]
        if not pg2.isdigit():
            return False
        return -1

    def handle_bad_page_requests(self, page_num_valid):
        """
        If a page not in the doc is requested, this will set the page number to a valid
        one and print a warning.

        page_num_valid is passed in so that this method already knows whether it should
        be checking a list or single number.
        """
        doc_length = len(self.pdf_document)
        err = False
        double_err_text = " At least one other error was not displayed- see entry box."
        if page_num_valid == -1: # ie, page number is a range
            if self.page_number[0] < 1: # This will only take effect if the starting page is set to 0. Beginning hyphens are already invalid.
                self.page_number[0] = 1
                self.msg.config(text="First page entered is less than 1; setting first page to 1", foreground="red")
                self.page_entry.delete(0, tk.END)
                self.page_entry.insert(0, "1-" + str(self.page_number[1]))
                err = True
            if self.page_number[1] < 1:
                self.page_number[1] = 1
                self.page_entry.delete(0, tk.END)
                if(err): # This will only happen if the user enters some form of "0-0"- trying to do a negative anywhere doesn't count as a range, just invalid
                    self.msg.config(text="PDFs start with page 1, not 0. Additionally, you can enter just one page instead of a range if you'd like. Going to page 1.", foreground="red")
                    self.page_entry.insert(0, "1")
                else:
                    self.msg.config(text="Second page entered is less than 1; setting second page to 1", foreground="red")
                    self.page_entry.insert(0, str(self.page_number[0]) + "-1")
                    err = True
            if self.page_number[1] > doc_length:
                self.page_number[1] = doc_length
                if(err):
                    err_text = "Last page entered is greater than the length of the PDF; setting last page to the end of the PDF." + double_err_text
                else:
                    err_text = "Last page entered is greater than the length of the PDF; setting last page to the end of the PDF."
                    err = True
                self.msg.config(text=err_text, foreground="red")
                self.page_entry.delete(0, tk.END)
                self.page_entry.insert(0, str(self.page_number[0]) + "-" + str(self.page_number[1]))
            if self.page_number[0] > doc_length:
                self.page_number[0] = doc_length
                err_text = "First page entered is greater than the length of the PDF; setting first page to the end of the PDF."
                if(err):
                    err_text = err_text + double_err_text
                self.msg.config(text=err_text, foreground="red")
                self.page_entry.delete(0, tk.END)
                self.page_entry.insert(0, str(self.page_number[0]) + "-" + str(self.page_number[1]))
        else: # ie. there is a single page
            if self.page_number < 1: # This may as well be self.page_number == 0. A beginning hyphen is already invalid (not a digit or a range).
                self.page_number = 1
                self.msg.config(text="Page entered is too small; setting to 1", foreground="red")
                self.page_entry.delete(0, tk.END)
                self.page_entry.insert(0, "1")
            if self.page_number > doc_length:
                self.page_number = doc_length
                self.msg.config(text="Page entered is too large; setting it to the last page (" + str(doc_length) + ")", foreground="red")
                self.page_entry.delete(0, tk.END)
                self.page_entry.insert(0, str(doc_length))

    def handle_page_range(self, page_range: list):
        """
        Sets everything related to the page number with the assumption that
        the user has entered a range of numbers rather than a single page. I.e.,
        the range is ordered correctly, self.page_number is set to a list of
        two integer values, and self.chunk is set to the starting page.

        Spacing should be removed from page_range before it's passed into this method.
        """
        dash_index = page_range.find("-")
        pg1 = int(page_range[0 : dash_index])
        pg2 = int(page_range[dash_index + 1:])
        self.page_number = [pg1, pg2]
        # Switch first and last page if the user's first number was the smaller one.
        if(self.page_number[1] < self.page_number[0]):
            self.msg.config(text="A larger page number was entered first. The pages will be displayed in order from smallest to largest anyway.", foreground="red")
            placeholder = self.page_number[0]
            self.page_number[0] = self.page_number[1]
            self.page_number[1] = placeholder
            self.page_entry.delete(0, tk.END)
            self.page_entry.insert(0, str(self.page_number[0]) + "-" + str(self.page_number[1]))
        self.chunk=self.page_number[0]

    def is_spaced_range(self, raw_page_entry: str):
        """
        Checks to see if a page entry is simply two numbers separated by a space, which
        the program should handle as a range of pages.
        
        Lots of processing of page_entry is done both before and after this method is
        called. It will never be called on an entry with zany spacing, and it can be
        wrong when it comes to invalid inputs since they'll get filtered out anyway.
        """
        first_space = raw_page_entry.find(" ")
        # If there is one space...
        if(not(first_space == -1)) and (first_space == raw_page_entry.rfind(" ")):
            # And if this space is surrounded by only two valid, positive digits...
            if(raw_page_entry[0 : first_space].isdigit() and raw_page_entry[first_space+1 :]):
                return True
        return False

    def clean_spaces_in_page_entry(self, raw_page_entry: str):
        """
        Removes extra spaces. Then it checks to see if a user entered a range separated with
        spaces and replaces the spaces with a dash if so.
        """
        old_entry = raw_page_entry.strip() # Remove loading and trailing spaces so that something like " 2 5" gets loaded as "2-5" instead of "25"
        # Remove all spaces that are adjacent to a dash or a space
        # The below line is straight from GeeksForGeeks, they're wonderful
        all_spaces = [i for i in range(len(old_entry)) if old_entry.startswith(" ", i)]
        entry = ""
        for i in range(0, len(old_entry)):
            if not(i in all_spaces):
                entry = entry + old_entry[i] 
            elif not(old_entry[i-1] == "-" or old_entry[i+1] == "-" or old_entry[i+1] == " "):
                    entry = entry + old_entry[i]
        # Past this point, only single spaces that are next to a dash should exist. This could be something like -  -,
        # but page_num_is_valid should catch that later.
        if(self.is_spaced_range(entry)):
            self.msg.config(text="You have entered two numbers with spacing in between. Loading those pages and the pages between them.", foreground="orange")
            entry = entry.replace(" ", "-")
            # Replace user entry with how the program has read it.
            self.page_entry.delete(0, tk.END)
            self.page_entry.insert(0, entry)
        return entry

    def load_page_from_button(self):
        """
        Loading the page can cause warnings to pop on on the bottom, especially with ranges.
        If you press "load data" and the warning from your last page load is still there, it
        can look like you just got an error even though you didn't. Thus, pressing the button
        to load the page first clears any warnings.
        """
        self.msg.config(text="")
        self.load_page()

    def load_page(self):
        """
        Load contents of a PDF or text file into text box.

        If the entry box for page number has a value, it will load the page specified. If not, by default it will
        load the first page.
        """
        # TODO: Give users the option to load text files in addition to pdf files.
        if self.raw_file is None:
            self.msg.config(text="No raw data file has been selected. Please select a file to load.", foreground="red")
        else:

            # Reset annotation dictionary
            self.cust_ents_dict = {}

            page_num = self.clean_spaces_in_page_entry(self.page_entry.get())
            page_num_valid = self.page_num_is_valid(page_num)
            if page_num_valid == False:
                self.msg.config(text="Valid page number not entered. Value initialized to 1", foreground="red")
                self.page_number = 1
                self.page_entry.delete(0,tk.END)
                self.page_entry.insert(0, str(self.page_number))
                self.chunk=self.page_number
            elif page_num_valid == True:
                self.page_number = int(page_num)
                self.chunk=self.page_number
            else: # Range of numbers
                self.handle_page_range(page_num)

            # Delete contents
            self.text.delete(1.0, tk.END)

            # Load PDF file
            self.load_pdf()

            self.handle_bad_page_requests(page_num_valid)

            if not (page_num_valid == -1): # Single page, whether page_num_valid is true or false
                page = self.pdf_document[self.page_number - 1]
                #  doesn't necessarily have to be removed for a single page; It gets removed in
                # the else because tagging across multiple pages doesn't work correctly if  exists.
                # However, it's removed here as well for consistency and neatness.
                txt = page.text().replace("\r", "").replace("", "")
            else: # Page range
                txt = ""
                for page in self.pdf_document[self.page_number[0] - 1 : self.page_number[1]]:
                    txt = txt + page.text().replace("\r", "").replace("", "")
            self.text.insert("1.0",txt)
            return txt

    def update_scrolled_text_line_content_index(self):
        """
        Populate the dictionary self.scrolled_text_line_content_index with position indices for the first and
        last characters in each line in the text box.

        Trying to figure out where entities are on scrollTextbox is a little tricky because tKinter uses newline
        characters to split text. Here we are keeping track of how many characters appear before a line in the
        GUI. This should make it easier to figure out where a token is given its
        start and end indices. Given (Steveland/Luther//Wintermalt 1001 1029 PED)  named entity, we know the first
        character is at position 1001 and the last character is at position 1029. Question is, where is it in the
        textbox? This dictionary will have line number as the key and a tuple
        (index of first char in line, index of last char in line) as values e.g.,  {1: (0, 113), 2: (114, 228). This
        dictionary tells you the first line has the first 113 characters and the second line has characters starting
        with index 114 up to index 228.
        """
        input_text = self.text.get(1.0, "end")
        lines = input_text.splitlines()
        line_no = 1
        num_char = 0
        for line in lines:
            line_len = len(line)
            interval = (num_char, num_char + line_len)
            self.scrolled_text_line_content_index[line_no] = interval
            num_char = num_char + line_len + 1  # The 1 we are adding is for newline character
            line_no = line_no + 1

    def highlight_ent(self, start_char: int, end_char: int, label: str):
        """
        Given the start index and end index of a named entity, highlight it in the text box.

        Expects the dictionary (self.scrolled_text_line_content_index) with indices for characters in each line in
        the text box to be specified. The label for the named entity needs to have been added to
        self.text.tag_configure.
        """
        line_start = -1
        char_start = -1
        line_end = -1
        char_end = -1
        # Loop through lines in the text field and find where this tag is.
        for key, value in self.scrolled_text_line_content_index.items():
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

    def pre_tag(self, selection: str):
        """
        Pre-tag selected content or all the text in text box with NER tags.

        Parameters
        ----------
        selection : str
            String specifying the type tagging to be done.

        If a user has selected a block of text and clicked the "Pre-Tag Selection" button, the selected text will be
        tagged and annotation displayed in the text box.

        If they clicked the "Pre-Tage Pages(s)" button, all the text loaded in the text box will be annotated.
        """
        input_text = None
        # Clear warning message, if one exists
        self.msg.config(text="")
        if self.model_dir is None:
            self.msg.config(text="Warning!! Unable to pre-tag. No NER model selected.", foreground="red")
        else:
            input_text = None
            # Get page number
            page_num = self.clean_spaces_in_page_entry(self.page_entry.get())
            if not page_num.isdigit(): # Either invalid or a range.
                if self.page_num_is_valid(page_num) == False: # Invalid
                    self.msg.config(text="Page number not entered. Page 1 in PDF loaded", foreground="red")
                    page_num = 1
                else: # Range
                    self.handle_page_range(page_num)
            else: # Single valid page
                self.page_number = int(page_num)
                self.chunk = self.page_number

            if selection == "selection":
                # TODO: If a user clicks the "Pre-Tag Selection" button but they have not selected any text, an
                # error is through without displaying a warning message. Check to make sure "sel.first" and
                # "sel.last" are defined before calling self.text.get()
                input_text =  self.text.get("sel.first", "sel.last")
                self.text.delete(1.0, tk.END)
                self.text.insert("1.0", input_text)
            else:
                if self.pdf_document is None:
                    self.msg.config(text="Warning!! No PDF was detected. Will attempt to load PDF ", foreground="red")
                    self.load_pdf()

                input_text = self.load_page()


            # Reset annotation dictionary
            self.cust_ents_dict = {}

            # Update variable that holds number of lines in textbox. You need this for
            # the function highlight_ent to work
            self.update_scrolled_text_line_content_index()
            doc = self.tag_ner_with_spacy(input_text)

            if(len(doc.ents) == 0):
                self.msg.config(text="Warning!! No entities were found in this selection.", foreground="red")
            if type(self.page_number) is list:
                page_start = self.page_number[0]
            else:
                page_start = self.page_number
            for ent in doc.ents:
                # NER is in our list of custom tags
                if ent.label_ in self.tags:
                    # index = self.tags.index(ent.label_) # Find index for an element in a list
                    self.highlight_ent(ent.start_char, ent.end_char, ent.label_)
                    if self.cust_ents_dict.get(page_start, False):
                        self.cust_ents_dict[page_start].append((ent.start_char, ent.end_char, ent.label_))
                    else:
                        self.cust_ents_dict[page_start] = [(ent.start_char, ent.end_char, ent.label_)]

            if self.cust_ents_dict.get(page_start, False):
                tags = self.cust_ents_dict[page_start]
                self.cust_ents_dict[page_start] = [input_text, tags]

    def overlap(self, interval_one: list, interval_two: list) -> bool:
        """
        Check to see if two intervals overlap.

        Parameters
        ----------
        interval_one : list[start1, end1]
            List containing two int values [start1, end1].

        interval_two : list[start2, end2]
            List containing two int values [start2, end2].

        Returns
        -------
        bool
            True if the intervals overlap and False otherwise.
        """
        overlap = False
        interval_one_start = interval_one[0]
        interval_one_end = interval_one[1]

        interval_two_start = interval_two[0]
        interval_two_end = interval_two[1]

        if (interval_two_start >= interval_one_start) and (interval_two_start < interval_one_end):
            overlap = True
        elif (interval_two_end > interval_one_start) and (interval_two_end <= interval_one_end):
            overlap = True
        elif (interval_two_start <= interval_one_start) and (interval_two_end >= interval_one_end):
            overlap = True
        return overlap

    def get_selected_interval(self) -> tuple:
        """
        Determines the index of the first and last characters (char_start, char_end) selected by the user.

        Returns
        -------
        tuple
            Indices of first and last characters selected (char_start, char_end) .
        """

        selection_start_line = int(self.text.index("sel.first").split(".")[0])
        tmp_selection_start = int(self.text.index("sel.first").split(".")[1])
        selection_start = self.scrolled_text_line_content_index[selection_start_line][0] + tmp_selection_start

        selection_end_line = int(self.text.index("sel.last").split(".")[0])
        tmp_selection_end = int(self.text.index("sel.last").split(".")[1])
        selection_end = self.scrolled_text_line_content_index[selection_end_line][0] + tmp_selection_end
        result = (selection_start, selection_end)
        return result

    def get_ner(self, tag_label: str):
        """
        Tag a piece of text that has been selected as a named entity.

        Parameters
        ----------
        tag_label : str
            Label to assign to the named entity that was selected.
        """
        # TODO: This function has a major bug. If you try to tag text that spans multiple pages, it will not only
        # fail, but it will also remove some annotations.

        # Clear warning message, if one exists
        self.msg.config(text="")
        try:
            # Get text
            input_text = input_text = self.text.get(1.0, "end")

            # Update variable that holds number of lines in textbox.
            self.update_scrolled_text_line_content_index()

            # Get indices for the first and last characters selected
            (ent_char_start, ent_char_end) = self.get_selected_interval()

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
                self.cust_ents_dict[self.chunk][1].append((ent_char_start,ent_char_end, tag_label))
            else:
                self.cust_ents_dict[self.chunk] = [input_text, [(ent_char_start,ent_char_end, tag_label)]]

            # Highlight the new NER  tag
            self.text.tag_add(tag_label, "sel.first", "sel.last")

        except tk.TclError:
            self.msg.config(text="Warning!! get_ner error.", foreground="red")

    def remove_tag(self):
        """
        Untag a piece of text that was classified as a named entity.

        Extract the piece of text that was selected and remove it from the list of named entities.
        """

        # Clear warning message, if one exists
        self.msg.config(text="")

        # Get indices for the first and last characters selected
        (selection_start, selection_end) = self.get_selected_interval()

        new_ents = []
        overlapping_tags = []
        input_text = self.cust_ents_dict[self.chunk][0]
        entities = self.cust_ents_dict[self.chunk][1]

        # Loop through tags and find ones that overlap with selected region and remove them.
        for (start, end, label) in entities:
            if not self.overlap([selection_start, selection_end], [start, end]):
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

    def get_custom_labels(self, data: dict):
        """
        Given a dictionary representing the entirety of a json file generated by this program,
        this method finds every custom, user-defined label and loads them back into the program.
        """
        labels = []
        for sentence_item in data['sentences']:
            for entity_item in data['sentences'][sentence_item]:
                label = data['sentences'][sentence_item][entity_item]['label']
                if (not (label in labels)) and (not (label in self.tags)):
                    # If a new tag is found, essentially auto-fill the custom trait field and press the button to add a custom entity.
                    labels.append(label)
                    self.trait_entry.delete(0, tk.END)
                    self.trait_entry.insert(0, label)
                    self.add_ent()
                    self.trait_entry.delete(0, tk.END)

    def review_annotations(self):
        """
        Load a json file containing annotations and review it.

        It does not take as input any parameters, but it expects the variable that hold annotation
        file name (self.annotation_file)  to have a valid json file value.
        """

        # Clear warning message, if one exists
        self.msg.config(text="")

        if self.annotation_file is None:
            self.msg.config(text="Please select an annotations file (json)", foreground="red")
        else:
            # Load annotation data
            data = json_2_dict(self.annotation_file.name)
            train_data = dict_2_mixed_type(data)
            self.get_custom_labels(data)
            """
            doc = data['doc']
            url = data['url']
            """
            self.chunk = int(data['chunk'])
            self.page_number = self.chunk

            # Empty text box so we can load annotations
            self.text.delete(1.0, tk.END)

            annotated_text = None
            entities = None

            # Annotation file that contains more than one text block
            if len(train_data) > 1:
                total_num_char = 0
                annotated_text = ""
                entities = []
                for text_annotation in train_data:
                    annotated_text_tmp = text_annotation[0]
                    entities_tmp = text_annotation[1]['entities']
                    for ent_tmp in entities_tmp:
                        entities.append((total_num_char + ent_tmp[0],total_num_char + ent_tmp[1], ent_tmp[2]))
                    total_num_char = total_num_char + len(annotated_text_tmp) + 1
                    annotated_text = annotated_text + annotated_text_tmp + "\n"
                self.cust_ents_dict[self.chunk] = [annotated_text, entities]
            else:
                text_annotation = train_data[0]
                annotated_text = text_annotation[0]
                entities = text_annotation[1]['entities']
                self.cust_ents_dict[self.chunk] = [annotated_text,entities]

            self.text.insert("1.0", annotated_text + '\n')

            # Update variable that holds number of lines in textbox. You need this update
            # for highlight_ent to work
            self.update_scrolled_text_line_content_index()

            for ent_val in entities:
                self.highlight_ent(ent_val[0],ent_val[1], ent_val[2])

    def clear_message(self):
        """
        Clear warning message
        """
        self.msg.config(text="")

    def clear_data(self):
        """
        Clear data in text box and dictionary containing annotations.
        """
        # Clear annotations
        self.cust_ents_dict = {}

        # Clear warning message
        self.msg.config(text="")

        # Clear content
        self.text.delete(1.0, tk.END)

    def remove_all_tags(self):
        """
        Remove all the NER tags on text loaded in the text box.
        """
        for tag in self.tags:
            self.text.tag_remove(tag, "1.0", "end")

        # Clear annotations
        self.cust_ents_dict = {}

        # Clear warning message
        self.msg.config(text="")

    def tag_ner_with_spacy(self, text: str) -> spacy.tokens.Doc:
        """
        Use NLP pipeline to identify named entities in the text.
        """
        doc = self.nlp_agdata(text)
        return doc

    def continue_func(self, save_choice: str):
        """
        Continue the process of either saving annotation in a new file or overwriting an existing file.
        """
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
        """
        Save current annotation.
        """
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

    def next_page(self):
        """
        Load the next page.
        """
        if len(self.cust_ents_dict) == 0:
            self.msg.config(text="Warning!! No annotations to save.", foreground="red")
        else:
            self.msg.config(text="")
            # Save current annotation
            # Uncomment this for now. Initially it seemed like a good idea but there are a lot of
            # Instances where a user might not want to save annotations when they click next page
            # self.file_save()

        # Increment page number
        try:
            self.page_number = self.page_number + 1
            self.page_entry.delete(0, tk.END)
            self.page_entry.insert(0, str(self.page_number))

            # Reset annotation data
            self.annotation_file = None

            # Load data
            self.load_page()
        except TypeError:
            # While this would be easy to add, it's not clear what exactly SHOULD be incremented
            # if the user clicks "next page" on a range, so that's left to the user.
            self.msg.config(text="WARNING!! Cannot increment a range of pages.", foreground="red")

    def go(self):
        """
        Start running the GUI running.
        """
        self.rootWin.mainloop()

    def quit(self):
        """
        Callback method attached to the quit button.

        It destroys the main window, which ends the program
        """
        # TODO: If a user accidentally clicks the Exit button, the program quits without saving any of the current
        # annotation. Add functionality to first ask the user if they want to save or discard their current annotation,
        # if they have any. NOTE: Annotations are saved on self.cust_ents_dict. Checking to see if this dictionary
        # is empty should be a reasonable check on if a user has annotations that need to be saved.
        self.rootWin.destroy()


# Driver code
if __name__ == "__main__":
    ner_gui = CropNerGUI()
    ner_gui.go()
