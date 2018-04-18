class Node:
#It's a tree!

  	def __init__(self, attribute, isClass):
  		#attribute that will be used to split
    	self.attribute = attribute

    	#parent node - can only have one parent
    	self.parent = "ROOT"

    	#list of children nodes
    	self.children = []
      
      #If false, node is attribute. If true, node is class and "attribute" label denotes which class
      self.isClass = isClass
	
    def addparent(self,node):
    	self.parent = node

    def addchild(self,node):
    	self.children.append(node)

    def eraseparent(self):
    	self.parent = None

   	def erasechild(self,node):
   		self.children.remove(node)