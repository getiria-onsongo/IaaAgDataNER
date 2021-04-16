import tkinter as tk
from tkinter import filedialog as fd
from functools import partial
from agParse import *
from py2json import *

# TO DO NEXT:
# 1) Add code to load model, tag sentence and highlight text


# create a NER GUI class
class CropNerGUI:
    def __init__(self):
        # Create a GUI window
        self.rootWin = tk.Tk()
        #self.rootWin.option_add('*Font', 'Times 24')
        self.rootWin.title("GEMS NER Annotation Tool")

        self.rootWin.geometry('1100x400')

        self.content=[""]
        self.file=""
        self.annotation_file = ""
        self.nlp_agdata = ""

        self.cust_ents = []
        self.TRAIN_DATA = []
        self.output_file_name = "sample_p0_td.py"
        self.pageNumber=0
        self.line_num = 0
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

        self.clearTag_btn = tk.Button(self.topframe, text="Remove-Tag", command=partial(self.clear_tag))
        self.clearTag_btn.pack(side=tk.LEFT)
        self.pretag_btn = tk.Button(self.topframe, text="Pre-Tag", command=partial(self.pre_tag))
        self.pretag_btn.pack(side=tk.LEFT)

        # adding the text
        self.text = tk.Text(self.rootWin, height=8, font = "Times 24")
        self.text.insert(tk.END, self.content[self.line_num])
        self.text.focus_force()

        #self.text.tag_configure("test", background="yellow", foreground="red")
        #self.text.tag_add("test", "1.1", "1.5")

        self.text.grid(row=1, column=0, columnspan = 4,padx=5, pady=5)

        # configuring a tag called start which will be used to highlight the text
        self.text.tag_configure("highlight", foreground="black", background="red")

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
        self.load_btn = tk.Button(self.bottom_frame, text="Load Data", width=10, command=self.LoadFirstLine)
        self.load_btn.pack(side=tk.LEFT)



        # Highlight button
        self.bold_btn = tk.Button(self.bottom_frame, text="Highlight Text",width=10, command=self.highlight_text)
        self.bold_btn.pack(side = tk.LEFT)

        # Clear button
        self.clear_btn = tk.Button(self.bottom_frame, text="Clear All Tags",width=10, command=self.clear_highlight)
        self.clear_btn.pack(side = tk.LEFT)

        # Clear message button
        self.msg_btn = tk.Button(self.bottom_frame, text="Clear Warning Message", width=20, command=self.clear_message)
        self.msg_btn.pack(side=tk.LEFT)

        # Next line button
        self.next_btn = tk.Button(self.bottom_frame, text="Next Line", command=self.nextline)
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
        self.open_button = tk.Button(self.open_frame,text='Select Raw Data File(PDF/txt)',width=22,command=partial(self.open_file,"raw"))
        self.open_button.pack(side=tk.LEFT)

        self.pageLabel = tk.Label(self.open_frame, text="Raw Data File Page Num:",width=22)
        self.pageLabel.pack(side=tk.LEFT)

        self.pageEntry = tk.Entry(self.open_frame, width=10)
        self.pageEntry.pack(side=tk.LEFT)

        self.annotation_btn = tk.Button(self.open_frame, text="Select Annotation File(JSON)",width=22,command=partial(self.open_file,"json"))
        self.annotation_btn.pack(side=tk.LEFT)

        self.review_btn = tk.Button(self.open_frame, text="Review Annotations", command=partial(self.pre_tag))
        self.review_btn.pack(side=tk.LEFT)

    # method to highlight the selected text
    def highlight_text(self):
        # if no text is selected then tk.TclError exception occurs
        try:
            self.text.tag_add("highlight", "sel.first", "sel.last")
            print(self.text.index("sel.first"), self.text.index("sel.last"))
        except tk.TclError:
            self.msg.config(text="Warning!! No text was selected.",foreground="red")

    def clear_message(self):
        self.msg.config(text="")

    # method to clear all contents from text widget.
    def clear_highlight(self):
        for tag in self.tags:
            self.text.tag_remove(tag, "1.0", "end")

        self.msg.config(text="")


    def clear_tag(self):
        # if no text is selected then tk.TclError exception occurs
        try:
            h_start = int(self.text.index("sel.first").split(".")[1])
            h_end= int(self.text.index("sel.last").split(".")[1])

            new_ents = []
            for (start, end, label) in self.cust_ents:
                if(not self.overlap([h_start,h_end],[start, end])):
                    new_ents.append((start, end, label))
            self.cust_ents = new_ents

            for tag in self.tags:
                self.text.tag_remove(tag, "sel.first", "sel.last")
        except tk.TclError:
            self.msg.config(text="Warning!! No text was selected.", foreground="red")



    def get_ner(self,tagLabel):
        # NOTE: We need to make this function more robust by first checking
        # if there is an entity overlapping the selected text and remove it before
        # adding a new entity.
        try:
            # Get start and end char positions
            h_start = int(self.text.index("sel.first").split(".")[1])
            h_end = int(self.text.index("sel.last").split(".")[1])

            # Check if selected area overlaps with another NER tag. If it does,
            # delete the existing tag. SpaCy does not allow NER tags to overlap.
            new_ents = []
            for (start, end, label) in self.cust_ents:
                if (not self.overlap([h_start, h_end], [start, end])):
                    new_ents.append((start, end, label))
            self.cust_ents = new_ents

            # Add the new tag
            self.text.tag_add(tagLabel, "sel.first", "sel.last")
            self.cust_ents.append((h_start,h_end,tagLabel))

            # Print to make sure it worked. This code needs to be removed after
            # code has been tested.
            self.cust_ents.sort()
            #print(self.cust_ents)

        except tk.TclError:
            self.msg.config(text="Warning!! get_ner error.", foreground="red")

    def tag_ner_with_spacy(self, text):
        doc = self.nlp_agdata(text)
        return doc

    def pre_tag(self):
        input_text = self.text.get(1.0, tk.END)
        doc = self.tag_ner_with_spacy(input_text)
        for ent in doc.ents:
            #print(ent.text, ent.start_char, ent.end_char, ent.label_)
            if(ent.label_ in self.tags):
                self.text.tag_add(ent.label_, "1."+str(ent.start_char), "1."+str(ent.end_char))
            else:
                self.text.tag_add("highlight", "1." + str(ent.start_char), "1." + str(ent.end_char))
            self.cust_ents.append((ent.start_char, ent.end_char, ent.label_))


    def overlap(self, interva1, interval2):
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

    def nextline(self):

        if(len(self.cust_ents)> 0):
            text = self.content[self.line_num].strip()
            self.cust_ents.sort()
            ents = {'entities': self.cust_ents}
            self.TRAIN_DATA.append((text, ents))
            #print(ents)

        if(self.line_num == (self.page_lines - 1)):
            self.msg.config(text="Warning!! No more sentences.", foreground="red")
        else:
            # Add next line
            self.cust_ents=[]
            self.line_num = self.line_num + 1
            self.text.delete(1.0, tk.END)
            self.text.insert(tk.END, self.content[self.line_num])

        #print("TRAIN DATA=\n",self.TRAIN_DATA)

    def open_file(self, file_type):
        # file type
        filetypes = (
            ('text files', '*.txt'),
            ('json files', '*.json'),
            ('All files', '*.*')
        )

        # show the open file dialog
        f = fd.askopenfile(filetypes=filetypes)
        if(file_type == "json"):
            self.annotation_file = f
        else:
            self.file=f

    def LoadModel(self):
        # Load spacy model
        source_nlp = spacy.load("en_core_web_sm")
        model_dir = "/Users/gonsongo/Desktop/research/iaa/Projects/python/IaaAgDataNER/NerModel/model-best"
        self.nlp_agdata = spacy.load(model_dir)
        self.nlp_agdata.add_pipe("parser", before="ner", source=source_nlp)
        self.nlp_agdata.add_pipe("tagger", before="parser", source=source_nlp)
        # self.nlp_agdata.add_pipe("compound_trait_entities", after='ner')

    def LoadFirstLine(self):
        if isinstance(self.file, str):
            self.msg.config(text="No raw data file has been selected. Please select a file to load.", foreground="red")
        else:
            self.LoadModel()
            # Delete contents
            self.text.delete(1.0, tk.END)

            # read the text file and show its content on the Text
            self.content = self.file.readlines()
            self.line_num = 0
            self.page_lines = len(self.content)
            self.text.insert(tk.END, self.content[self.line_num])


    '''
    I COMMENTED THIS FUNCTION BECAUSE IT IS A LOT SIMPLER TO LOAD A SINGLE LINE AND ANNOTATE PER LINE.
    THIS IS BECAUSE THE ANNOTATION GETS SAVED PER LINE (SENTENCE) 
    WHILE IT MIGHT BE EASIER TO LOAD THE WHOLE PAGE AND VIEW SENTENCES IN CONTEXT, THIS APPROACH WILL MAKE
    THINGS A BIT COMPLICATED. 
    def LoadData(self):
        if isinstance(self.file, str):
            self.msg.config(text="No raw data file has been selected. Please select a file to load.", foreground="red")
        else:
            self.LoadModel()
            # Delete contents
            self.text.delete(1.0, tk.END)

            self.line_num = 0
            file_content = self.file.readlines()
            # read the text file and show its content on the Text
            for line in file_content:
                self.text.insert(tk.END, line)
                self.line_num = self.line_num + 1
            self.page_lines = self.line_num
    '''

    def file_save(self):
        filepath = fd.asksaveasfilename(defaultextension=".json")
        #print(filepath)
        if ((filepath is None) or (len(filepath) == 0)):  # asksaveasfile return `None` if dialog closed with "cancel".
            return

        if(len(self.TRAIN_DATA) == 0):
            # This means the user has not annotated anything
            if (len(self.cust_ents) > 0):
                # This means there were annotations that were not added to the training data.
                # Annotations are added when a user clicks "Next Line"
                text = self.content[self.line_num].strip()
                self.cust_ents.sort()
                ents = {'entities': self.cust_ents}
                self.TRAIN_DATA.append((text, ents))
        train_dict = mixed_type_2_dict(self.TRAIN_DATA, "args.chunk", "args.doc", "args.url")
        dict_2_json(train_dict, filepath)

        #f.write('TRAIN_DATA = '+str(self.TRAIN_DATA)+"\n")
        #f.close()

    def go(self):
        """This takes no inputs, and sets the GUI running"""
        self.rootWin.mainloop()

    def quit(self):
        """This is a callback method attached to the quit button.
        It destroys the main window, which ends the program"""
        self.rootWin.destroy()

# Driver code
if __name__ == "__main__":
    myGui = CropNerGUI()
    myGui.go()
