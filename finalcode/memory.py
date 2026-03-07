class Scope:
    def __init__(self, parent=None):
        self.parent = parent
        self.variables = {}

    def set_variable(self, name, value):
        self.variables[name] = value

    def get_variable(self, name):
        if name in self.variables:
            return self.variables[name]
        elif self.parent is not None:
            return self.parent.get_variable(name)
        else:
            raise NameError(f"Variable '{name}' not found in scope.")
        
    def set_hypervariable(self, name, params, relationship):
        self.variables[name] = {
            "params": params,
            "relationship": relationship
        }
        
    def get_hypervariable(self, name):
        if name in self.variables:
            return self.variables[name]
        elif self.parent is not None:
            return self.parent.get_hypervariable(name)
        else:
            raise NameError(f"Hypervariable '{name}' not found in scope.")
    
    
        
class Memory:
    def __init__(self):
        self.global_scope = Scope()
        self.current_scope = self.global_scope

    def enter_scope(self):
        new_scope = Scope(parent=self.current_scope)
        self.current_scope = new_scope

    def exit_scope(self):
        if self.current_scope.parent is not None:
            self.current_scope = self.current_scope.parent
        else:
            raise Exception("Cannot exit global scope.")

    def set_variable(self, name, value):
        if self.current_scope is not None:
            self.current_scope.set_variable(name, value)

    def get_variable(self, name):
        return self.current_scope.get_variable(name)
    
    
ram = Memory()
ram.set_variable('x', 10)
ram.enter_scope()
ram.set_variable('y', 20)
print(ram.get_variable('x'))  # Output: 10
print(ram.get_variable('y'))  #Output: 20
ram.exit_scope()
ram.get_variable('y')  # This will raise an exception since 'y' is not in the global scope

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

