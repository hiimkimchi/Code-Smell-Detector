import re

MAX_LOC = 15

# pre : - only called in check_LOC_and_params
# post: - returns name of function (or returns none)
def check_LOC (line, start_index, index):
    function_name_pattern = re.compile(r'^\s*def\s+([A-Za-z_]\w*)\s*\(')
    function_name = function_name_pattern.match(line)
    LOC = index - start_index
    if LOC > MAX_LOC:
        return function_name
    return None

# pre : - only called in check_LOC_and_params
# post: - returns name of function (or returns none)
def check_parameters (line):
    print()

# pre : - only called in read_lines
# post: - returns result of check_LOC and result of check_parameters
def check_LOC_and_params (contents, start_index, index):
    return check_LOC(contents[start_index], start_index, index), check_parameters(contents[index])

# pre : - contents are correctly read in FileLogic.py
# post: - returns list of methods that are too long and methods that have too many parameters
def read_lines (contents):
    current_start_index, long_methods, long_parameters = None, [], []
    for index in range(len(contents)):
        if not contents[index].startswith("def ") or index < len(contents):
            continue
        if not current_start_index:
            current_start_index = index
        long_method, long_param_list = check_LOC_and_params(contents, current_start_index, index)
        if long_method:
            long_methods.append(long_method)
        if long_param_list:
            long_parameters.append(long_param_list)
        current_start_index = index
    return long_methods, long_parameters


# duplicated code (use Jaccard Similarity for each method, compare two at a time)
# refactor dup (whichever method is called more, replace lesser used ones with the more used ones, send to FileLogic)

