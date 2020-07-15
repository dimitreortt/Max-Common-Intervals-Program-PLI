import os

def coherseList(list):
  return [int(i) for i in list]

def readGenomeFromStringFormat(pathToGenome):
  return coherseList(open(pathToGenome).read().split())

def stringToList(string):
  return string.replace('[', '').replace(']', '').replace(' ', '').replace('\'', '').split(',')

def readGenomeFromListFormat(pathToGenome):
  genomeListString = open(pathToGenome).read()
  return coherseList(stringToList(genomeListString))

def readGenome(name):
  prefix = os.path.dirname(__file__) + '/../../../Entradas/Genomes/'
  try:
    return readGenomeFromStringFormat(prefix + name)
  except ValueError:
    return readGenomeFromListFormat(prefix + name)