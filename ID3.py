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
  benchmark = test(node, examples)
  visited = [] #list of already visited nodes
  done = False
  currNode = node
  ptree = None
  while(not done):
    if(check_children_for_classes(currNode)):
      temp = prune_test(node, currNode, examples, benchmark)
      ptree = temp[0]
      benchmark = temp[1]
    else:
      for c in currNode.children:
        if(c not in visited and not c.isClass):
          currNode = c
          break
      if(currNode.parent=="ROOT"):
        done = True #root node reached, so no more pruning left to do
      else: #all children have been tested but parent is not root; test parent
        temp = prune_test(node, currNode, examples, benchmark)
        ptree = temp[0]
        benchmark = temp[1]

  return ptree

#Tests whether the given node in the tree should be pruned given the validation set
def prune_test(root, node, vset, benchmark):
  newNode = node
  bm = benchmark

  #substitute each of the's children in place of the node in the tree and run test
  for c in newNode.children:
    c.addparent(newNode.parent) #child's parent is now the parent's parent
      #add in child as child of node's parent, and remove node as child
      #value for child being added is identical to value for parent node being removed
      newNode.parent.addchild(c,newNode.parent.children[newNode])
      newNode.parent.erasechild(newNode)
      result = test(root, vset)
      if(result >= bm):
        newNode = c
        bm = result
      else: #revert changes to tree for retesting
        newNode.parent.addchild(newNode,newNode.parent.children[c])
        c.addparent(newNode)
        newNode.parent.erasechild(c)
  
  #return the root of the modified tree and the new benchmark
  return [root, bm]


#Checks whether all children of the node are classes
def check_children_for_classes(node):
  for c in node.children:
    if(not c.isClass):
      return False
  return True
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



