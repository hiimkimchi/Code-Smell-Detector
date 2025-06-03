import re

MAX_LOC = 15
MAX_PARAMS = 3
JACCARD_THRESHOLD = 0.75

# pre : - index < len(contents)
# post: - returns True if line is start of a method, False if line is not a start of a method
def is_method (contents, index):
    line = contents[index].lstrip()
    return line.startswith("def ")

# pre : - line is a method definition header (e.g. def ...)
# post: - returns the method name within the line
def get_method_name(line):
    line = line.lstrip()
    if line.startswith("if __name__ == \"__main__\""):
        return "MAIN"
    method_name_pattern = re.match(r'^\s*def\s+([A-Za-z_]\w*)\s*\(', line)
    return method_name_pattern.group(1) if method_name_pattern else None

# pre : - start_index < index
#       - line is a function definition start and is non empty 
# post: - returns name of function (or returns none)
def check_LOC (line, start_index, index, blank_line_count):
    function_name = get_method_name(line)
    LOC = index - start_index - blank_line_count
    if LOC > MAX_LOC:
        return function_name
    return None

# pre : - line is a function definition start and is non empty 
# post: - returns name of function (or returns none)
def check_parameters (line):
    name = get_method_name(line)
    param_pattern = re.compile(r'(?:\s*)(\[[^\]]*\]|\([^\)]*\)|[^,\[\]\(\)]+)(?=\s*,|\s*$)', re.VERBOSE)
    param_str = line[line.find("(")+1 : line.rfind(")")]
    params = [p.strip() for p in param_pattern.findall(param_str)]
    if len(params) > MAX_PARAMS:
        return name
    return None

# pre : - start_index < index
#       - line is a function definition start and is non empty 
# post: - returns result of check_LOC and result of check_parameters
def check_LOC_and_params (contents, start_index, index, blank_line_count):
    last_index = index
    if index == len(contents):
        last_index = start_index
    return check_LOC(contents[start_index], start_index, index, blank_line_count), check_parameters(contents[last_index])

# pre : -finds index boundaries for each method as well as the amount of blank_lines within
# post: - returns a list of tuples (start index, index, blank lines)
def collect_boundaries (contents):
    boundaries, current_start_index, blank_count = [], None, 0
    for index in range(len(contents)):
        if not is_method(contents, index):
            if current_start_index is not None and contents[index] == '\n':
                blank_count += 1
            continue
        if current_start_index is None:
            current_start_index, blank_count = index, 0
        else:
            boundaries.append((current_start_index, index, blank_count))
            current_start_index, blank_count = index, 0
    if current_start_index is not None:
        boundaries.append((current_start_index, len(contents), blank_count))
    return boundaries

# pre : - collect_boundaries collects index boundaries and blank_lines within correctly
# post: - returns list of methods that are too long and methods that have too many parameters
def find_LOC_and_params (contents):
    long_methods, long_parameters = [], []
    boundaries = collect_boundaries(contents)
    for start_index, index, blank_count in boundaries:
        long_method, long_parameter = check_LOC_and_params(contents, start_index, index, blank_count)
        if long_method:
            long_methods.append(long_method)
        if long_parameter:
            long_parameters.append(long_parameter)
    return long_methods, long_parameters

# pre : - method_name is properly retrieved by get_method_name
# post: - returns True if the name is found, False if not
def name_in_line (method_name, line):
    name_pattern = re.compile(rf'\b{re.escape(method_name)}\s*\([^)]*\)')
    return bool(name_pattern.search(line))
    
# pre : - len of method1 and 2 are not 0
# post: - returns a jaccard similarity score (float theoretically in between 0.0 and 1.0)
def jaccard_sim (method1, method2):
    text1 = "".join(method1)
    text2 = "".join(method2)
    set1 = set(text1)
    set2 = set(text2)
    intersection = set1 & set2
    union = set1 | set2
    return len(intersection) / len(union) if union else 1.0

# pre : - method_name is properly retrieved by get_method_name
# post: - returns number of calls of the method made in the code except the line where it is defined
def get_calls (method_name, contents):
    calls = 0
    for index in range(len(contents)):
        if not is_method(contents, index) and name_in_line(method_name, contents[index]):
            calls += 1
    return calls

# pre : - len of method1 and 2 are not 0
# post: - returns a pair formatted as such {(method1, method2) : {method1 : amount of calls, method2 : amount of calls}}
def check_duplicated (method1, method2, contents):
    if jaccard_sim(method1, method2) < JACCARD_THRESHOLD:
        return None
    method1_name, method2_name = get_method_name(method1[0]), get_method_name(method2[0])
    method1_count, method2_count = get_calls(method1_name, contents), get_calls(method2_name, contents)
    return {(method1_name, method2_name) : {method1_name : method1_count, method2_name : method2_count}}