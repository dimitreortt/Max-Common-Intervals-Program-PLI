from MaxCI_Sequencial.timeMeasurer import secondsToTime
import time

startTime = 0
wasChecked = False
def doMeasureTime(idx2):
  global startTime
  global globalG1
  global wasChecked

  # print('lala start time', startTime, time.time())  
  if idx2 == 2 and not wasChecked:
    startTime = time.time()
    wasChecked = True
    
  elif idx2 == 3:
    timeTaken = time.time() - startTime
    listadetamanhos = [j - i for i in range(len(globalG1)) for j in range(i, len(globalG1))]
    numPossib1 = len(listadetamanhos)
    prediction = (time.time() - startTime) * numPossib1
    print(startTime, (time.time() - startTime), numPossib1, prediction)
    exit('A predição de tempo diz: %s' % secondsToTime(prediction))

  pass

lastShown = 0
def showPercentageCovered():
  global globalG1
  global idx1
  global idx2
  global lastShown

  if idx2 == 2 or idx2 == 3:
    doMeasureTime(idx2)

  if len(globalG1) < 50:
    val = (idx1 / len(globalG1) * 100)
    if val != lastShown:
      print('%.2f percent of tuple vars explored...' % val)
      lastShown = val

  elif idx1 % int(len(globalG1) / 200) == 1:
    val = (idx1 / len(globalG1) * 100)
    if val != lastShown:
      print('%.2f percent of tuple vars explored...' % val)
      lastShown = val

def resetNextVarTuples(newGenome1, newGenome2):
  global globalG1
  global globalG2
  global idx1
  global idx2

  globalG1 = newGenome1
  globalG2 = newGenome2
  idx1 = 0
  idx2 = 1
  idx3 = 0
  idx4 = 0

def updateNextVarTuplesAndReturn():
  global globalG1
  global globalG2
  global idx1
  global idx2
  global idx3
  global idx4  

  if idx4 >= len(globalG2) - 1:
    if idx3 < len(globalG2) - 2:
      idx3 += 1
      idx4 = idx3 + 1

    else:
      if idx2 >= len(globalG1) - 1:
        if idx1 < len(globalG1) - 2:
          idx1 += 1
          idx2 = idx1 + 1
          idx3 = 0
          idx4 = 1

        else:
          return
      
      else:
        idx2 += 1
        idx3 = 0
        idx4 = 1

  else:
    idx4 += 1
  
  if idx2 == 2 or idx2 == 3:
    doMeasureTime(idx2)
  # if idx4 % 200 == 0:
  #   if idx3 % 5 == 0:
      # print((idx1, idx2, idx3, idx4))
  return (idx1, idx2, idx3, idx4)

globalG1 = []
globalG2 = []
idx1 = 0
idx2 = 1
idx3 = 0
idx4 = 0
def nextVarTuple(g1, g2):
  global globalG1
  global globalG2
  global idx1
  global idx2
  global idx3
  global idx4

  if globalG1 != g1 or globalG2 != g2:
    resetNextVarTuples(g1, g2)

  return updateNextVarTuplesAndReturn()