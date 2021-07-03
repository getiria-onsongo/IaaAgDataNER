# program taken from http://stackoverflow.com/questions/4969543/colour-chart-for-tkinter-and-tix-using-python
#
from tkinter import *
from tkinterColorList import  *

MAX_ROWS = 36
FONT_SIZE = 10 # (pixels)

MAX_ROWS = 36
FONT_SIZE = 10 # (pixels)

root = Tk()
root.title("Named colour chart")
row = 0
col = 0
for color in color_list:
  e = Label(root, text=color, background=color,
        font=(None, -FONT_SIZE))
  e.grid(row=row, column=col, sticky=E+W)
  row += 1
  if (row > 36):
    row = 0
    col += 1

root.mainloop()