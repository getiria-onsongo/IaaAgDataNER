import tkinter as tk
from tkinter import filedialog as fd


# create a NER GUI class
class NERgui:
    def __init__(self):
        # Create a GUI window
        self.rootWin = tk.Tk()
        #self.rootWin.option_add('*Font', 'Times 24')
        self.rootWin.title("NER Annotation")

        self.rootWin.geometry('1100x300')

        # ALAS=varietal_alias
        # CROP=crop
        # CVAR=crop_variety
        # JRNL=journal_reference
        # PATH=pathogen,
        # PED=pedigree,
        # PLAN=plant_anatomy
        # PPTD=plant_predisposition_to_disease
        # TRAT=trait

        # ALAS button
        self.exit_btn = tk.Button(self.rootWin, text="ALAS", command=self.clear)
        self.exit_btn.grid(row=0, column=0)

        # adding the text
        self.text = tk.Text(self.rootWin, height=8, font = "Times 24")
        self.text.insert("end", "Pandemic has resulted in economic slowdown worldwide")
        self.text.focus()

        self.text.tag_configure("test", background="yellow", foreground="red")
        self.text.tag_add("test", "1.1", "1.5")

        self.text.grid(row=1, column=0, columnspan = 4,padx=5, pady=5)

        # configuring a tag called start which will be used to highlight the text
        self.text.tag_configure("highlight", background="black", foreground="red")

        # Exit button
        self.exit_btn = tk.Button(self.rootWin, text="Exit", command=self.quit)
        self.exit_btn.grid(row=2, column=0)

        # Highlight button
        self.bold_btn = tk.Button(self.rootWin, text="Highlight", command=self.highlight_text)
        self.bold_btn.grid(row=2, column=1)

        # Clear button
        self.clear_btn = tk.Button(self.rootWin, text="Clear", command=self.clear)
        self.clear_btn.grid(row=2, column=2)

        # Next line button
        self.next_btn = tk.Button(self.rootWin, text="Next", command=self.clear)
        self.next_btn.grid(row=2,column=3)

        # open file button
        self.open_button = tk.Button(self.rootWin,text='Open a File',command=self.open_text_file )
        self.open_button.grid(row=1,column=4,  sticky='w', padx=5, pady=5)



    # method to highlight the selected text
    def highlight_text(self):

        # if no text is selected then tk.TclError exception occurs
        try:
            self.text.tag_add("highlight", "sel.first", "sel.last")
        except tk.TclError:
            pass

    # method to clear all contents from text widget.
    def clear(self):
        print("sel.last")
        self.text.tag_remove("highlight", "1.0", 'end')
        self.text.tag_remove("test", "1.0", 'end')

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
        content = f.readlines()
        self.text.insert('1.0', content[0])




    def go(self):
        """This takes no inputs, and sets the GUI running"""
        self.rootWin.mainloop()

    def quit(self):
        """This is a callback method attached to the quit button.
        It destroys the main window, which ends the program"""
        self.rootWin.destroy()

# Driver code
if __name__ == "__main__":
    myGui = NERgui()
    myGui.go()
