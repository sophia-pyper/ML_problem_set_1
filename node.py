class Node:
#It's a tree!
  def __init__(self, attribute, isClass):
		#attribute that will be used to split
    self.attribute = attribute

  	#parent node - can only have one parent
    self.parent = "ROOT"

  	#list of children nodes
    self.children = {}
    
    #If false, node is attribute. If true, node is class and "attribute" label denotes which class
    self.isClass = isClass

    #Sets a default child value based on the mode. Used for classifying examples with values the tree has not seen
    self.defaultChild = 0

  def addparent(self,node):
  	self.parent = node

  def addchild(self,node, val):
  	self.children[node] = val

  def eraseparent(self):
  	self.parent = None

  def erasechild(self,node):
 		del self.children[node]

  def copyAttributes(self, aList):
    self.attribute = aList[0]
    self.children = aList[1]
    self.isClass = aList[2]
    self.defaultChild = aList[3]

  def exportAttributes(self):
    return [self.attribute, self.children, self.isClass, self.defaultChild]

    

