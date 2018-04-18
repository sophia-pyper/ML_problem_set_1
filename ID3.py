from node import Node
import math
import copy

def ID3(examples, default):
  #If no examples, return default option
  if (len(examples) <= 0):
    return Node(default, True)
  #Check whether non-trivial splits are available
  no_split = sameCheck(examples)
  #If not, return node with the default option
  if (no_split):
    nodeVal = mode(examples)
    return Node(nodeVal, True)
  else:
    best = choose_attribute(examples)
    dTree = Node(best, False)
    bestValues = []
    valueMode = 0
    modeChild = 0
    #Find all values of attribute
    for e in examples:
      if (e[best] not in bestValues):
        bestValues.append(e[best])
    #Iterate through values 
    for v in bestValues:
      newExamples = []
      #Go through all the examples whose attribute is equal to the given value
      for ex in examples:
        if (best in ex):
          if (ex[best] == v):
            #deletes attributes from example so they don't get split on again
            newEx = copy.deepcopy(ex)
            del newEx[best]
            newExamples.append(newEx)
      #Changes default value for ambiguous data for parent node
      if (len(newExamples) > valueMode):
        valueMode = len(newExamples)
      #Add value node to root node, recursing to continue the tree
      newTree = ID3(newExamples, mode(newExamples))
      if (valueMode == len(newExamples)):
        modeChild = newTree
      newTree.addparent(dTree)
      dTree.addchild(newTree, v)
    #Add default child to parent
    dTree.defaultChild = modeChild
    return dTree



#Returns True if no non-trivial splits exist, and False otherwise
def sameCheck(examples):
  #First, check if the list is only one item long
  if (len(examples) == 1):
    return True
  #Otherwise, proceed to check for non-trivial splits
  classCheck = False
  attCheck = False
  exCompare = examples[0]
  #Iterate through examples
  for ex in examples:
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
    return True

#Takes in a list as input and returns the item that appears most on the list
def mode(examples):
  itemCounter = {}
  maxMode = 0
  maxItem = 0
  for i in examples:
    if (i["Class"] not in itemCounter):
      itemCounter[i["Class"]] = 1
    else:
      itemCounter[i["Class"]] += 1
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
      #If entropy is better (less negative) than previous entropy, set it as the new max
      if (entropySum > maxEntropy):
        maxEntropy = entropySum
        att_to_split = att     
  return att_to_split


#Returns pruned tree based on accuracy stats from validation set (examples)
def prune(node, examples):
  #If child is not the bottom-most attribute above leaves, keep going down
  for c in node.children:
    if (not c.isClass):
      c = prune(c, examples)
  #Find root to establish baseline
  root = node
  while (root.parent != "ROOT"):
    root = root.parent
  baseline = test(root, examples)
  #For each child, copy info to parent and retest accuracy
  for child in node.children:
    savedNodeInfo = node.exportAttributes()
    childInfo = child.exportAttributes()
    node.copyAttributes(childInfo)
    newAccuracy = test(root, examples)
    #If accuracy doesn't improve, revert node to previous info
    if (newAccuracy <= baseline):
      node.copyAttributes(savedNodeInfo)
    #Otherwise, leave child in the place of old parent
    else:
      baseline = newAccuracy
  return node





#Classifies a series of nodes and gets accuracy of tree
def test(node, examples):
  total = len(examples)
  correctCount = 0
  #For each example, evaluate and see whether tree classifies correctly. 
  for e in examples:
    guessClass = evaluate(node, e)
    if (guessClass == e['Class']):
      correctCount += 1
  return (float(correctCount)/float(total))


#Evaluates classifications of an individual node
def evaluate(node, example):
  #If node is a leaf, return value
  if (node.isClass):
    return node.attribute
  else:
    #Otherwise, find value of example for node's attribute
    exValue = example[node.attribute]
    #Recurse with the child node who is assigned that value
    for child in node.children:
      if (exValue == node.children[child]):
        return evaluate(child, example)
    #If it makes it here, no node had that attribute value
    #In that case, we send it to the default child
    newChild = node.defaultChild
    return evaluate(newChild, example)



