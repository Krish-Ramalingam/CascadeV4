class dependencyGraph:
    def __init__(self):
        self.nodes = []
        
    def addNode(self, node):
        self.nodes.append(node)

    def getNodes(self):
        return self.nodes
    
    def findNode(self, name):
        for node in self.nodes:
            if node.name == name:
                return node
        return None
    
    def addEdge(self, fromNodeName, toNodeName):
        fromNode = self.findNode(fromNodeName)
        toNode = self.findNode(toNodeName)
        if fromNode and toNode:
            fromNode.edges.append(toNode)
    
    def getEdges(self):
        edges = {}
        for node in self.nodes:
            edges[node.name] = [edge.name for edge in node.edges]
        return edges
    
    def returnAllPointingTo(self, nodeName):
        pointingNodes = []
        for node in self.nodes:
            for edge in node.edges:
                if edge.name == nodeName:
                    pointingNodes.append(node.name)
        return pointingNodes
    
    def returnAllPointedFrom(self, nodeName):
        node = self.findNode(nodeName)
        if node:
            return [edge.name for edge in node.edges]
        return []
    
    
class Node:
    def __init__(self, name, value=None):
        self.name = name
        self.value = value
        self.edges = []
        
        