import sys
# sys.path.append("..")
from readGenome import readGenome

def addFinalSuffix(genomeName):
  return genomeName + '.final' if '.final' not in genomeName else genomeName

def getG(name):
  return readGenome(addFinalSuffix(name))

def getGenomes(argv):
  genomeName1, genomeName2 = argv[1], argv[2]
  g1, g2 = getG(genomeName1), getG(genomeName2)
  # print(g1, g2)
  return g1, g2

def getFamily(genome):
  fmly = {}

  for idx, g in enumerate(genome):
    if g not in fmly:
      fmly[g] = [idx]
    else:
      fmly[g].append(idx)

  return fmly
