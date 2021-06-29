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
class CropNerGUIv2:
    def __init__(self):
        # Create a GUI window
        self.rootWin = tk.Tk()
        #self.rootWin.option_add('*Font', 'Times 24')
        self.rootWin.title("GEMS NER Annotation Tool")

        self.rootWin.geometry('1500x900')

        self.font_size = "20"
        self.content = [""]
        self.custom_ents = {}
        self.line_num = 0

        self.topframe = tk.Frame(self.rootWin)
        self.topframe.grid(row=0, column=0)

        self.alas_btn = tk.Button(self.topframe, highlightbackground="violet", text="ALAS",
                                  command=partial(self.get_ner, "ALAS"))
        self.alas_btn.pack(side=tk.LEFT)

        # adding the text: Note, height defines height if widget in lines based in font size
        self.text = ScrolledText(self.rootWin, height=25, width=140, font="Times " + self.font_size)
        self.text.insert(tk.END, self.content[self.line_num])
        self.text.focus_force()
        self.text.grid(row=1, column=0, columnspan=4, padx=5, pady=5)

        self.bottom_frame = tk.Frame(self.rootWin)
        self.bottom_frame.grid(row=2, column=0)

        # Exit button
        self.exit_btn = tk.Button(self.bottom_frame, text="Exit", width=10, command=self.quit)
        self.exit_btn.pack(side=tk.LEFT)

        self.traitLabel = tk.Label(self.bottom_frame, text="Enter Entity Label:", width=20)
        self.traitLabel.pack(side=tk.LEFT)
        self.traitEntry = tk.Entry(self.bottom_frame, width=10)
        self.traitEntry.pack(side=tk.LEFT)

        # Add entity button
        self.add_ent_btn = tk.Button(self.bottom_frame, text="Add Entity", width=10, command=self.add_ent)
        self.add_ent_btn.pack(side=tk.LEFT)

        # Remove entity button
        self.remove_ent_btn = tk.Button(self.bottom_frame, text="Remove Entity", width=10, command=self.remove_ent)
        self.remove_ent_btn.pack(side=tk.LEFT)

    def go(self):
        """This takes no inputs, and sets the GUI running"""
        self.rootWin.mainloop()

    def quit(self):
        """This is a callback method attached to the quit button.
        It destroys the main window, which ends the program"""

        self.rootWin.destroy()

    def get_ner(self, tagLabel):
        print(tagLabel)

    def add_ent(self):
        ent_label = self.traitEntry.get().upper()
        ent_btn = tk.Button(self.topframe, highlightbackground="lawn green", text=ent_label,command=partial(self.get_ner, ent_label))
        ent_btn.pack(side=tk.LEFT)
        self.custom_ents[ent_label] = ent_btn

    def remove_ent(self):
        ent_label = self.traitEntry.get().upper()
        ent_btn = self.custom_ents[ent_label]
        ent_btn.pack_forget()

# Driver code
if __name__ == "__main__":
    myGui = CropNerGUIv2()
    myGui.go()