import PIL.Image as Image
import PIL.ImageTk as ImageTk
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from functools import partial
from agParse import *

class nerModel():
    def __init__(self):
        self.name = "Hello"

    def getName(self):
        return self.name


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
            #self.cust_ents.sort()
            #print(self.cust_ents)
        except tk.TclError:
            self.msg.config(text="Warning!! No text was selected.", foreground="red")

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
            print(ents)

        if(self.line_num == (self.page_lines - 1)):
            self.msg.config(text="Warning!! No more sentences.", foreground="red")
        else:
            # Add next line
            self.cust_ents=[]
            self.line_num = self.line_num + 1
            self.text.delete(1.0, tk.END)
            self.text.insert(tk.END, self.content[self.line_num])

        #print("TRAIN DATA=\n",self.TRAIN_DATA)

    def open_text_file(self):
        # file type
        filetypes = (
            ('text files', '*.txt'),
            ('All files', '*.*')
        )

        # show the open file dialog
        f = fd.askopenfile(filetypes=filetypes)

        # Delete contents
        self.text.delete(1.0, tk.END)

        # read the text file and show its content on the Text
        self.content = f.readlines()
        self.line_num = 0
        self.page_lines = len(self.content)
        self.text.insert(tk.END, self.content[self.line_num])

    def file_save(self):
        f = fd.asksaveasfile(mode='w', defaultextension=".txt")
        if f is None:  # asksaveasfile return `None` if dialog closed with "cancel".
            return
        f.write('TRAIN_DATA = '+str(self.TRAIN_DATA)+"\n")
        f.close()

    def go(self):
        """This takes no inputs, and sets the GUI running"""
        self.rootWin.mainloop()

    def quit(self):
        """This is a callback method attached to the quit button.
        It destroys the main window, which ends the program"""
        self.rootWin.destroy()

model = nerModel()

LARGEFONT =("Verdana", 35)
class tkinterApp(tk.Tk):
    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("GEMS NER Annotation Tool")
        self.geometry('1100x400')

        # creating a container
        container = tk.Frame(self)
        container.pack(side = "top", fill = "both", expand = True)

        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        #   initializing frames to an empty array
        self.frames = {}

        # iterating through a tuple consisting
        # of the different page layouts
        for F in (WelcomePage, Annotate, Review):

            frame = F(container,self)

            # initializing frame of that object from
            # WelcomePage, Annotate, Review respectively with
            # for loop
            self.frames[F] = frame

            frame.grid(row = 0, column = 0, sticky ="nsew")

        self.show_frame(WelcomePage)

    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

# first window frame WelcomePage

class WelcomePage(tk.Frame):
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)

        top_frame = tk.Frame(self)
        top_frame.grid(row=0, column=0)
        
        # label of frame Layout 2
        label = ttk.Label(top_frame, text ="NER Crop Annotation Tool", font = LARGEFONT)

        # putting the grid in its place by using
        # grid
        label.grid(row = 0, column = 0, padx = 10, pady = 10)
        
        button_frame = tk.Frame(self)
        button_frame.grid(row=1, column=0)

        annotate_button = ttk.Button(button_frame, text ="Annotate", width=17,
                     command = lambda : controller.show_frame(Annotate))

        # putting the button in its place by
        # using grid
        annotate_button.grid(row = 0, column = 0, padx = 10, pady = 10)

        ## button to show frame 2 with text layout2
        review_button = ttk.Button(button_frame, text ="Review Annotation",width=17,
                     command = lambda : controller.show_frame(Review))

        # putting the button in its place by
        # using grid
        review_button.grid(row = 0, column = 1, padx = 10, pady = 10)

        img_frame = tk.Frame(self)
        img_frame.grid(row=2, column=0)
        tPic = Image.open("logo.png")
        logo_pic = ImageTk.PhotoImage(tPic)   # IMAGES MUST ALWAYS BE OBJECT VARIABLES!!
        imgLabel = tk.Label(img_frame, image=logo_pic)
        imgLabel.image=logo_pic
        #imgLabel = tk.Label(img_frame, text="Hello")
        imgLabel.grid(row=0, column=0)

# second window frame Annotate
class Annotate(tk.Frame):
    
    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)

        self.content = ["Hello World!"]
        self.line_num = 0

        top_frame = tk.Frame(self)
        top_frame.grid(row=0, column=0)

        label = ttk.Label(top_frame, text ="Tag Crop Named Entities", font = LARGEFONT)
        label.grid(row = 0, column = 0, padx = 10, pady = 10)


        button_frame = tk.Frame(self)
        button_frame.grid(row=1, column=0)

        # button to show frame 2 with text
        # layout2
        welcome_button = ttk.Button(button_frame, text ="Welcome Page",width=17,
                     command = lambda : controller.show_frame(WelcomePage))

        # putting the button in its place
        # by using grid
        welcome_button.grid(row = 0, column = 0, padx = 10, pady = 10)

        # button to show frame 2 with text
        # layout2
        review_button = ttk.Button(button_frame, text ="Review Annotation",width=17,
                     command = lambda : controller.show_frame(Review))

        # putting the button in its place by
        # using grid
        review_button.grid(row = 0, column = 1, padx = 10, pady = 10)

        tags_frame = tk.Frame(self)
        tags_frame.grid(row=2, column=0)
        # NOTE: A partial function is created from another function, where some of the parameters are fixed.
        # In the instance below, we want to call the function self.get_ner (which takes a single input) several
        # times but each time we pass it a different value depending on the button that was clicked. If the ALAS
        # button is clicked, we want to pass the text "ALAS" but if the "CROP" button was clicked we want to pass the
        # text CROP. So, partial(self.get_ner, "ALAS") is the same as self.get_ner("ALAS")

        # Named entity buttons
        self.alas_btn = tk.Button(tags_frame, highlightbackground="violet", text="ALAS",
                                  command=partial(model.get_ner, "ALAS"))
        self.alas_btn.pack(side=tk.LEFT)
        self.crop_btn = tk.Button(tags_frame, highlightbackground="lawn green", text="CROP",
                                  command=partial(model.get_ner, "CROP"))
        self.crop_btn.pack(side=tk.LEFT)
        self.cvar_btn = tk.Button(tags_frame, highlightbackground="deep sky blue", text="CVAR",
                                  command=partial(model.get_ner, "CVAR"))
        self.cvar_btn.pack(side=tk.LEFT)
        self.jrnl_btn = tk.Button(tags_frame, highlightbackground="yellow", text="JRNL",
                                  command=partial(model.get_ner, "JRNL"))
        self.jrnl_btn.pack(side=tk.LEFT)
        self.path_btn = tk.Button(tags_frame, highlightbackground="red", text="PATH",
                                  command=partial(model.get_ner, "PATH"))
        self.path_btn.pack(side=tk.LEFT)
        self.ped_btn = tk.Button(tags_frame, highlightbackground="orange", text="PED",
                                 command=partial(model.get_ner, "PED"))
        self.ped_btn.pack(side=tk.LEFT)
        self.plan_btn = tk.Button(tags_frame, highlightbackground="pink", text="PLAN",
                                  command=partial(model.get_ner, "PLAN"))
        self.plan_btn.pack(side=tk.LEFT)
        self.pptd_btn = tk.Button(tags_frame, highlightbackground="brown", text="PPTD",
                                  command=partial(model.get_ner, "PPTD"))
        self.pptd_btn.pack(side=tk.LEFT)
        self.trat_btn = tk.Button(tags_frame, highlightbackground="MediumPurple1", text="TRAT",
                                  command=partial(model.get_ner, "TRAT"))
        self.trat_btn.pack(side=tk.LEFT)

        self.spaceLabel = tk.Label(tags_frame, text="    ", width=17)
        self.spaceLabel.pack(side=tk.LEFT)

        self.clearTag_btn = tk.Button(tags_frame, text="Remove-Tag", command=partial(model.clear_tag))
        self.clearTag_btn.pack(side=tk.LEFT)
        self.pretag_btn = tk.Button(tags_frame, text="Pre-Tag", command=partial(model.pre_tag))
        self.pretag_btn.pack(side=tk.LEFT)

        text_frame = tk.Frame(self)
        text_frame.grid(row=3, column=0)

        # adding the text
        self.text = tk.Text(text_frame, height=8, font="Times 24")
        self.text.insert(tk.END, self.content[self.line_num])
        self.text.focus_force()
        self.text.grid(row=0, column=0, columnspan=4, padx=5, pady=5)


# third window frame Review
class Review(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        top_frame = tk.Frame(self)
        top_frame.grid(row=0, column=0)

        label = ttk.Label(top_frame, text ="Review       Annotation", font = LARGEFONT)
        label.grid(row = 0, column = 4, padx = 10, pady = 10)

        button_frame = tk.Frame(self)
        button_frame.grid(row=1, column=0)

        # button to show frame 2 with text
        # layout2
        annotate_button = ttk.Button(button_frame, text ="Annotate",width=17,
                     command = lambda : controller.show_frame(Annotate))

        # putting the button in its place by
        # using grid
        annotate_button.grid(row = 0, column = 1, padx = 10, pady = 10)

        # button to show frame 3 with text
        # layout3
        welcome_button = ttk.Button(button_frame, text ="Welcome Page",width=17,
                     command = lambda : controller.show_frame(WelcomePage))

        #    putting the button in its place by
        # using grid
        welcome_button.grid(row = 0, column = 0, padx = 10, pady = 10)






# Driver Code
app = tkinterApp()
app.mainloop()

