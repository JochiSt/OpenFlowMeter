# -*- coding: utf-8 -*-
"""

calculations based on:
http://earmark.net/gesr/opamp/case2b.htm

"""


from sympy import Symbol, pprint

# Vref = 3.3
Vin = Symbol("Vin")
Vref = Symbol("Vref")
Rf = Symbol("Rf")
Rg = Symbol("Rg")

R1 = Symbol("R1")
R2 = Symbol("R2")


R1pR2 = 1/(1/R1 + 1/R2)
m = (Rf + Rg + R1pR2) / ( Rg + R1pR2 )
b = Vref * ( R2/(R1+R2) ) * ( Rf / ( Rg + R1pR2 ))

Vout = m * Vin - b

pprint(Vout)