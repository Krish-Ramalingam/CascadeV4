
class Node:
    pass

# Statement Nodes
    
class HyperVarDeclNode(Node):
    def __init__(self, name, dependencies, expr):
        self.name = name
        self.dependencies = dependencies
        self.expr = expr
    def __repr__(self):
        return f"HyperVarDecl({self.name}, {self.dependencies}, {self.expr})" 
class OutNode(Node):
    def __init__(self, expr):
        self.expr = expr
    def __repr__(self):
        return f"Out({self.expr})"

class VarDeclNode(Node):
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr
    def __repr__(self):
        return f"VarDecl({self.name}, {self.expr})"

class IfNode(Node):
    def __init__(self, condition, block):
        self.condition = condition
        self.block = block
    def __repr__(self):
        return f"If({self.condition}, {self.block})"

class ExprStmtNode(Node):
    def __init__(self, expr):
        self.expr = expr
    def __repr__(self):
        return f"ExprStmt({self.expr})"

# Expression Node (postfix)
class ExprNode(Node):
    def __init__(self, tokens):
        self.tokens = tokens
    def __repr__(self):
        return f"Expr({self.tokens})"
    
class WhileNode(Node):
    def __init__(self, condition, block):
        self.condition = condition
        self.block = block
    def __repr__(self):
        return f"While({self.condition}, {self.block})"

class HyperDependencyGraph:
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
    
    def returnAllPointsToX(self, nodeName):
        pointingNodes = []
        for node in self._nodes:
            for edge in node.getEdges():
                if edge.getName() == nodeName:
                    pointingNodes.append(node.getName())
        return pointingNodes
    
    def returnAllXPointsTo(self, nodeName):
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
    
class HyperNode:
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

class Interpreter:
    def __init__(self):
        self.env = {}  # variable environment
        self.hyperdeps = {}  # hypervariable dependencies
        self.hyperenv = {}  # hypervariable environment
        self.hyperGraph = HyperDependencyGraph()

    # Evaluate a postfix expression
    def eval_expr(self, expr_node):
        stack = []
        for tok in expr_node.tokens:
            typ, val = tok
            if typ == 'int':
                stack.append(val)
            elif typ == 'var':
     
                if val not in self.env and val not in self.hyperenv:
                    raise Exception(f"Variable {val} not defined")
                if val in self.env:
                    stack.append(self.env[val])
                else:
                    stack.append(self.eval_expr(self.hyperenv[val]))
            elif typ in ['+', '-', '*', '/', '^']:
                b = stack.pop()
                a = stack.pop()
                if typ == '+':
                    stack.append(a + b)
                elif typ == '-':
                    stack.append(a - b)
                elif typ == '*':
                    stack.append(a * b)
                elif typ == '/':
                    stack.append(a / b)
                elif typ == '^':
                    stack.append(a ** b)
            elif typ == '>':
                b = stack.pop()
                a = stack.pop()
                stack.append(a > b)
            else:
                raise Exception(f"Unknown token type: {typ}")
        if len(stack) != 1:
            raise Exception(f"Malformed expression: {expr_node.tokens}")
        return stack[0]

    # Execute a list of nodes
    def exec_nodes(self, nodes):
        for node in nodes:
            self.exec_node(node)

    
    def update_ancestors(self, node):
        if node.name in self.hyperGraph.getEdges():
                    for dep in self.hyperGraph.returnAllPointsToX(node.name):
                        if dep in self.hyperenv:
                            self.hyperenv[dep] = self.eval_expr(self.hyperenv[dep])
                            self.update_ancestors(self.hyperGraph.findNode(dep))
    # Execute a single node
    def exec_node(self, node):
        if str(type(node)).split(".")[-1].replace("'>", "") == "HyperVarDeclNode":
            val = self.eval_expr(node.expr)
        elif str(type(node)).split(".")[-1].replace("'>", "") == "VarDeclNode":
            if node.expr:
                val = self.eval_expr(node.expr)
                self.update_ancestors(node)
            else:
                val = None
            self.env[node.name] = val
        elif str(type(node)).split(".")[-1].replace("'>", "") == "ExprStmtNode":
            self.eval_expr(node.expr)
        elif str(type(node)).split(".")[-1].replace("'>", "") == "IfNode":
            cond_val = self.eval_expr(node.condition)
            if cond_val:
                self.exec_nodes(node.block)
        elif str(type(node)).split(".")[-1].replace("'>", "") == "OutNode":
            val = self.eval_expr(node.expr)
            print(val)
        elif str(type(node)).split(".")[-1].replace("'>", "") == "HyperVarDeclNode":
            print("hi")
            if node.expr:
                ex = node.expr
            else:
                ex = None
            self.hyperenv[node.name] = ex
            print(self.hyperenv)
            self.hyperdeps[node.name] = node.dependencies
            self.hyperGraph.addNode(HyperNode(node.name, ex))
            for dep in node.dependencies:
                self.hyperGraph.addEdgeFromXToY(node.name, dep)
        
            
        else:
            raise Exception(f"Unknown node type: {node}")
       
 
