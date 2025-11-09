# Logic Circuit Simulator with Boolean Algebra & Simplification
"""
Windows-Compatible Version (Corrected for 'not' operator)
File: logiccir.py

How to Run in VS Code or PowerShell:

▶ To run built-in examples:
    python logiccir.py --example

▶ To run with your own expression (e.g., A.B + !A.C):
    python logiccir.py "A.B + !A.C" --kmap
"""

import itertools
import argparse
import re
from typing import List, Dict, Set

# ---------------------------
# Boolean Expression Parser
# ---------------------------

def parse_expression(expr: str):
    expr = expr.replace(" ", "")
    expr = expr.replace(".", "&").replace("+", "|")
    # Wrap 'not' operands with parentheses for correct Python syntax
    expr = re.sub(r'!([A-Za-z0-9_]+)', r'(not \1)', expr)
    return expr


def evaluate_expression(expr: str, variables: Dict[str, int]) -> int:
    local_vars = {var: bool(val) for var, val in variables.items()}
    return int(eval(expr, {}, local_vars))

# ---------------------------
# Generate Truth Table
# ---------------------------
def truth_table(expr: str) -> List[Dict[str, int]]:
    vars_sorted = sorted(set(ch for ch in expr if ch.isalpha()))
    parsed_expr = parse_expression(expr)
    table = []
    for combo in itertools.product([0, 1], repeat=len(vars_sorted)):
        assignment = dict(zip(vars_sorted, combo))
        result = evaluate_expression(parsed_expr, assignment)
        assignment['F'] = result
        table.append(assignment)
    return table


def print_truth_table(table: List[Dict[str, int]]):
    headers = list(table[0].keys())
    print(" | ".join(headers))
    print("-" * (4 * len(headers)))
    for row in table:
        print(" | ".join(str(v) for v in row.values()))

# ---------------------------
# Quine–McCluskey Simplification
# ---------------------------

def qm_simplify(minterms: Set[int], num_vars: int) -> Set[str]:
    def combine(a, b):
        diff = 0
        res = []
        for x, y in zip(a, b):
            if x != y:
                diff += 1
                res.append('-')
            else:
                res.append(x)
        return ''.join(res) if diff == 1 else None

    terms = {format(m, f'0{num_vars}b') for m in minterms}
    unchecked = terms.copy()
    new_terms = set()

    for a in terms:
        for b in terms:
            combined = combine(a, b)
            if combined:
                new_terms.add(combined)
                unchecked.discard(a)
                unchecked.discard(b)

    if not new_terms:
        return unchecked
    return qm_simplify({int(t.replace('-', '0'), 2) for t in new_terms}, num_vars) | unchecked


def bits_to_expr(bits: str, vars_sorted: List[str]) -> str:
    terms = []
    for b, v in zip(bits, vars_sorted):
        if b == '1':
            terms.append(v)
        elif b == '0':
            terms.append(f'!{v}')
    return '.'.join(terms) if terms else '1'

# ---------------------------
# Karnaugh Map (basic)
# ---------------------------
def kmap_display(table: List[Dict[str, int]]):
    print("\nKarnaugh Map (for visualization):")
    for row in table:
        print(row)

# ---------------------------
# Main CLI Function
# ---------------------------
def main():
    parser = argparse.ArgumentParser(description="Logic Circuit Simulator with simplification (QM + small K-map)")
    parser.add_argument('expr', nargs='?', help='Boolean expression (use + for OR, . or whitespace for AND, ! for NOT). Quote it')
    parser.add_argument('--dontcare', '-d', help='Comma-separated list of dont-care minterms (e.g. 1,3)')
    parser.add_argument('--kmap', action='store_true', help='Show Karnaugh map (if <=4 vars)')
    parser.add_argument('--example', action='store_true', help='Run examples')
    args = parser.parse_args()

    if args.example:
        print("\nExample: Expression = A.B + !A.C\n")
        expr = "A.B + !A.C"
    elif args.expr:
        expr = args.expr
    else:
        parser.print_help()
        return

    print(f"\nEvaluating Expression: {expr}\n")
    table = truth_table(expr)
    print_truth_table(table)

    minterms = {i for i, row in enumerate(table) if row['F'] == 1}
    vars_sorted = sorted(set(ch for ch in expr if ch.isalpha()))

    simplified = qm_simplify(minterms, len(vars_sorted))
    simplified_expr = ' + '.join(bits_to_expr(s, vars_sorted) for s in simplified)

    print("\nSimplified Expression (approx):", simplified_expr)

    if args.kmap and len(vars_sorted) <= 4:
        kmap_display(table)


if __name__ == "_main_":
    main()