#!/usr/bin/env python3
from tkinter import *
from tkinter import ttk
import FileLogic
import Processing

root = Tk()
root.title("Code Smell Detector")
frame = ttk.Frame(root, padding=10)
frame.grid()
ttk.Label(frame, text="Hello World!").grid(column=0, row=0)
ttk.Button(frame, text="Quit", command=root.destroy).grid(column=0, row=1)
root.mainloop()
