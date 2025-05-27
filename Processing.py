import re

MAX_LOC = 15



# long method (check for lines of code (no more than 15) from every "def", use regex)

# pre :
# post:
def check_LOC (contents):
    current_start_index = 0
    long_methods = []
    function_name_pattern = re.compile(r'^\s*def\s+([A-Za-z_]\w*)\s*\(')
    for index in range(len(contents)):
        if not contents[index].startswith("def "):
            continue
        function_name = function_name_pattern.match(contents[index])
        LOC = index - current_start_index
        if LOC > MAX_LOC:
            long_methods.append(function_name)
    return long_methods

# long parameter list (check line of def, use regex to see parameters within commas after the ( and before the ))
# duplicated code (use Jaccard Similarity for each method, compare two at a time)
# refactor dup (whichever method is called more, replace lesser used ones with the more used ones, send to FileLogic)

