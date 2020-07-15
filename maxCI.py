import sys
from utils import getGenomes
from variables import createCVariablesAndApplyRules, createXVariables
from constraints import createConstraints
from output import writeOutput

# import gurobi
import gurobipy as gp
from gurobipy import GRB

# Read input
g1, g2 = getGenomes(sys.argv)

# Create model
model = gp.Model('maxCI')

# Create variables (already apply rules to speed up the program)
C, L = createCVariablesAndApplyRules(model, g1, g2)
X = createXVariables(model, g1, g2)

# Set objective
model.setObjective(C.sum(), GRB.MAXIMIZE)

# Create constraints
createConstraints(model, C, X, g1, g2)

# Optimize
model.optimize()

# Write output
writeOutput(model, L)