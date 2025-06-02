#!/usr/bin/env python3
from tkinter import *
from tkinter import ttk, filedialog, messagebox
from FileLogic import get_file
from Processing import find_LOC_and_params

root = Tk()
root.title("Code Smell Detector")
frame = ttk.Frame(root, padding=10)
frame.grid()

global loaded_path, original_contents

title_label = ttk.Label(frame, text="Code Smell Detector")
status_label = ttk.Label(frame, text="No file loaded", relief="sunken", anchor="w")
load_btn = ttk.Button(frame, text="Load .py File", command=lambda: load_file(status_label))
quit_btn = ttk.Button(frame, text="Quit", command=root.destroy)
codesmell_btn = ttk.Button(frame, text="Process", command=lambda: find_codesmells())

#
#
def load_file(status_label):
    path = filedialog.askopenfilename(title="Select a Python file to refactor", filetypes=[("Python Files", "*.py")])
    if not path:
        return
    try:
        original_contents = get_file(path)
    except Exception as e:
        messagebox.showerror("Error", f"Could not read file:\n{e}")
        return
    loaded_path = path
    status_label.config(text=f"Loaded: {path}")
    codesmell_btn.grid(column=1, row=2, padx=(5, 0), pady=(5, 0), sticky="e")

#
#
def find_codesmells():
    print()


#TODO: add file input support and UI that is responsive to file upload, and can spit out refactored files
title_label.grid(column=0, row=0, columnspan=2, pady=(0,10))
load_btn.grid(column=0, row=1, sticky="w", padx=(0,5))
quit_btn.grid(column=1, row=1, sticky="e", padx=(5,0))
status_label.grid(column=0, row=2, columnspan=2, sticky="we", pady=(10,0))

frame.columnconfigure(0, weight=1)
frame.columnconfigure(1, weight=1)
root.mainloop()