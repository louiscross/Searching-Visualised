#This is the class to represent maps
class Map:
  def __init__(self, nodes):
    self.nodes = nodes
  
    
  def addNodes(self,nodes):
    self.nodes.append(nodes)

  def getNodes(self,nodes):
    return self.nodes
  
  def getNodeByIndex(self, index):
    if 0 <= int(index) < len(self.nodes):
        return self.nodes[index]
    else:
        return None
  
  def getNodeByName(self, nodename):     
    for node in self.nodes:
      if node.nodeName == nodename:
        return node
  def getWeightByName(self,nodename):
    for node in self.nodes:
      if node.nodeName == nodename:
        return node.weight

  def __str__(self):
    node_strings = [str(node) for node in self.nodes]
    return "\n".join(node_strings)
  
