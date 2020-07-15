# Add constraints: C.01
def createConstraintsC01(model, C, X, g1):
  model.addConstrs((X.sum(i, "*") <= 1 for i in range(len(g1))), "C.01")

# Add constraints: C.02
def createConstraintsC02(model, C, X, g2):
  model.addConstrs((X.sum("*", j) <= 1 for j in range(len(g2))), "C.02")

# Add constraints: C.03
def createConstraintsC03(model, C, X):
  print('Creating constraints C.03...')
  for cijkl in C:
    a = 4 * C[cijkl]
    
    i, j, k, l = cijkl
    lisk = [val for val in range(i, j + 1)]
    lisi = [val for val in range(k, l + 1)]

    b = X.sum(i, lisi)
    c = X.sum(j, lisi)
    d = X.sum(lisk, k)
    e = X.sum(lisk, l)
    model.addConstr(a - b - c - d - e <= 0, "C.03.c[%s]" % str(cijkl))

  model.update()

# Add constraint: C.04
def createConstraintsC04(model, C, X, lisij, lisk, cijkl):
  for item in lisij:
    listOff = X.select(item, lisk)
    if(listOff):
      for element in listOff:
        model.addConstr(C[cijkl] + element <= 1, 'C.04')

# Add constraint: C.05
def createConstraintsC05(model, C, X, lisij, lisl, cijkl):
  for item in lisij:    
    listOff2 = X.select(item, lisl)
    if(listOff2):
      for element in listOff2:
        model.addConstr(C[cijkl] + element <= 1, 'C.05')

# Add constraint: C.06
def createConstraintsC06(model, C, X, liskl, lisi, cijkl):
  for item in liskl:    
    listOff = X.select(lisi, item)
    if(listOff):
      for element in listOff:
        model.addConstr(C[cijkl] + element <= 1, 'C.06')

# Add constraint: C.07
def createConstraintsC07(model, C, X, liskl, lisj, cijkl):  
  for item in liskl:
    listOff2 = X.select(lisj, item)
    if(listOff2):
      for element in listOff2:
        model.addConstr(C[cijkl] + element <= 1, 'C.07')

# Add constraints C.04 to C.07
def createConstraintsC04ToC07(model, C, X, g1, g2):
  print('Creating constraints C.04 to C.07...\n')
  for cijkl in C:   
    i = cijkl[0]; j = cijkl[1]; k = cijkl[2]; l = cijkl[3]
    lisij = [val for val in range(i+1, j)]
    lisk = [val for val in range(0,k)]
    lisl = [val for val in range(l+1, len(g2))]

    createConstraintsC04(model, C, X, lisij, lisk, cijkl)
    createConstraintsC05(model, C, X, lisij, lisl, cijkl)

    liskl = [val for val in range(k+1, l)]
    lisi = [val for val in range(0,i)]
    lisj = [val for val in range(j+1,len(g1))]

    createConstraintsC06(model, C, X, liskl, lisi, cijkl)
    createConstraintsC07(model, C, X, liskl, lisj, cijkl)

# Add constraint: C.08
def createConstraintsC08(model, X, g1, g2):
    fmly = {}
    # create dictionary {gene family : members of family in GA}
    for idx, itm in enumerate(g1):
        if(itm not in fmly):
            fmly[itm] = [idx]
        else:
            fmly[itm].extend([idx])
    
    # create dictionary {gene family : numbers of members of family in GB}
    fmly2 = {}
    for itm in g2:
        if(itm not in fmly2):
            fmly2[itm] = 1
        else:
            fmly2[itm] = fmly2[itm] + 1
    # at this point fmly2 holds the number of presences of each family in GB
    
    numDuplicates = 0
    # the code below stores in fmly2 for each family present in GA and GB the min number of appearances
        # considering GA and GB, that is used for mapping the most duplicate genes possible in maximum matching model
    for itm in fmly2:
        if(itm in fmly):
            numDuplicates = numDuplicates + fmly2[itm] + len(fmly[itm]) - 2
            fmly2[itm] = min(fmly2[itm], len(fmly[itm]))
            #print itm, fmly2[itm], len(fmly[itm]),  fmly2[itm] + len(fmly[itm]) - 2, numDuplicates

    for g in fmly:
        # essential verification
        if(g in fmly2):
            # this code adds the constraint C.08, telling m.addConstr(X.sum(fmly[g], '*') == fmly2[g]) we say
                # that we want to match the most duplicates possible, this is the maximum matching model
            model.addConstr(X.sum(fmly[g], '*') == fmly2[g])

def createConstraints(model, C, X, g1, g2):
  createConstraintsC01(model, C, X, g1)
  createConstraintsC02(model, C, X, g2)
  createConstraintsC03(model, C, X)
  createConstraintsC04ToC07(model, C, X, g1, g2)
  createConstraintsC08(model, X, g1, g2)
