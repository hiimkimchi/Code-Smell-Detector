#!/usr/bin/env python3
from tkinter import *
from tkinter import ttk, filedialog, messagebox
from FileLogic import get_file, produce_refactored
from Processing import find_LOC_and_params
from Refactoring import find_duplicates, refactor_duplicates

loaded_path = ""
original_contents = []
new_contents = []
duplicate_code = None

root = Tk()
root.title("Code Smell Detector")
frame = ttk.Frame(root, padding=10)
frame.grid()

title_label = ttk.Label(frame, text="Code Smell Detector")
status_label = ttk.Label(frame, text="No file loaded", relief="sunken", justify="center")
LOC_label = ttk.Label(frame, text="Long Method/Function not detected.", relief="raised")
params_label = ttk.Label(frame, text="Long Parameter List not detected.", relief="raised")
duplicates_label = ttk.Label(frame, text="Duplicate Code not detected.", relief="raised")
refactor_label = ttk.Label(frame, text=f"Duplicate Code successfully refactored in same directory as original.\nNOTE: code may not be semantically correct. Please double check results.", relief="raised", justify="center")
load_btn = ttk.Button(frame, text="Load .py File", command=lambda: load_file())
quit_btn = ttk.Button(frame, text="Quit", command=root.destroy)
codesmell_btn = ttk.Button(frame, text="Find Code Smells", command=lambda: find_codesmells())
refactor_btn = ttk.Button(frame, text="Refactor Duplicate Code", command=lambda: refactor_duplicate_code())

# pre : - status_label is declared before function definition
# post: - file is loaded or error is declared to client
def load_file():
    global loaded_path, original_contents
    reset_smell_results()
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
    codesmell_btn.grid(column=0, row=3, columnspan=2, pady=(5, 0))

# pre : - LOC_label, params_label, duplicates_label, and refactor_btn are declared before function definition
# post: - Code smells are displayed to client
def find_codesmells():
    global original_contents, duplicate_code
    long_methods, long_parameters = find_LOC_and_params(original_contents)
    duplicate_code = find_duplicates(original_contents)
    if long_methods: 
        LOC_label.config(text="Long Method/Function(s) detected: " + ", ".join(long_methods))
    if long_parameters:
        params_label.config(text="Long Parameter List(s) detected: " + ", ".join(long_parameters))
    if duplicate_code:
        pairs = [f"{m1} & {m2}" for (m1, m2) in duplicate_code.keys()]
        duplicates_label.config(text="Duplicate Code detected: " + "; ". join(pairs))
        refactor_btn.grid(column=0, row=7, columnspan=2)
    activate_codesmell_labels()

# pre : - LOC_label, params_label, and duplicates_label are declared before function definition
# post: - Labels are shown to client
def activate_codesmell_labels():
    LOC_label.grid(column=0, row=4, columnspan=2)
    params_label.grid(column=0, row=5, columnspan=2)
    duplicates_label.grid(column=0, row=6, columnspan=2)

# pre : - LOC_label, params_label, and duplicates_label are declared before function definition
# post: - Labels are hidden from client and are reset to default values
def reset_smell_results():
    LOC_label.config(text="Long Method/Function not detected.")
    params_label.config(text="Long Parameter List not detected.")
    duplicates_label.config(text="Duplicate Code not detected.")
    LOC_label.grid_forget()
    params_label.grid_forget()
    duplicates_label.grid_forget()

# pre : - refactor_label is declared before function definition
# post: - Code is refactored and placed in same directory as the input file
def refactor_duplicate_code():
    global loaded_path, new_contents
    try:
        new_contents = refactor_duplicates(duplicate_code, original_contents)
        produce_refactored(loaded_path, new_contents)
        refactor_label.grid(column=0, row=8, columnspan=2, pady=(5, 0))
    except:
        refactor_label.config(text="Error: Code was unable to be refactored. Try again please.")
        refactor_label.grid(column=0, row=8, columnspan=2, pady=(5, 0))

title_label.grid(column=0, row=0, columnspan=2, pady=(0,10))
load_btn.grid(column=0, row=1, sticky="w", padx=(0,5))
quit_btn.grid(column=1, row=1, sticky="e", padx=(5,0))
status_label.grid(column=0, row=2, columnspan=2, sticky="we", pady=(10,0))

frame.columnconfigure(0, weight=1)
frame.columnconfigure(1, weight=1)
root.mainloop()