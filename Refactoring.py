import re
from itertools import combinations
from Processing import check_duplicated, is_method

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
#       - assumes there is duplicated code
# post: - returns new version of contents where all duplicates are replaced with their higher frequency counterparts
#       - NOTE: this is not semantically accurate in some examples. warn client about it through GUI
def refactor_duplicates (pairs, contents):
    replace_map = winner_loser_replacement_map(pairs)
    loser_map = create_loser_map(replace_map)
    return rewrite_contents (replace_map, contents, loser_map)

# pre : - pairs is a hashmap formatted as such {(method1, method2) : {method1 : amount of calls, method2 : amount of calls}}
# post: - returns hashmap as such {winner : loser}, where loser is the method to be replaced by winner
def winner_loser_replacement_map (pairs):
    replace_map = {}
    for (method1, method2), counts in pairs.items():
        count1, count2 = counts[method1], counts[method2]
        if count1 >= count2:
            winner, loser = method1, method2
        else:
            winner, loser = method2, method1
        replace_map[loser] = winner
    return replace_map

# pre : - replace_map is non-empty
# post: - returns hashmap as such {loser : pattern} where pattern is the regex corresponding to calling loser
def create_loser_map (replace_map):
    call_patterns = {}
    for loser in replace_map:
        pattern = re.compile(rf'\b{re.escape(loser)}\s*\(')             
        call_patterns[loser] = pattern
    return call_patterns

# pre : - all parameters are non empty
# post: - new_line is either not changed or if the line contains loser method calls, replace with winner counterpart
def rewrite_line (replace_map, line, loser_map):
    new_line = line
    for loser, winner in replace_map.items():
        new_line = loser_map[loser].sub(f"{winner}(", new_line)
    return new_line

# pre : - stripped successfully is a line stripped of indentation
#       - replace_map is non-empty
# post: - returns True if line is definition of loser function, False if not
def detect_loser_def (stripped, replace_map):
    if stripped.startswith("def "):
        match = re.match(r'def\s+([A-Za-z_]\w*)\s*\(', stripped)
        if match and match.group(1) in replace_map: 
            return True
    return False

# pre : - replace_map is non-empty
#       - loser_map is non-empty
# post: - returns a modified version of contents, with all duplicates removed
def rewrite_contents(replace_map, contents, loser_map):
    new_contents, skipping, skip_indent = [], False, 0
    for line in contents:
        stripped = line.lstrip()
        indent = len(line) - len(stripped)
        if skipping:
            if indent > skip_indent: continue
            skipping = False
        if detect_loser_def(stripped, replace_map):
                skipping, skip_indent = True, indent
                continue
        new_contents.append(rewrite_line(replace_map, line, loser_map))
    return new_contents