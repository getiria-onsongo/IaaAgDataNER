import tkinter as tk
import random

# Code to try dyanmically adding buttons
# 
#

print("Hello world")

class App(tk.Frame):

    def __init__(self,):

        super().__init__()

        self.master.title("Hello World")

        self.count = 0
        self.labels = {}

        self.init_ui()

    def init_ui(self):

        self.f = tk.Frame()

        w = tk.Frame()

        tk.Button(w, text="Color", command=self.callback).pack()
        tk.Button(w, text="Close", command=self.on_close).pack()

        w.pack(side=tk.RIGHT, fill=tk.BOTH, expand=0)
        self.f.pack(side=tk.LEFT, fill=tk.BOTH, expand=0)

    def callback(self):

        text_label = "I'm the {} label".format(self.count)
        text_button = "I'm the {} button".format(self.count)

        color = "#" + ("%06x" % random.randint(0, 16777215))
        obj = tk.Label(self.f, text=text_label, bg=color)
        obj.pack()
        self.labels[self.count]=obj
        tk.Button(self.f,
                  text=text_button,
                  command=lambda which=self.count: self.change_color(which)).pack()
        self.count +=1

    def change_color(self,which):

        color = "#" + ("%06x" % random.randint(0, 16777215))
        self.labels[which].config(bg=color)


    def on_close(self):
        self.master.destroy()

if __name__ == '__main__':
    app = App()
    app.mainloop()
