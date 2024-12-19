from sys import argv
from re import findall

def evaluate_expr(expr: str) -> float:
    """Evaluates an expression without brackets and returns it's value."""

    while expr.count("^") > 0:
        pos = expr.index("^")
        operands = [expr[pos-1],expr[pos+1]]

        if operands[0] in var_vals:
            operands[0] = var_vals[operands[0]]
        if operands[1] in var_vals:
            operands[1] = var_vals[operands[1]]

        result = float(operands[0]) ** float(operands[1])
        expr[pos-1] = result
        del expr[pos:pos+2]

    for op in ["*/","+-"]:
        # print(expr.count(op[0]), expr.count(op[1]))
        while expr.count(op[0]) > 0 or expr.count(op[1]) > 0:
            for pos, elem in enumerate(expr):
                if elem == op[0] or elem == op[1]:
                    index = pos
                    operands = [expr[pos-1],expr[pos+1]]

                    if operands[0] in var_vals:
                        operands[0] = var_vals[operands[0]]
                    if operands[1] in var_vals:
                        operands[1] = var_vals[operands[1]]

                    if elem == "*":
                        result = float(operands[0]) * float(operands[1])
                        break
                    elif elem == "/":
                        result = float(operands[0]) / float(operands[1])
                        break
                    elif elem == "+":
                        result = float(operands[0]) + float(operands[1])
                        break
                    elif elem == "-":
                        result = float(operands[0]) - float(operands[1])
                        break

            expr[index-1] = result
            del expr[index:index+2]
            # print(f"{operands[0]} op {operands[1]} = {result}")

    return expr[0]

def evaluate_br(expr: str, brackets: list) -> float:
    """Evaluates each set of brackets in an expression and returns the final value."""
    brackets.append([-1,len(expr)])
    results = []
    for pos1, bracket1 in enumerate(brackets):
        for pos2, bracket2 in enumerate(brackets[:pos1]):
            expr[bracket2[0]:bracket2[1]+1] = [results[pos2]] + ["" for _ in range(len(expr[bracket2[0]:bracket2[1]+1])-1)]

        contents = expr[bracket1[0]+1:bracket1[1]]
        results.append(evaluate_expr([x for x in contents if x != ""]))
    return results[-1:][0]

## Open brig file from argument

path = argv[1]

# path = "test.br"

try:
    with open(path, "r") as file:
        if path[-3:] == ".br":
            lines = [line for line in file.read().splitlines() if line != ""]
        else:
            raise FileNotFoundError("File should have a \".br\" file extension.") from None
except FileNotFoundError:
    raise FileNotFoundError("File does not exist.") from None

var_vals = {}

for num, line in enumerate(lines):
    line = line.replace(" ","").split("=")
    variable, expr = line[0], line[1]

    expr = findall(r'[a-zA-Z0-9]+|[+\-*/\^()]', expr)
    # Find locations of all brackets
    unclosed_br = []
    closed_br = []
    for pos, char in enumerate(expr):
        if char == "(":
            unclosed_br.append([pos])
        elif char == ")":
            try:
                closed_br.append(unclosed_br.pop() + [pos])
            except IndexError:
                raise SyntaxError(f"Unopened \")\" on line {num+1}:\n{line}") from None
            
    if unclosed_br != []:
        print(f"Error: Unclosed \"(\" at line {num+1}.")
        raise SyntaxError(f"Unclosed \"(\" on line {num+1}:\n{line[1]}") from None
    
    # Evaluate the expression
    var_vals[variable] = evaluate_br(expr, closed_br)
    
print(var_vals)