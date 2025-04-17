# CREATES CHRISTOFFEL SYMBOLS

import sympy as sm
from einsteinpy.symbolic import MetricTensor, ChristoffelSymbols

# Define 4D spacetime
dimensions = sm.symbols("t r theta phi")
G, M, c, a = sm.symbols("G M c a") # a is the Schwarzchild radius

# Define Schwarzchild metric tensor
list2d = [[0 for i in range(4)] for i in range(4)]
list2d[0][0] = 1 - (a / dimensions[1])
list2d[1][1] = -1 / ((1 - (a / dimensions[1])) * (c ** 2))
list2d[2][2] = -1 * (dimensions[1] ** 2) / (c ** 2)
list2d[3][3] = -1 * (dimensions[1] ** 2) * (sm.sin(dimensions[2]) ** 2) / (c ** 2)
sch_metric_tensor = MetricTensor(list2d, dimensions)
sch_metric_tensor.tensor()

# Create simplified Christoffel symbols
sch_christoffel_symbols = ChristoffelSymbols.from_metric(sch_metric_tensor).simplify()
print(sch_christoffel_symbols)