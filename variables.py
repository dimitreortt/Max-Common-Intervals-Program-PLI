from gurobipy import GRB
from utils import getFamily
from rules import applyRules, isAcceptedInAllRules
from nextVarTuple import nextVarTuple

# same functionality from class gurobipy.tupledict()
class MyX():
  def __init__(self, g1, g2):
    self.g1 = g1
    self.g2 = g2
    pass

  def select(self, lst1='*', lst2='*'):
    if lst1 == '*':
      lst1 = self.g1

    elif type(lst1) == type(1):
      lst1 = [lst1]

    if lst2 == '*':
      lst2 = self.g2

    elif type(lst2) == type(1):
      lst2 = [lst2]

    selected = []
    for i in lst1:
      for j in lst2:
        if self.g1[i] == self.g2[j]:
          selected.append((i, j))
    
    return selected

  def sum(self, lst1, lst2):
    return len(self.select(lst1, lst2))

def calculateL(g1, g2):
  fmly1 = getFamily(g1)
  fmly2 = getFamily(g2)

  L = 0
  for f in fmly1:
    if f in fmly2:
      L += min(len(fmly1[f]), len(fmly2[f]))

  return L

def createCVariablesAndApplyRulesSecondFormat(model, g1, g2):
  myX = MyX(g1, g2)
  tupleList = []
  varTuple = nextVarTuple(g1, g2)
  while varTuple:
    if isAcceptedInAllRules(varTuple, myX, g1, g2):
      tupleList.append(varTuple)
    
    varTuple = nextVarTuple(g1, g2)

  L = calculateL(g1, g2)
  C = model.addVars(tupleList, vtype = GRB.BINARY, name='c')

  return C, L

# Create Variables Cijkl already applying [Rule 1], [Rule 2], [Rule 3]
def createCVariablesAndApplyRules(model, g1, g2):
  # Create tupleList already applying [Rule 1]
  tupleList = [(i,j,k,l) for i in range(len(g1)) for j in range(i, len(g1)) for k in range(len(g2)) for l in range(k,len(g2)) if i != j and k != l]

  L = calculateL(g1, g2)

  myX = MyX(g1, g2)
  applyRules(tupleList, myX, g1, g2)

  C = model.addVars(tupleList, vtype = GRB.BINARY, name='c')
  return C, L

def createXVariables(model, g1, g2):
  # Create Variables Xik
  varList = [(i,k) for i in range(len(g1)) for k in range(len(g2)) if g1[i] == g2[k]]
  X = model.addVars(varList, vtype = GRB.BINARY, name='x')
  return X
