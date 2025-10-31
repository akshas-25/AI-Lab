import re
from itertools import product

def convert_expression(expr):
    expr = expr.replace('~', ' not ')
    expr = expr.replace('^', ' and ')

    # Replace uppercase V only (with spaces around it)
    expr = re.sub(r'(?<=\s)v(?=\s)', ' or ', expr)
    expr = re.sub(r'(?<=\()v(?=\s)', ' or ', expr)
    expr = re.sub(r'(?<=\s)v(?=\))', ' or ', expr)

    # implication as before ...
    while '->' in expr:
        start = expr.find('->')
        left = ''
        i = start - 1
        while i >= 0 and (expr[i].isalnum() or expr[i] in [' ', 'n', 'o', 't']):
            left = expr[i] + left
            i -= 1
        left = left.strip()
        right = ''
        j = start + 2
        while j < len(expr) and (expr[j].isalnum() or expr[j] in [' ', 'n', 'o', 't']):
            right += expr[j]
            j += 1
        right = right.strip()
        replacement = f'((not {left}) or {right})'
        expr = expr[:i+1] + replacement + expr[j:]

    return expr


def extract_symbols(expressions):
    symbols = set()
    for expr in expressions:
        for ch in expr:
            if ch.isalpha() and ch not in ['v']:  # exclude operator v here
                symbols.add(ch)
    return sorted(symbols)

def evaluate_expression(expr, model):
    for var, val in model.items():
        expr = expr.replace(var, str(val))
    expr = convert_expression(expr)
    try:
        return eval(expr)
    except Exception as e:
        return False

def PL_TRUE(sentence, model):
    return evaluate_expression(sentence, model)

def tt_check_all(KB, alpha, symbols, model):
    if not symbols:
        if all(PL_TRUE(s, model) for s in KB):
            return PL_TRUE(alpha, model)
        else:
            return True
    else:
        rest = symbols[1:]
        sym = symbols[0]
        model_true = model.copy()
        model_true[sym] = True
        model_false = model.copy()
        model_false[sym] = False
        return tt_check_all(KB, alpha, rest, model_true) and tt_check_all(KB, alpha, rest, model_false)

def tt_entails(KB, alpha):
    symbols = extract_symbols(KB + [alpha])
    return tt_check_all(KB, alpha, symbols, {})

def print_truth_table(KB, queries):
    symbols = extract_symbols(KB + queries)
    headers = symbols + ['KB: ' + s for s in KB] + ['Query: ' + q for q in queries]

    col_width = 12  # width for each column

    # Print header with fixed width, centered
    header_row = ' | '.join(h.center(col_width) for h in headers)
    print(header_row)
    print('-' * len(header_row))

    for values in product([True, False], repeat=len(symbols)):
        model = dict(zip(symbols, values))
        kb_vals = [PL_TRUE(s, model) for s in KB]
        query_vals = [PL_TRUE(q, model) for q in queries]

        row = []
        for s in symbols:
            row.append('T'.center(col_width) if model[s] else 'F'.center(col_width))
        for val in kb_vals:
            row.append('T'.center(col_width) if val else 'F'.center(col_width))
        for val in query_vals:
            row.append('T'.center(col_width) if val else 'F'.center(col_width))

        print(' | '.join(row))
        print(' | '.join(row))

def main():
    print("Enter knowledge base sentences one per line using ^ (AND), v (OR), ~ (NOT), -> (IMPLIES). Enter blank line to finish:")
    KB = []
    while True:
        line = input()
        if not line.strip():
            break
        KB.append(line.strip())

    print("Enter query sentences one per line (same format). Enter blank line to finish:")
    queries = []
    while True:
        line = input()
        if not line.strip():
            break
        queries.append(line.strip())

    print("\nTruth Table:")
    print_truth_table(KB, queries)

    for q in queries:
        entails = tt_entails(KB, q)
        print(f"\nDoes the knowledge base entail the query '{q}'? {'Yes' if entails else 'No'}")

if __name__ == "__main__":
    main()