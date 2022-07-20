#!/bin/env python3
import platform
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

# 1) WE NEED TO RESOLVE STANDARDIZING THINGS SUCH AS
# "ROUGH AWNS" and "AWNS ARE ROUGH", WHITE ALEURONE AND ALEURONE IS WHITE. NOTE: Maybe compound traits
# do not make sense because we need to be able to know
# relationships. We should look at co-reference resolution.
# See: https://medium.com/huggingface/state-of-the-art-neural-coreference-resolution-for-chatbots-3302365dcf30
#
# 2) WE NEED TO GROUP ANNOTATIONS SUCH AS TRAITS INTO CATEGORIES THAT
# MAKE SENSE TO THE USER. RIGHT NOW WE HAVE "early maturity" AND "winter"
# AS TRAITS WHILE ACCORDING TO THE SPECS WE SHOULD BE RETURNING
# “Maturity” : “early maturity”, “Season”: “winter”
#
# 3) "It is medium maturing and medium tall (averages about 41 inches in plant height) with fair straw strength."
#    In the sentence above, medium tall will be tagged as trait. There is additional useful information in brackets
# that tells you exactly what medium tall means (above 41 inches). Is it possible to extract this additional
# information about the definition of medium tall.
#
# 4) If we are able to get NER to be reasonably accurate, the next step is being able to link properties to a
# particular crop variety. Identifying crop traits is good but what would even be better is to know what crop
# variety these traits are associated with. EXAMPLE:
#
# Alexis is a two-row spring malting and feed barley. It was released by Western Plant Breeders. It was selected from
# the cross BI1622a/Triumph. It is midseason in maturity and is mid-tall with fair straw strength. At the time of
# evaluation it was resistant to stripe rust. It was evaluated as Entry 966 in the UC Regional Cereal Testing program
# in 1997 for spring planting in the intermountain region of northern California.
#
# What would be very useful is knowing what "it" is referring to in the paragraph above.
#
# 5) Need to start thinking about an ontology


# Create NER GUI class
class CropNerGUI:
    """ A class used to represent NER tagging GUI window.

    ...
    Attributes
    ----------
    self.model_default : str
        default model from argparse if given
    self.file_default : str
            default file from argparse if given
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
    self.file_name : str
        Name of the pdf/text file being annotated. e.g., BarCvDescLJ11.pdf
    self.file_prefix : str
        File path prefix (minus file type) e.g., for BarCvDescLJ11.pdf path prefix is Data/DavisLJ11/BarCvDescLJ11
    self.file_mode : str
        Specifies whether the program is working on a pdf or text file
    self.scrolled_text_line_content_index : dict
        Contains index position of characters in a given line. Key = line number tuple is index of first and last
        characters respectively. {2: (114, 228)} = line 2 has characters from index 114 to index 228
    self.nlp_agdata : class (spacy.lang)
        spaCy language model. Defaults to en_core_web_lg if not specified
    self.cust_ents_dict : dict
        Contains NER tag annotations. key = chunk number, values = entities
    self.page_number : int
        Current page number
    self.metadata_toggle : bool
        Boolean determining whether the metadata panel should be visible or not
    self.json_initialized : bool
        Whether a json file has been initialized in the workspace or not

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
    file_save(self)
        Save current annotation.
    next_page(self)
        Load the next page.
    go(self)
        Start running the GUI running.
    quit(self)
        Callback method attached to the quit button.
    """

    def __init__(self, model_default=None, file_default=None):
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
        self.file_name = None
        self.file_prefix = None
        self.file_mode = None
        self.scrolled_text_line_content_index = {}
        self.nlp_agdata = None
        self.cust_ents_dict = {}
        self.page_number = 0
        self.metadata_toggle = False
        self.json_initialized = False

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
            # Button colors already behaved differently between all 3 major platforms (highlightbackground
            # behaves... weirdly on MacOS, just has an outline for Linux, and doesn't work on Windows). Now
            # it still behaves differently on all of them, but fully highlights the button on Windows.
            if(platform.system() == "Windows"):
                btn.config(bg=color_value)
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

        # Label displaying the current working json file
        self.working_file_label = tk.Label(self.rootWin, text="Working Annotation File: "+str(self.annotation_file))
        self.working_file_label.pack(side=tk.TOP)

        # Blank label for formatting
        self.blank_label_two = tk.Label(self.cust_ent_frame, text="   ")
        self.blank_label_two.pack(side=tk.LEFT)

        # Frame containing options for users to add their own NER tags
        self.edit_ent_frame = tk.Frame(self.rootWin)
        self.edit_ent_frame.pack(side=tk.TOP, fill="x", padx="40")

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

        # Middle frame for text box and additional file elements like metadata entries
        self.middle_frame = tk.Frame(self.rootWin)
        self.middle_frame.pack(side=tk.TOP, fill="x")

        # Text box. Note, height defines height in widget in lines based on font size. If the font size is bigger,
        # you end up with a bigger textbox because each line will occupy more space.
        self.text = ScrolledText(self.middle_frame, height=20, width=140, font="Times "+self.font_size, wrap='word')
        self.text.focus_force()
        self.text.pack(side=tk.TOP)

        # Metadata button for setting metadata for current raw file
        self.metadata_btn = tk.Button(self.edit_ent_frame, text="Metadata", width=10, command = self.toggle_metadata)
        self.metadata_btn.pack(side=tk.RIGHT)

        # Doc label
        self.doc_label = tk.Label(self.middle_frame, text="Document Name")
        # Doc entry
        self.doc_entry = tk.Entry(self.middle_frame, width=30)
        # URL label
        self.url_label = tk.Label(self.middle_frame, text="URL")
        # URL entry
        self.url_entry = tk.Entry(self.middle_frame, width=30)
        # Date label
        self.date_label = tk.Label(self.middle_frame, text="Date file created")
        # Date entry
        self.date_entry = tk.Entry(self.middle_frame, justify=tk.CENTER, width=30)
        self.date_entry.insert(0, "File not initialized")
        self.date_entry.config(state=tk.DISABLED)

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
        self.next_btn.pack(side=tk.LEFT)
        # Save button
        self.save_btn = tk.Button(self.bottom_frame, text="Save", width=10, command=self.file_save)
        self.save_btn.pack(side=tk.LEFT)

        # Frame that will contain messages being displayed to the user
        self.msg_frame = tk.Frame(self.rootWin)
        self.msg_frame.pack(side=tk.TOP)
        # Label to display messages
        self.msg = tk.Label(self.msg_frame, text="", padx=5, pady=5)
        self.msg.pack(side=tk.LEFT)

        # Frame for selecting files and folders
        self.open_frame = tk.Frame(self.rootWin)
        self.open_frame.pack(side=tk.TOP,fill="x")
        # Blank label for formatting
        self.blank_label_five = tk.Label(self.open_frame, text="   ")
        self.blank_label_five.pack(side=tk.LEFT)
        # Select file to be annotated button
        self.open_button = tk.Button(self.open_frame,text='Select Raw Data File(PDF/txt)', width=18,
                                     command=partial(self.open_file, "pdf/txt"))
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
        self.page_entry.bind("<Return>", self.load_page_from_button)
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
        Increase font size for text in ScrolledText (text box), changing window size with it.

        Expects the global variable self.font_size which is of type string to be set. The default value is "16".
        This function increments self.font_size by 1 and then updates font size in self.text.
        """
        prev_text_size = self.text.winfo_reqheight()
        self.font_size = str(int(self.font_size) + 1)
        self.text['font'] = "Times "+self.font_size
        new_size = (self.text.winfo_reqheight() - prev_text_size) + self.rootWin.winfo_reqheight()
        self.rootWin.geometry(str(self.rootWin.winfo_reqwidth()) + "x" + str(new_size))

    def font_minus(self):
        """
        Decrease font size for text in ScrolledText (text box), changing window size with it.

        Expects the global variable self.font_size which is of type string to be set. The default value is "16".
        This function decreases self.font_size by 1 and then updates font size in self.text.
        """
        prev_text_size = self.text.winfo_reqheight()
        if not (int(self.font_size) <= 1):
            self.font_size = str(int(self.font_size) - 1)
        else:
            self.msg.config(text="Font size can't get any smaller!", foreground="red")
        self.text['font'] = "Times "+self.font_size
        new_size = (self.text.winfo_reqheight() - prev_text_size) + self.rootWin.winfo_reqheight()
        self.rootWin.geometry(str(self.rootWin.winfo_reqwidth()) + "x" + str(new_size))

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
            if(platform.system() == "Windows"):
                btn.config(bg=color)
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
        try:
            color = self.tag_colors_buttonID[ent_label][0]
            ent_btn = self.tag_colors_buttonID[ent_label][1]
            ent_btn.pack_forget()
            # Remove elements from dictionary and arrays
            self.tag_colors_buttonID.pop(ent_label)
            self.colors.remove(color)
            self.tags.remove(ent_label)

            # Remove highlighting
            self.text.tag_remove(ent_label, "1.0", "end")

            # Remove from annotation dictionary. This can probably be simplified.
            new_ents = []
            input_text = self.cust_ents_dict[self.chunk][0]
            entities = self.cust_ents_dict[self.chunk][1]
            for ent in entities:
                if not (ent[2] == ent_label):
                    new_ents.append(ent)
            new_ents.sort()
            self.cust_ents_dict[self.chunk] = [input_text, new_ents]

            # Clear warning message
            self.msg.config(text="")
        except:
            self.msg.config(text="WARNING!! The entity you tried to remove does not exist.", foreground="red")

    def toggle_metadata(self):
        """
        A button toggle to introduce/remove entry boxes for setting metadata for the json file.
        """
        self.metadata_toggle = not self.metadata_toggle

        if self.metadata_toggle:
            self.text.pack(side=tk.LEFT, padx=(30,0))
            self.doc_label.pack(side=tk.TOP)
            self.doc_entry.pack(side=tk.TOP, pady=(0,10))
            self.url_label.pack(side=tk.TOP)
            self.url_entry.pack(side=tk.TOP, pady=(0,10))
            self.date_label.pack(side=tk.TOP)
            self.date_entry.pack(side=tk.TOP, pady=(0,10))
        else:
            self.text.pack(side=tk.TOP)
            self.doc_label.pack_forget()
            self.doc_entry.pack_forget()
            self.url_label.pack_forget()
            self.url_entry.pack_forget()
            self.date_label.pack_forget()
            self.date_entry.pack_forget()

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

        dir = fd.askdirectory()
        # Do nothing if the user presses cancel or X
        if dir == "":
            return

        self.model_dir = dir
        try:
            self.nlp_agdata = spacy.load(self.model_dir)
            lang = self.nlp_agdata.lang # Attribute error thrown if valid language model is not selected
            self.msg.config(text="NOTE: Model for "+lang+" language identified", foreground="orange")
        except OSError:
            self.msg.config(text="WARNING!!: Selected folder does not contain valid language model \n"
                                 "Default model 'en_core_web_lg' will be used.", foreground="red")
            self.nlp_agdata = spacy.load("en_core_web_lg")
            # Resize window to fit error (it'll push buttons below the bottom if you don't
            # do this and the window has been resized before)
            new_height = self.rootWin.winfo_reqheight() + 15
            self.rootWin.geometry(str(self.rootWin.winfo_reqwidth()) + "x" + str(new_height))
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
        # Clear warning message, if one exists
        self.msg.config(text="")

        # file type
        if file_type == "json":
            filetypes = [("json files", "*.json")]
        elif file_type == "pdf/txt":
            filetypes = [("data files", "*.pdf *.txt")]

        # show the open file dialog
        f = fd.askopenfile(filetypes=filetypes)

        # do nothing is no file is chosen
        if f is None:
            self.msg.config(text="No file was chosen", foreground="red")
            return
        elif file_type == "json":
            self.next_btn.pack_forget()
            self.annotation_file = f
            self.file_prefix = self.annotation_file.name.split(".")[0]
            self.file_name = self.annotation_file.name.split("/")[-1]
            self.working_file_label.config(text="Working Annotation File: "+str(self.annotation_file.name.split("/")[-1]))
            self.json_initialized = True
            self.raw_file=None
            self.review_annotations()
        elif file_type == "pdf/txt":

            self.raw_file=f

            # Ends the operation if a raw file wasn't selected
            if self.raw_file is None:
                self.msg.config(text="No raw data file has been selected. Please select a file to load.", foreground="red")
                return

            # Detects file type
            self.file_mode = self.raw_file.name.split(".")[-1]

            self.page_entry.delete(0, tk.END)

            if self.file_mode == "pdf":
                # Bring back the "Next Page" button, placing it before the save button.
                self.save_btn.pack_forget()
                self.next_btn.pack(side=tk.LEFT)
                self.save_btn.pack(side=tk.LEFT)
                self.page_entry.insert(0, "1")
            else:
                # Remove "Next Page" button if loading a txt file, which has no pages.
                self.next_btn.pack_forget()

            self.file_prefix = self.raw_file.name.split(".")[0]
            self.file_name = self.raw_file.name.split("/")[-1]
            self.pdf_document = None
            self.annotation_file = None
            self.json_initialized = False

            # Reset metadata
            self.working_file_label.config(text="Working Annotation File: "+str(self.annotation_file))
            self.doc_entry.delete(0, tk.END)
            self.doc_entry.insert(0, self.file_name)
            self.url_entry.delete(0, tk.END)
            self.date_entry.config(state=tk.NORMAL)
            self.date_entry.delete(0, tk.END)
            self.date_entry.insert(0, "File not initialized")
            self.date_entry.config(state=tk.DISABLED)

            self.load_page()
        else:
            self.msg.config(text="Warning!! Please select a valid file.", foreground="red")

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
        # Past this point, only single spaces that aren't next to a dash should exist.
        if(self.is_spaced_range(entry)):
            self.msg.config(text="You have entered two numbers with spacing in between. Loading those pages and the pages between them.", foreground="orange")
            entry = entry.replace(" ", "-")
            # Replace user entry with how the program has read it.
            self.page_entry.delete(0, tk.END)
            self.page_entry.insert(0, entry)
        return entry

    def load_page_from_button(self, event=None):
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
        # TODO: Currently only loads 1 page. Update to load arbitrary number of pages (max=size of document).
        # TODO: Give users the option to load text files in addition to pdf files.
        # TODO: Update self.annotation_file. This become an issue if a user opened an annotation file and then decides
        # to annotate a new page. The old annotation file name will be in self.annotation_file which can result in a
        # user overwriting the file

        if self.raw_file is None:
            self.msg.config(text="No raw data file has been selected. Please select a file to load.", foreground="red")

        # Reset annotation dictionary
        self.cust_ents_dict = {}

        # Delete contents
        self.text.delete(1.0, tk.END)

        # Calls pyxpdf in case the file is a PDF, otherwise reads as txt
        if self.file_mode == "pdf":
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

            # Load PDF file
            if self.pdf_document is None:
                self.pdf_document = Document(self.raw_file.name)

            self.handle_bad_page_requests(page_num_valid)

            if not (page_num_valid == -1): # Single page, whether page_num_valid is true or false
                page = self.pdf_document[self.page_number - 1]
                # doesn't necessarily have to be removed for a single page; It gets removed in
                # the else because tagging across multiple pages doesn't work correctly if exists.
                # However, it's removed here as well for consistency and neatness.
                txt = page.text().replace("\r", "").replace("", "")
            else: # Page range
                txt = ""
                for page in self.pdf_document[self.page_number[0] - 1 : self.page_number[1]]:
                    txt = txt + page.text().replace("\r", "").replace("", "")
        else:
            self.page_number = 0
            self.chunk = self.page_number
            txt = self.raw_file.read().replace("\r", "").replace("", "")
            self.raw_file.seek(0)

        self.text.insert(1.0,txt)
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

    def get_pos(self, ent):
        '''
        Proceses a given entity with rules that use pos tag data to expand
        the entity span if needed.
        :param ent: entity to possibly expand span of
        :param nlp: spacy model for pos tagging
        :returns: entity, with an expanded span if needed
        '''
        doc = self.pos_model(ent.sent.text)
        if(len(doc[ent.start:ent.end]) > 0):
            current_index = doc[ent.start:ent.end][0].i
            label = ent.label_
            # functions that expands ents to contain proceeding adjectives
            ent = self.adj_combine_noun_ent(doc, current_index, ent, label)
        return ent

    def adj_combine_noun_ent(self, doc, current_index, ent, label):
        '''
        If the first token in an entity is a noun or proper noun, finds
        all adjectives proceeding the entity and expands the span to
        contain all of them.
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
                    print("entity: " + str(ent))
                    i = current_index
                    start_index = ent.start
                    # keeps searching until all adjectives are found
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

    def pre_tag(self, selection: str):
        """
        Pre-tag selected content or all the text in text box with NER tags.

        Parameters
        ----------
        selection : str
            String specifying the type tagging to be done.

        If a user has selected a block of text and clicked the "Pre-Tag Selection" button, the selected text will be
        tagged and annotation displayed in the text box.

        If they clicked the "Pre-Tag Pages(s)" button, all the text loaded in the text box will be annotated.
        """
        # Clear warning message, if one exists
        self.msg.config(text="")

        # Checks if there is an active NER model
        if self.model_dir is None:
            self.msg.config(text="Warning!! Unable to pre-tag. No NER model selected.", foreground="red")
        # Pre-tag with NER model
        else:
            if selection == "selection":
                if (len(self.text.tag_ranges("sel")) > 0):
                    input_text =  self.text.get("sel.first", "sel.last")
                else:
                    self.msg.config(text="No selection detected; no text was tagged.", foreground="red")
                    return
            else:
                if self.raw_file is None:
                    self.msg.config(text="Warning!! No PDF or txt file was detected. Attempting to tag what's currently in the text box.", foreground="red")
                    # Will pre-tag whatever's in the current text box without trying to load data.
                    input_text = self.text.get(1.0, "end")
                else:
                    input_text = self.load_page()

            if not self.json_initialized:
                self.initialize_new_file()

            self.text.delete(1.0, tk.END)
            self.text.insert(1.0, input_text)

            # Reset annotation dictionary
            self.cust_ents_dict = {}

            # Update variable that holds number of lines in textbox. You need this for
            # the function highlight_ent to work
            self.update_scrolled_text_line_content_index()
            doc = self.tag_ner_with_spacy(input_text)

            custom_tags_present = False

            if type(self.page_number) is list:
                page_start = self.page_number[0]
            else:
                page_start = self.page_number

            for ent in doc.ents:
                # NER is in our list of custom tags
                if ent.label_ in self.tags:
                    custom_tags_present = True
                    # index = self.tags.index(ent.label_) # Find index for an element in a list
                    self.highlight_ent(ent.start_char, ent.end_char, ent.label_)
                    if self.cust_ents_dict.get(page_start, False):
                        self.cust_ents_dict[page_start].append((ent.start_char, ent.end_char, ent.label_))
                    else:
                        self.cust_ents_dict[page_start] = [(ent.start_char, ent.end_char, ent.label_)]

            if not custom_tags_present:
                self.msg.config(text="No custom agriculture tags detected in the text!", foreground="red")
            if len(doc.ents) == 0:
                self.msg.config(text="No entities detected in the text!", foreground="red")

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

    def initialize_new_file(self):
        self.json_initialized = True
        self.working_file_label.config(text="Working Annotation File: Untitled.json")
        self.date_entry.config(state=tk.NORMAL)
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, datetime.now().strftime("%m_%d_%Y_%H_%M_%S"))
        self.date_entry.config(state=tk.DISABLED)

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
                self.initialize_new_file()
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
        try:
            (selection_start, selection_end) = self.get_selected_interval()
        except:
            self.msg.config(text="No selection detected!", foreground="red")
            return

        new_ents = []
        overlapping_tags = []
        input_text = self.cust_ents_dict[self.chunk][0]
        entities = self.cust_ents_dict[self.chunk][1]

        # Loop through tags and find ones that overlap with selected region and remove them.
        for (start, end, label) in entities:
            if not self.overlap([selection_start, selection_end], [start, end]):
                new_ents.append((start, end, label))
            else:
                overlapping_tags.append((start, end, label))
        if len(overlapping_tags) == 0:
            self.msg.config(text="Warning!! It appears the region you selected ("+str(selection_start)+
                                 "-"+str(selection_end)+") did not overlap with a tag.", foreground="red")
        else:
            for (start, end, label) in overlapping_tags:
                # Removes tag using the tag's actual indices instead of the selection's indices
                self.text.tag_remove(label, f"1.0+{start}c", f"1.0+{end}c")

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
            try:
                data = json_2_dict(self.annotation_file.name)
                train_data = dict_2_mixed_type(data)
                self.get_custom_labels(data)
            except:
                self.msg.config(text="WARNING!!: Couldn't load data from annotation file. Are you sure you loaded a valid json?", foreground="red")
                self.annotation_file = None
                return
            """
            doc = data['doc']
            url = data['url']
            """

            # Updates the 'metadata' panel with information from json file, if info is different or invalid then the user is instructed to verify the data in a proper format.
            try:
                self.doc_entry.delete(0, tk.END)
                self.doc_entry.insert(0, data['doc'])
                self.url_entry.delete(0, tk.END)
                self.url_entry.insert(0, data['url'])
                self.date_entry.config(state=tk.NORMAL)
                self.date_entry.delete(0, tk.END)
                self.date_entry.insert(0, data['date'])
                self.date_entry.config(state=tk.DISABLED)
            except:
                self.msg.config(text="Error retrieving metadata; please verify metadata manually", foreground="red")
                self.date_entry.config(state=tk.NORMAL)


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

            self.text.insert(1.0, annotated_text + '\n')

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

    def file_save(self):
        """
        Brings up a file dialog to choose a file name/location then saves annotations to it in .json format.
        """

        if self.cust_ents_dict:
            # Opens a tkinter save as file dialog and stores the file to a var
            json_file = fd.asksaveasfile(initialfile=self.file_name.split(".")[0]+"_pg"+str(self.page_number)+".json", mode='w', defaultextension='.json')

            if json_file is None or json_file.name[-4:] != "json":
                self.msg.config(text="Invalid file or no file chosen; annotations not saved.", foreground="red")
                return
            else:
                self.annotation_file = json_file
                self.working_file_label.config(text="Working Annotation File: "+str(self.annotation_file.name.split("/")[-1]))

            input_text = self.cust_ents_dict[self.chunk][0]
            entities = self.cust_ents_dict[self.chunk][1]

            # Calls dict_2_json on the newly created json file
            ann_train_dict = mixed_type_2_dict([(input_text,{'entities': entities})], self.chunk, self.doc_entry.get(), self.url_entry.get(), self.date_entry.get())
            dict_2_json_file(ann_train_dict, json_file)

            json_file.close()
            self.msg.config(text="Data successfully saved!", foreground="orange")
        else:
            self.msg.config(text="No NER data detected to save", foreground="red")


    def next_page(self):
        """
        Load the next page.
        """
        if self.file_mode == "pdf":
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
        else:
            self.msg.config(text="Warning!! No PDF is currently loaded, so the next page of it can't be loaded either.", foreground="red")

    def go(self):
        """
        Start running the GUI running.
        """
        self.rootWin.mainloop()

    def quit(self):
        """
        Callback method attached to the quit button.

        It check for unsaved changes and opens a save dialog window, otherwise it destroys the main window, which ends the program
        """
        # Creates a save dialog window if there are annotations in the workspace
        if self.cust_ents_dict:

            # Button for saving and quitting that invokes save dialog
            def save_and_quit():
                """
                Callback method attached to the save and quit button in the save dialog window.
                """
                self.file_save()
                self.rootWin.destroy()

            # Button for discaring changes and quitting
            def discard_and_quit():
                """
                Callback method attached to the discard and quit button in the save dialog window.
                """
                self.rootWin.destroy()

            self.save_dialog = tk.Toplevel(self.rootWin)
            label = tk.Label(self.save_dialog, text="You currently have annotations in the workspace. Would you like to save or discard them?")
            label.pack(side=tk.TOP)
            savedialog_discard = tk.Button(self.save_dialog, text="Discard and Quit", command=discard_and_quit)
            savedialog_discard.pack(side=tk.BOTTOM)
            savedialog_confirm = tk.Button(self.save_dialog, text="Save", command=save_and_quit)
            savedialog_confirm.pack(side=tk.BOTTOM)
        else:
            self.rootWin.destroy()



# Driver code
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='runs GUI with option for default model and file',
        epilog='python src/CropNerGUI --model senter_ner_model/model-best --file Data/CSU/Bill-Brown-Reprint.pdf'
        )
    parser.add_argument(
        '--model', help='path to trained model',
        action='store', default=None
        )
    parser.add_argument(
        '--file', help='path to directory of dataset',
        action='store', default=None
        )
    args = parser.parse_args()
    model, file = args.model, args.file
    ner_gui = CropNerGUI(model_default=model, file_default=file)
    ner_gui.go()
