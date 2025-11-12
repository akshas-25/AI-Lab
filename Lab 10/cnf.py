from sympy import symbols
from sympy.logic.boolalg import to_cnf

P, Q, R = symbols('P Q R')
expr = P >> (Q | ~R)
cnf_expr = to_cnf(expr, simplify=True)

print("Original Expression:", expr)
print("CNF Form:", cnf_expr)
