from node import Node
import math

def ID3(examples, default):
  #If no examples, return default option
  if (len(examples) <= 0):
    return Node(default, True)
  no_split = sameCheck(examples)
  if (no_split):
    return Node(no_split, True)
  else:
    best = choose_attribute(examples)
    dTree = Node(best, False)
    bestValues = []
    for e in examples:
      if (e[best] not in bestValues):
        bestValues.append(e[best])
    for v in bestValues:
      newExamples = []
      for ex in examples:
        if (ex[best] == v):
          newExamples.append(ex)
      


#Returns false if non-trivial splits exist, and the most common attribute otherwise
def sameCheck(examples):
  #First, check if the list is only one item long
  if (len(examples) == 1):
    return examples[0]["Class"]
  #Otherwise, proceed to check for non-trivial splits
  classCheck = False
  attCheck = False
  exCompare = examples[0]
  classList = []
  #Iterate through examples
  for ex in examples:
    classList.append(ex["Class"])
    #If any classes differ, we know not all classes are same
    if (ex["Class"] != exCompare["Class"]):
      classCheck = True
    for key in ex:
      if (key != "Class"):
        #if any non-class attributes differ, we know there can be categorical splits
        if (ex[key] != exCompare[key]):
          attCheck = True
  #if there are both categorical splits and not all classes are the same, then there are non-trivial splits
  if (classCheck and attCheck):
    return False
  #otherwise, return most common class
  else:
    return mode(classList)

#Takes in a list as input and returns the item that appears most on the list
def mode(mList):
  itemCounter = {}
  maxMode = 0
  maxItem = 0
  for i in mList:
    if (i not in itemCounter):
      itemCounter[i] = 1
    else:
      itemCounter[i] += 1
  for item in itemCounter:
    if (itemCounter[item] > maxMode):
      maxItem = item
      maxMode = itemCounter[item]
  return maxItem

#Cycles through attributes and computes entropy. Returns attribute that reduces entropy the most or false if none reduce entropy
def choose_attribute(examples):
  #gets a list of attributes to assess examples by
  sample = examples[0]
  attList = sample.keys()

  #keeps track of min entropy and which attribute to split on
  maxEntropy = -1000000000000
  att_to_split = False

  #iterate through each attribute
  for att in attList:
    if (att != "Class"):
      attValues = {}
      entropySum = 0
      for x in examples:
        #Create a new dictionary entry for each unique attribute value
        if (x[att] not in attValues):
          attValues[x[att]] = {x["Class"] : 1}
        else:
          #If no instance of that class has occurred under that attribute value, add new entry for class
          if (x["Class"] not in attValues[x[att]]):
            attValues[x[att]][x["Class"]] = 1
          #If it has occurred, iterate the counter for that class
          else:
            attValues[x[att]][x["Class"]] += 1
      #For each attribute value, calculate entropy
      for a in attValues:
        branchEntropy = 0
        totalCount = 0
        #Get the sum of all items who had an attribute of that value 
        for val in attValues[a].itervalues():
          totalCount += val
        #calculate the entropy of each class 
        for c in attValues[a].itervalues():
          p = (float(c)/float(totalCount))
          branchEntropy -= p*math.log(p,2)
        entropySum -= branchEntropy
      if (entropySum > maxEntropy):
        maxEntropy = entropySum
        att_to_split = att     
  return att_to_split


def prune(node, examples):
  '''
  Takes in a trained tree and a validation set of examples.  Prunes nodes in order
  to improve accuracy on the validation data; the precise pruning strategy is up to you.
  '''

def test(node, examples):
  '''
  Takes in a trained tree and a test set of examples.  Returns the accuracy (fraction
  of examples the tree classifies correctly).
  '''


def evaluate(node, example):
  '''
  Takes in a tree and one example.  Returns the Class value that the tree
  assigns to the example.
  '''
