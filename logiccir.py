"""
Logic Circuit Simulator with Boolean Algebra
- Evaluate Boolean expressions
- Generate truth table
- Automatically simplifies expression using SymPy
- Auto-runs example if no expression is provided
"""

import itertools
import argparse
import sys

# ---------------------------
# Boolean Expression Evaluation
# ---------------------------
def eval_expr(expr, values):
    """Evaluate a Boolean expression given variable values"""
    expr_eval = expr
    for var, val in values.items():
        expr_eval = expr_eval.replace(var, str(val))
    return int(eval(expr_eval))

# ---------------------------
# Generate Truth Table
# ---------------------------
def truth_table(expr, variables):
    table = []
    for combination in itertools.product([0,1], repeat=len(variables)):
        values = dict(zip(variables, combination))
        result = eval_expr(expr, values)
        table.append((combination, result))
    return table

# ---------------------------
# Simplify Expression
# ---------------------------
def simplify_expr(expr, variables):
    try:
        import sympy
        from sympy.logic.boolalg import simplify_logic
        # Define symbols
        syms = {v: sympy.Symbol(v) for v in variables}
        # Convert string to sympy expression
        sym_expr = sympy.sympify(expr, locals=syms)
        simplified = simplify_logic(sym_expr, form='dnf')
        return str(simplified)
    except ImportError:
        return expr  # fallback if sympy not installed

# ---------------------------
# Argument Parser
# ---------------------------
def get_args():
    parser = argparse.ArgumentParser(description="Logic Circuit Simulator")
    parser.add_argument("expr", nargs='?', default=None,
                        help="Boolean expression (use & for AND, | for OR, ~ for NOT)")
    parser.add_argument("--example", action="store_true", help="Run example circuits")
    args, unknown = parser.parse_known_args()  # Ignore unknown args (useful for Jupyter)
    return args

# ---------------------------
# Main
# ---------------------------
def main():
    args = get_args()

    # Auto-run example if no expression is provided
    if args.example or not args.expr:
        expr = "A & B | ~A & C"
        variables = ["A", "B", "C"]
        print("Running built-in example circuit!")
    else:
        expr = args.expr
        # Auto-detect variables
        variables = sorted(set(filter(str.isalpha, expr)))
        print(f"Expression: {expr}")

    # Truth table
    table = truth_table(expr, variables)
    print("\nTruth Table:")
    print(" | ".join(variables) + " | OUT")
    print("-"*(4*len(variables)+6))
    for row, out in table:
        print(" | ".join(map(str,row)) + " | " + str(out))

    # Always simplify expression
    simplified = simplify_expr(expr, variables)
    print(f"\nSimplified Expression: {simplified}")

# ---------------------------
# Run
# ---------------------------
if __name__ == "__main__":
    main()
