from utils import getFamily

# [Rule 2.1]
def rule2_1(X, cijkl):
  i, j, k, l = cijkl
  inKL = list(range(k, l + 1))   
  matchesIKL = X.select(i, inKL)
  matchesJKL = X.select(j, inKL)
  
  if len(matchesIKL) == 0 or len(matchesJKL) == 0:
    return True

# [Rule 2.2]
def rule2_2(X, cijkl, g1):
  i, j, k, l = cijkl
  inKL = list(range(k, l + 1)) 
  matchesIKL = X.select(i, inKL)
 
  if len(matchesIKL) < 2 and g1[i] == g1[j]:
    True

# [Rule 2.3]
def rule2_3(X, cijkl):
  i, j, k, l = cijkl
  inIJ = list(range(i, j + 1))
  matchesKIJ = X.select(inIJ, k)
  matchesLIJ = X.select(inIJ, l)

  if len(matchesKIJ) == 0 or len(matchesLIJ) == 0:    
    return True

# [Rule 2.4]
def rule2_4(X, cijkl, g2):
  i, j, k, l = cijkl
  inIJ = list(range(i, j + 1))
  matchesKIJ = X.select(inIJ, k)

  if len(matchesKIJ) < 2 and g2[k] == g2[l]:
    return True    

def removeVariables(C, variablesToBeRemoved):
  for cijkl in variablesToBeRemoved:    
    C.remove(cijkl)

def showCUpdate(C, variablesToBeRemoved, rule=''):
  print('Removing %.2f percent of C in rule %s' \
    % (len(variablesToBeRemoved)/len(C), rule))
  print('len(C): %d -> %d\n' % (len(C), len(C) - len(variablesToBeRemoved)))


def applyRule2(C, X, g1, g2):
  variablesToBeRemoved = []
  for cijkl in C:    
    if rule2_1(X, cijkl):
      variablesToBeRemoved.append(cijkl)      

    elif rule2_2(X, cijkl, g1):
      variablesToBeRemoved.append(cijkl)
      
    elif rule2_3(X, cijkl):
      variablesToBeRemoved.append(cijkl)

    elif rule2_4(X, cijkl, g2):
      variablesToBeRemoved.append(cijkl)  

  showCUpdate(C, variablesToBeRemoved, '2')  
  removeVariables(C, variablesToBeRemoved)

def occ(gene, genome, i='', j=''):
  if i != '' and j != '':
    genome = genome[i: j + 1]

  return genome.count(gene)

def rule3Abs1(cijkl, gene, g1, g2):
  i, j, k, l = cijkl  
  return abs(occ(gene, g1, i, j) - occ(gene, g2, k, l))

def rule3Abs2(gene, g1, g2):
  return abs(occ(gene, g1) - occ(gene, g2))

def getSubAlphabet(cijkl, g1, g2):
  i, j, k, l = cijkl

  fmly1 = getFamily(g1[i: j + 1])
  fmly2 = getFamily(g2[k: l + 1])

  lst1 = list(fmly1.keys())
  lst2 = list(fmly2.keys())

  # union of lists
  subAlphabet = list(set().union(lst1, lst2))

  return subAlphabet

def removeDuplicates(variablesToBeRemoved):
  checked = []
  for cijkl in variablesToBeRemoved:
    if cijkl not in checked:
      checked.append(cijkl)

  return checked

def applyRule3(C, g1, g2):
  variablesToBeRemoved = []
  for cijkl in C:    
    subAlphabet = getSubAlphabet(cijkl, g1, g2)
    for g in subAlphabet:
      if rule3Abs1(cijkl, g, g1, g2) > rule3Abs2(g, g1, g2):
        variablesToBeRemoved.append(cijkl)

  variablesToBeRemoved = removeDuplicates(variablesToBeRemoved)  

  showCUpdate(C, variablesToBeRemoved, '3')
  removeVariables(C, variablesToBeRemoved)

def rule4_1(cijkl, genome1):
  i, j, k, l = cijkl

  subGenome1 = genome1[i: j + 1]
  subFmly1 = getFamily(subGenome1)  

  for g in subFmly1:
    occBefore = occ(g, genome1, 0, i - 1)
    occAfter = occ(g, genome1, j + 1, len(genome1) - 1)
    if  occBefore + occAfter  != 0:
      return False
    
  return True

def rule4_2(cijkl, genome2):
  i, j, k, l = cijkl

  subGenome2 = genome2[k: l + 1]
  subFmly2 = getFamily(subGenome2)

  for g in subFmly2:
    occBefore = occ(g, genome2, 0, k - 1)
    occAfter = occ(g, genome2, l + 1, len(genome2) - 1)
    if  occBefore + occAfter  != 0:
      return False
    
  return True

def rule4_3(cijkl, g1, g2):
  i, j, k, l = cijkl

  val1 = occ(g1[i], g1) <= occ(g1[i], g2)
  val2 = occ(g1[j], g1) <= occ(g1[j], g2)
  return val1 and val2

def rule4_4(cijkl, g1, g2):
  i, j, k, l = cijkl

  val1 = occ(g2[k], g2) <= occ(g2[k], g1)  
  val2 = occ(g2[l], g2) <= occ(g2[l], g1)
  return val1 and val2

def applyRule4(model, C, g1, g2, X):
  # Update model with changes made
  model.update()

  variablesToBeRemoved = []

  for cijkl in C:
    if not rule4_1(cijkl, g1):
      continue
    elif not rule4_2(cijkl, g2):
      continue
    elif not rule4_3(cijkl, g1, g2):
      continue
    elif not rule4_4(cijkl, g1, g2):
      continue
    else:
      print('will be removed: ', cijkl)
      variablesToBeRemoved.append(cijkl)    

  removeVariables(model, C, variablesToBeRemoved)

def applyRules(C, X, g1, g2):
  applyRule2(C, X, g1, g2)
  applyRule3(C, g1, g2)
  # applyRule4(model, C, g1, g2, X)
  pass

def isAcceptedInRule1(cijkl):
  i, j, k, l = cijkl
  if i != j and k != l:
    return True
    
  return False

def isAcceptedInRule2(cijkl, X, g1, g2):
  if rule2_1(X, cijkl):
    return False    

  elif rule2_2(X, cijkl, g1):
    return False
    
  elif rule2_3(X, cijkl):
    return False

  elif rule2_4(X, cijkl, g2):
    return False

  return True

def isAcceptedInRule3(cijkl, g1, g2):
  subAlphabet = getSubAlphabet(cijkl, g1, g2)
  for g in subAlphabet:
    if rule3Abs1(cijkl, g, g1, g2) > rule3Abs2(g, g1, g2):
      return False

  return True

def isAcceptedInAllRules(cijkl, X, g1, g2):
  if not isAcceptedInRule1(cijkl):
    return False

  if not isAcceptedInRule2(cijkl, X, g1, g2):
    return False

  if not isAcceptedInRule3(cijkl, g1, g2):
    return False
  
  return True
