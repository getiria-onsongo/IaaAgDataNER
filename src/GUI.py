import tkinter as tk
from tkinter import filedialog as fd
from functools import partial


# create a NER GUI class
class NERgui:
    def __init__(self):
        # Create a GUI window
        self.rootWin = tk.Tk()
        #self.rootWin.option_add('*Font', 'Times 24')
        self.rootWin.title("NER Annotation")

        self.rootWin.geometry('1100x400')

        self.content=["Pandemic has resulted in economic slowdown worldwide. People are tired. "]
        self.line_num = 0
        self.page_lines = 1

        self.topframe = tk.Frame(self.rootWin)
        self.topframe.grid(row=0, column=0)

        # Named entity buttons
        self.alas_btn = tk.Button(self.topframe, text="ALAS", command=partial(self.get_ner, "ALAS","alas_color_tag"))
        self.alas_btn.pack(side = tk.LEFT)

        self.crop_btn = tk.Button(self.topframe, text="CROP", command=partial(self.get_ner, "CROP","crop_color_tag"))
        self.crop_btn.pack(side = tk.LEFT)

        self.cvar_btn = tk.Button(self.topframe, text="CVAR", command=partial(self.get_ner, "CVAR","cvar_color_tag"))
        self.cvar_btn.pack(side = tk.LEFT)

        self.jrnl_btn = tk.Button(self.topframe, text="JRNL", command=partial(self.get_ner, "JRNL","jrnl_color_tag"))
        self.jrnl_btn.pack(side = tk.LEFT)

        self.path_btn = tk.Button(self.topframe, text="PATH", command=partial(self.get_ner, "PATH","path_color_tag"))
        self.path_btn.pack(side = tk.LEFT)

        self.ped_btn = tk.Button(self.topframe, text="PED", command=partial(self.get_ner, "PED","ped_color_tag"))
        self.ped_btn.pack(side = tk.LEFT)

        self.plan_btn = tk.Button(self.topframe, text="PLAN", command=partial(self.get_ner, "PLAN","plan_color_tag"))
        self.plan_btn.pack(side = tk.LEFT)

        self.pptd_btn = tk.Button(self.topframe, text="PPTD", command=partial(self.get_ner, "PPTD","pptd_color_tag"))
        self.pptd_btn.pack(side = tk.LEFT)

        self.trat_btn = tk.Button(self.topframe, text="TRAT", command=partial(self.get_ner, "TRAT","trat_color_tag"))
        self.trat_btn.pack(side = tk.LEFT)

        # adding the text
        self.text = tk.Text(self.rootWin, height=8, font = "Times 24")
        self.text.insert(tk.END, self.content[self.line_num])
        self.text.focus_force()

        #self.text.tag_configure("test", background="yellow", foreground="red")
        #self.text.tag_add("test", "1.1", "1.5")

        self.text.grid(row=1, column=0, columnspan = 4,padx=5, pady=5)

        # configuring a tag called start which will be used to highlight the text
        self.text.tag_configure("highlight", foreground="black", background="red")

        self.text.tag_configure("default_color_tag", foreground="black")
        self.text.tag_configure("alas_color_tag", foreground="blue")
        self.text.tag_configure("crop_color_tag", foreground="green")
        self.text.tag_configure("cvar_color_tag", foreground="violet")
        self.text.tag_configure("jrnl_color_tag", foreground="gold")
        self.text.tag_configure("path_color_tag", foreground="red")
        self.text.tag_configure("ped_color_tag", foreground="orange")
        self.text.tag_configure("plan_color_tag", foreground="pink")
        self.text.tag_configure("pptd_color_tag", foreground="brown")
        self.text.tag_configure("trat_color_tag", foreground="purple")


        self.bottom_frame = tk.Frame(self.rootWin)
        self.bottom_frame.grid(row=2, column=0)

        # Exit button
        self.exit_btn = tk.Button(self.bottom_frame, text="Exit",width=10,command=self.quit)
        self.exit_btn.pack(side = tk.LEFT)

        # Highlight button
        self.bold_btn = tk.Button(self.bottom_frame, text="Highlight Text",width=10, command=self.highlight_text)
        self.bold_btn.pack(side = tk.LEFT)

        # Clear button
        self.clear_btn = tk.Button(self.bottom_frame, text="Clear",width=10, command=self.clear_highlight)
        self.clear_btn.pack(side = tk.LEFT)

        # Clear message button
        self.msg_btn = tk.Button(self.bottom_frame, text="Clear Warning Message", width=20, command=self.clear_message)
        self.msg_btn.pack(side=tk.LEFT)

        # Next line button
        self.next_btn = tk.Button(self.bottom_frame, text="Next Line", command=self.nextline)
        self.next_btn.pack(side = tk.LEFT)

        self.msg_frame = tk.Frame(self.rootWin)
        self.msg_frame.grid(row=3, column=0)

        # Label to display messages
        self.msg = tk.Label(self.msg_frame, text="", padx=5, pady=5)
        self.msg.pack(side=tk.LEFT)

        # open file button
        self.open_button = tk.Button(self.rootWin,text='Open a File',command=self.open_text_file )
        self.open_button.grid(row=1,column=4,  sticky='w', padx=5, pady=5)

    # method to highlight the selected text
    def highlight_text(self):
        # if no text is selected then tk.TclError exception occurs
        try:
            self.text.tag_add("highlight", "sel.first", "sel.last")
            print(self.text.get("sel.first", "sel.last"))
        except tk.TclError:
            self.msg.config(text="Warning!! No text was selected.",foreground="red")

    def clear_message(self):
        self.msg.config(text="")

    # method to clear all contents from text widget.
    def clear_highlight(self):
        self.text.tag_remove("highlight", "1.0", 'end')

        for tag in self.text.tag_names():
            self.text.tag_remove(tag, "1.0", "end")

        self.msg.config(text="")


    def get_ner(self,label,tagLabel):
        # if no text is selected then tk.TclError exception occurs
        try:
            self.text.tag_add(tagLabel, "sel.first", "sel.last")
            print(self.line_num, self.text.get("sel.first", "sel.last"),label)
        except tk.TclError:
            self.msg.config(text="Warning!! No text was selected.", foreground="red")

    def nextline(self):
        # Delete contents
        if(self.line_num == (self.page_lines - 1)):
            self.msg.config(text="Warning!! No more sentences.", foreground="red")
        else:
            # Add next line
            self.line_num = self.line_num + 1
            self.text.delete(1.0, tk.END)
            self.text.insert(tk.END, self.content[self.line_num])

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
