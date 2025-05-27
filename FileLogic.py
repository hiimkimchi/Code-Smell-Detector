import os

# pre : - filepath must be in the Desktop folder on MacOS
# post: - returns contents of file 
def get_file(filename):
    full_path = "~/Desktop/" + filename
    if not filename.endswith(".py") or not os.path.exists():
        return []
    with open(full_path, "r") as infile:
        all_lines = infile.readlines()
    return all_lines

# pre : - assumed to only be called when content is assumed to be correctly refactored in Processing
# post: - content written in filename_refactored.py
def produce_refactored(filename, content):
    produced = os.path.splitext(filename)[0] + "_refactored.py"
    full_path = "~/Desktop/" + produced
    with open(full_path, "w") as outfile:
        outfile.writelines(content)