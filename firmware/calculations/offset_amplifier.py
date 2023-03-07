# -*- coding: utf-8 -*-
"""

"""
from sympy import Symbol, symbols, solve, pprint, Eq

Up, Un = symbols("U_+, U_-")


Uout  = Symbol("U_out")
Ubias = Symbol("U_bias")

R1, R2 = symbols("R_1, R_2")

I_R1R2 = (Uout - Ubias) / (R1 + R2)

Un = I_R1R2 * R2 + Ubias

eq1 = Eq( Up , Un )
pprint(eq1)

Uin = symbols("U_in")
eq1 = eq1.subs(Up, Uin)
pprint(eq1)

sol = solve(eq1, Uout)[0].factor()
pprint(sol)
