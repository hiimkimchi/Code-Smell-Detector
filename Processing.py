import re

MAX_LOC = 15

def get_function_name(line):
    function_name_pattern = re.compile(r'^\s*def\s+([A-Za-z_]\w*)\s*\(')
    return function_name_pattern.match(line)

# pre : - start_index < index
#       - line is a function definition start and is non empty 
# post: - returns name of function (or returns none)
def check_LOC (line, start_index, index):
    function_name = get_function_name(line)
    LOC = index - start_index
    if LOC > MAX_LOC:
        return function_name
    return None

# pre : - line is a function definition start and is non empty 
# post: - returns name of function (or returns none)
def check_parameters (line):
    function_name = get_function_name(line)
    param_pattern = (r'?:\s*)(\[[^\]]*\]|\([^\)]*\)|[^,\[\]\(\)]+)(?=\s*,|\s*$)', re.VERBOSE)
    params = [p.strip() for p in param_pattern.findall(line)]
    if len(params) >= 3:
        return function_name
    return None


# pre : - start_index < index
#       - line is a function definition start and is non empty 
# post: - returns result of check_LOC and result of check_parameters
def check_LOC_and_params (contents, start_index, index):
    return check_LOC(contents[start_index], start_index, index), check_parameters(contents[index])

# pre : - contents are correctly read in FileLogic.py
# post: - returns list of methods that are too long and methods that have too many parameters
def read_lines (contents):
    current_start_index, long_methods, long_parameters = None, [], []
    for index in range(len(contents)):
        if is_not_method(contents, index):
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

# pre : - index < len(contents)
# post: - returns True if line is not start of a method, False if line is a start of a method
def is_not_method (contents, index):
    return not contents[index].startswith("def ") or not contents[index].startswith("if __name__ == \"__main__\"") or index < len(contents)

def jaccard_sim (method1, method2):
    lineset1 = {ln.strip() for ln in method1 if ln.strip()}
    lineset2 = {ln.strip() for ln in method2 if ln.strip()}
    intersection = lineset1 & lineset2
    union = lineset1 | lineset2
    return len(intersection)/len(union) if union else 1.0

def get_calls (function_name, contents):
    print()
    #TODO: gets number of calls of the function name EXCEPT the line where it is defined

def check_duplicated (method1, method2, contents):
    if jaccard_sim(method1, method2) < 0.75:
        return None
    method1_name = get_function_name(method1[0])
    method2_name = get_function_name(method2[0])
    method1_count, method2_count = get_calls(method1_name, contents), get_calls(method2_name, contents)
    return { {method1_name : method1_count} : {method2_name : method2_count} }

def read_pairs (contents):
    #TODO: matches pairs and checks if duplicated and adds to a hashmap if so
    print()

def refactor_duplicates (pairs, contents):
    #TODO:
    print()
    # refactor dup (whichever method is called more, replace lesser used ones with the more used ones, send to FileLogic)