#!/usr/bin/env python3
from tkinter import *
from tkinter import ttk, filedialog, messagebox
from FileLogic import get_file
from Processing import find_LOC_and_params
from Refactoring import find_duplicates, refactor_duplicates

loaded_path = ""
original_contents = []

root = Tk()
root.title("Code Smell Detector")
frame = ttk.Frame(root, padding=10)
frame.grid()

title_label = ttk.Label(frame, text="Code Smell Detector")
status_label = ttk.Label(frame, text="No file loaded", relief="sunken")
LOC_label = ttk.Label(frame, text="Long Method/Function not detected.", relief="raised")
params_label = ttk.Label(frame, text="Long Parameter List not detected.", relief="raised")
duplicates_label = ttk.Label(frame, text="Duplicate Code not detected.", relief="raised")
load_btn = ttk.Button(frame, text="Load .py File", command=lambda: load_file(status_label))
quit_btn = ttk.Button(frame, text="Quit", command=root.destroy)
codesmell_btn = ttk.Button(frame, text="Find Code Smells", command=lambda: find_codesmells(LOC_label, params_label, duplicates_label))
refactor_btn = ttk.Button(frame, text="Refactor Duplicate Code")

# pre :
# post:
def load_file(status_label):
    global loaded_path, original_contents
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

# pre :
# post:
def find_codesmells(LOC_label, params_label, duplicates_label):
    global original_contents
    long_methods, long_parameters = find_LOC_and_params(original_contents)
    duplicate_code = find_duplicates(original_contents)
    if long_methods: 
        LOC_label.config(text="Long Method/Function(s) detected!")
    if long_parameters:
        params_label.config(text="Long Parameter List(s) detected!")
    if duplicate_code:
        duplicates_label.config(text="Duplicate Code detected!")
    activate_codesmell_labels()

# pre :
# post:
def activate_codesmell_labels():
    LOC_label.grid(column=0, row=3)
    params_label.grid(column=0, row=4)
    duplicates_label.grid(column=0, row=5)

#TODO:
def refactor_duplicate_code():
    print()

def create_refactored():
    print()

title_label.grid(column=0, row=0, columnspan=2, pady=(0,10))
load_btn.grid(column=0, row=1, sticky="w", padx=(0,5))
quit_btn.grid(column=1, row=1, sticky="e", padx=(5,0))
status_label.grid(column=0, row=2, columnspan=2, sticky="we", pady=(10,0))

frame.columnconfigure(0, weight=1)
frame.columnconfigure(1, weight=1)
root.mainloop()