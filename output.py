def writeOutput(model, L):
  for v in model.getVars():
    if v.x == 1:
      print('%s %g, obj: %d' % (v.varName, v.x, model.objVal + L))

  print(L)      