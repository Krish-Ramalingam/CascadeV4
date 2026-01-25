class dependencyGraph:
    def __init__(self):
        self._nodes = []
        
    def addNode(self, node):
        self._nodes.append(node)

    def getNodes(self):
        return self._nodes
    
    def findNode(self, name):
        for node in self._nodes:
            if node.getName() == name:
                return node
        return None
    
    def addEdgeFromXToY(self, fromNodeName, toNodeName):
        fromNode = self.findNode(fromNodeName)
        toNode = self.findNode(toNodeName)
        if fromNode and toNode:
            fromNode.getEdges().append(toNode)

    def getEdges(self):
        edges = {}
        for node in self._nodes:
            edges[node.getName()] = [edge.getName() for edge in node.getEdges()]
        return edges
    
    def returnAllPointingTo(self, nodeName):
        pointingNodes = []
        for node in self._nodes:
            for edge in node.getEdges():
                if edge.getName() == nodeName:
                    pointingNodes.append(node.getName())
        return pointingNodes
    
    def returnAllPointedFrom(self, nodeName):
        node = self.findNode(nodeName)
        if node:
            return [edge.getName() for edge in node.getEdges()]
        return []
    
    def descendants(self, nodeName, visited=None):
        if visited is None:
            visited = set()
        node = self.findNode(nodeName)
        if node:
            for edge in node.getEdges():
                if edge.getName() not in visited:
                    visited.add(edge.getName())
                    self.descendants(edge.getName(), visited)
        return visited
    
    def ancestors(self, nodeName, visited=None):
        if visited is None:
            visited = set()
        for node in self._nodes:
            for edge in node.getEdges():
                if edge.getName() == nodeName and node.getName() not in visited:
                    visited.add(node.getName())
                    self.ancestors(node.getName(), visited)
        return visited
    
class Node:
    def __init__(self, name, value=None):
        self._name = name
        self._value = value
        self._edges = []
        
    def getName(self):
        return self._name

    def getValue(self):
        return self._value

    def getEdges(self):
        return self._edges
    
    def setName(self, name):
        self._name = name
        
    def setValue(self, value):
        self._value = value
        
    def addEdge(self, node):
        self._edges.append(node)
    
    def setEdges(self, edges: list):
        self._edges = edges
        
myDepGraph = dependencyGraph()
myDepGraph.addNode(Node("A"))
myDepGraph.addNode(Node("B"))

myDepGraph.addEdgeFromXToY("A", "B")
print(myDepGraph.getEdges())
print(myDepGraph.returnAllPointingTo("B"))
print(myDepGraph.returnAllPointedFrom("A"))
print(myDepGraph.descendants("A"))
print(myDepGraph.ancestors("B"))
myDepGraph.addNode(Node("C"))
myDepGraph.addEdgeFromXToY("B", "C")
print(myDepGraph.descendants("A"))
print(myDepGraph.ancestors("C"))