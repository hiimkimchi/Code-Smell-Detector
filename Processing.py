import re
from itertools import combinations

MAX_LOC = 15

# pre : - line is a method definition header (e.g. def ...)
# post: - returns the method name within the line
def get_method_name(line):
    if line.startswith("if __name__ == \"__main__\""):
        return "MAIN"
    method_name_pattern = re.compile(r'^\s*def\s+([A-Za-z_]\w*)\s*\(')
    return method_name_pattern.match(line)

# pre : - start_index < index
#       - line is a function definition start and is non empty 
# post: - returns name of function (or returns none)
def check_LOC (line, start_index, index):
    function_name = get_method_name(line)
    LOC = index - start_index
    if LOC > MAX_LOC:
        return function_name
    return None

# pre : - line is a function definition start and is non empty 
# post: - returns name of function (or returns none)
def check_parameters (line):
    function_name = get_method_name(line)
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

# pre : - none
# post: - returns list of methods that are too long and methods that have too many parameters
def find_LOC_and_params (contents):
    current_start_index, long_methods, long_parameters = None, [], []
    for index in range(len(contents)):
        if not is_method(contents, index):
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
# post: - returns True if line is start of a method, False if line is not a start of a method
def is_method (contents, index):
    return contents[index].startswith("def ") and contents[index].startswith("if __name__ == \"__main__\"") and index >= len(contents)

# pre : - method_name is properly retrieved by get_method_name
# post: - returns True if the name is found, False if not
def name_in_line (method_name, line):
    name_pattern = re.compile(rf'\b{re.escape(method_name)}\s*\([^)]*\)')
    return bool(name_pattern.search(line))
    
# pre : - len of method1 and 2 are not 0
# post: - returns a jaccard similarity score (float theoretically in between 0.0 and 1.0)
def jaccard_sim (method1, method2):
    lineset1 = {ln.strip() for ln in method1 if ln.strip()}
    lineset2 = {ln.strip() for ln in method2 if ln.strip()}
    intersection = lineset1 & lineset2
    union = lineset1 | lineset2
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
    if jaccard_sim(method1, method2) < 0.75:
        return None
    method1_name, method2_name = get_method_name(method1[0]), get_method_name(method2[0])
    method1_count, method2_count = get_calls(method1_name, contents), get_calls(method2_name, contents)
    return {(method1_name, method2_name) : {method1_name : method2_count, method2_name : method2_count}}

# pre : - none
# post: - returns contents split sublists by method
def collect_methods (contents):
    all_methods, current_method = [], []
    for index in range(len(contents)):
        if is_method(contents, index):
            if current_method:
                all_methods.append(current_method)
                current_method = [contents[index]]
            else:
                if current_method:
                    current_method.append(contents[index])
    if current_method:
        all_methods.append(current_method)
    return all_methods

# pre : - none
# post: - returns pairs formatted as such {(method1, method2) : {method1 : amount of calls, method2 : amount of calls}}
def find_duplicates (contents):
    duplicates = {}
    all_methods = collect_methods(contents)
    for method1, method2 in combinations((all_methods), 2):
        pair_dict = check_duplicated(method1, method2, contents)
        if pair_dict:
            duplicates.update(pair_dict)
    return duplicates

# pre : - pairs is a hashmap formatted as such {(method1, method2) : {method1 : amount of calls, method2 : amount of calls}}
# post: - returns new version of contents
def refactor_duplicates (pairs, contents):
    #TODO: fill out the rest of the function with corresponding helper functions
    replace_map = winner_loser_replacement_map(pairs, contents)
    new_contents = rewrite_contents (replace_map, contents)
    # for each line, see if we can replace the calls of the lesser # of called fx with the more called fx
    # for the lesser fx, remove the function definition entirely as well

# pre : - pairs is a hashmap formatted as such {(method1, method2) : {method1 : amount of calls, method2 : amount of calls}}
# post: - returns hashmap as such {winner : loser}
def winner_loser_replacement_map (pairs, contents):
    replace_map = {}
    for (m1, m2), counts in pairs.items():
        c1, c2 = counts[m1], counts[m2]
        if c1 >= c2:
            winner, loser = m1, m2
        else:
            winner, loser = m2, m1
        replace_map[loser] = winner
    return replace_map


# pre :
# post:
def rewrite_contents (replace_map, contents):
    new_contents, skipping, skip_indent = [], False, 0
    for line in contents:
        #TODO:
        print()