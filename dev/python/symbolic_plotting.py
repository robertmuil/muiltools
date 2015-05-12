from sympy import symbols
from sympy.plotting import plot

x = symbols('x')

p1 = plot(x*x, x**3, 2**x, (x, 0, 20))

