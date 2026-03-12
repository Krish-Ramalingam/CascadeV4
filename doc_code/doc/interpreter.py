class Node:
    pass

# --- Statement Nodes ---
    
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

class ForNode(Node):
    # in the form: for x in 1..10  { ... }
    def __init__(self, variable, start, end, block):
        self.variable = variable
        self.start = start
        self.end = end
        self.block = block
    def __repr__(self):
        return f"For({self.variable}, {self.start}, {self.end}, {self.block})"
    

class HyperDependencyGraph:
    """
    Directed graph that models reactive dependencies between hypervariables.

    Each node represents a hypervariable. A directed edge from X to Y means
    "X depends on Y" — i.e. when Y changes, X may need to be recomputed.

    Internally, nodes are stored as a flat list and looked up by name.
    Edges are stored on each HyperNode as a list of neighbour references.
    """
    def __init__(self):
        self._nodes = []  # all registered HyperNode instances
        
    def addNode(self, node):
        self._nodes.append(node)

    def getNodes(self):
        return self._nodes
    
    def findNode(self, name):
        """Linear search for a node by name. Returns None if not found."""
        for node in self._nodes:
            if node.getName() == name:
                return node
        return None
    
    def addEdgeFromXToY(self, fromNodeName, toNodeName):
        """
        Add a directed dependency edge: fromNode → toNode.
        Silently does nothing if either name doesn't resolve to a known node.
        """
        fromNode = self.findNode(fromNodeName)
        toNode = self.findNode(toNodeName)
        if fromNode and toNode:
            fromNode.getEdges().append(toNode)

    def getEdges(self):
        """Return the full edge map as {nodeName: [dependencyNames]}."""
        edges = {}
        for node in self._nodes:
            edges[node.getName()] = [edge.getName() for edge in node.getEdges()]
        return edges
    
    def returnAllPointsToX(self, nodeName):
        """
        Return the names of all nodes that have a direct edge pointing TO nodeName.
        i.e. find all hypervariables that directly depend on the given variable.
        """
        pointingNodes = []
        for node in self._nodes:
            for edge in node.getEdges():
                if edge.getName() == nodeName:
                    pointingNodes.append(node.getName())
        return pointingNodes
    
    def returnAllXPointsTo(self, nodeName):
        """Return the names of all nodes that nodeName directly depends on (its outgoing edges)."""
        node = self.findNode(nodeName)
        if node:
            return [edge.getName() for edge in node.getEdges()]
        return []
    
    def descendants(self, nodeName, visited=None):
        """
        Recursively collect all nodes reachable from nodeName by following edges.
        i.e. everything that nodeName transitively depends on.
        Uses a visited set to guard against cycles.
        """
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
        """
        Recursively collect all nodes from which nodeName is reachable.
        i.e. every hypervariable that transitively depends on nodeName.
        Uses a visited set to guard against cycles.
        """
        if visited is None:
            visited = set()
        for node in self._nodes:
            for edge in node.getEdges():
                if edge.getName() == nodeName and node.getName() not in visited:
                    visited.add(node.getName())
                    self.ancestors(node.getName(), visited)
        return visited
    

class HyperNode:
    """
    A single node in the HyperDependencyGraph.
    
    Holds a hypervariable's name, its current cached value (or expression),
    and a list of outgoing edges (direct dependencies).
    """
    def __init__(self, name, value=None):
        self._name = name
        self._value = value  # cached value or ExprNode — recomputed on dependency change
        self._edges = []     # list of HyperNode references this node depends on
        
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
    """
    Tree-walk interpreter. Executes a list of AST nodes produced by the parser.

    State is held in three separate namespaces:
      env        — standard variable bindings: {name: value}
      hyperenv   — hypervariable expression store: {name: ExprNode}
                   Values are re-evaluated lazily each time the variable is read,
                   so they always reflect the current state of their dependencies.
      hyperdeps  — explicit dependency list per hypervariable: {name: [dep_names]}

    The hyperGraph mirrors the dependency relationships as a directed graph,
    enabling efficient ancestor/descendant traversal for reactive updates.
    """
    def __init__(self):
        self.env = {}          # standard variable environment: name → value
        self.hyperdeps = {}    # explicit dependency list per hvar: name → [dep names]
        self.hyperenv = {}     # hypervariable expression store: name → ExprNode
        self.hyperGraph = HyperDependencyGraph()

    def eval_expr(self, expr_node):
        """
        evaluate a postfix expr return its computed value

        uses a stack machine: data tokens are pushed, operators pop their operands
        and push the result. Supports arithmetic (+, -, *, /, ^), comparisons
        (>, <, ==, !=, >=, <=), and variable lookups from both env and hyperenv.
        """
        stack = []
        for tok in expr_node.tokens:
            typ, val = tok
            if typ == 'int':
                stack.append(val)
            elif typ == 'var':
                # Look up in standard env first; fall back to hyperenv with lazy eval
                if val not in self.env and val not in self.hyperenv:
                    raise Exception(f"Variable {val} not defined")
                if val in self.env:
                    stack.append(self.env[val])
                else:
                    stack.append(self.eval_expr(self.hyperenv[val]))
            elif typ in ['+', '-', '*', '/', '^']:
                #matches the operation to the logic to be performed
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
            elif typ == '<':
                b = stack.pop()
                a = stack.pop()
                stack.append(a < b)
            elif typ == '==':
                b = stack.pop()
                a = stack.pop()
                stack.append(a == b)
            elif typ == '!=':
                b = stack.pop()
                a = stack.pop()
                stack.append(a != b)
            elif typ == '>=':
                b = stack.pop()
                a = stack.pop()
                stack.append(a >= b)
            elif typ == '<=':
                b = stack.pop()
                a = stack.pop()
                stack.append(a <= b)
            else:
                raise Exception(f"Unknown token type: {typ}")
        if len(stack) != 1:
            raise Exception(f"Malformed expression: {expr_node.tokens}")
        return stack[0]

    def exec_nodes(self, nodes):
        """Execute a sequence of AST nodes in order (e.g. a block body)."""
        for node in nodes:
            self.exec_node(node)

    def update_ancestors(self, node):
        """
        Propagate a variable change upward through the dependency graph.

        After a standard variable is assigned, any hypervariable that depends on it
        (directly or transitively) needs its cached value refreshed. This method
        walks up the graph via returnAllPointsToX and recursively triggers updates
        on each ancestor so the reactive chain stays consistent.
        """
        if node.name in self.hyperGraph.getEdges():
                    for dep in self.hyperGraph.returnAllPointsToX(node.name):
                        if dep in self.hyperenv:
                            self.hyperenv[dep] = self.eval_expr(self.hyperenv[dep])
                            self.update_ancestors(self.hyperGraph.findNode(dep))

    def exec_node(self, node):
        """
        execution for a single AST node based on its type

        Uses string-based type inspection rather than isinstance() — this keeps
        the interpreter decoupled from the specific parser module that produced
        the nodes

          VarDeclNode       — evaluate RHS, store in env, propagate to dependents
          ExprStmtNode      — evaluate expression for side-effects, discard result
          IfNode            — evaluate condition; execute block only if true
          OutNode           — evaluate expression and print the result
          HyperVarDeclNode  — register expression and dependencies in hyperenv/graph
          WhileNode         — repeatedly evaluate condition and execute block
          ForNode           — iterate a loop variable over an integer range (inclusive)

        raises on any unrecognised node type.
        """
        # print(str(type(node)).split(".")[-1].replace("'>", ""))
        if str(type(node)).split(".")[-1].replace("'>", "") == "VarDeclNode":
            if node.expr:
                val = self.eval_expr(node.expr)
                #print(f"Updated {node.name} to {val}")
                self.update_ancestors(node)  # notify any hvars that depend on this variable
            else:
                val = None
            self.env[node.name] = val
        elif str(type(node)).split(".")[-1].replace("'>", "") == "ExprStmtNode":
            self.eval_expr(node.expr)
        elif str(type(node)).split(".")[-1].replace("'>", "") == "IfNode":
            print("Evaluating condition for if statement: ", node.condition)
            cond_val = self.eval_expr(node.condition)
            if cond_val:
                self.exec_nodes(node.block)
        elif str(type(node)).split(".")[-1].replace("'>", "") == "OutNode":
            val = self.eval_expr(node.expr)
            print(val)
        elif str(type(node)).split(".")[-1].replace("'>", "") == "HyperVarDeclNode":
            if node.expr:
                ex = node.expr
            else:
                ex = None
            # Register the expression and dependencies, then wire up the graph edges
            self.hyperenv[node.name] = ex
            self.hyperdeps[node.name] = node.dependencies
            self.hyperGraph.addNode(HyperNode(node.name, ex))
            for dep in node.dependencies:
                # Each dependency becomes a directed edge: this hvar → dep variable
                self.hyperGraph.addEdgeFromXToY(node.name, dep)
        elif str(type(node)).split(".")[-1].replace("'>", "") == "WhileNode":
            while self.eval_expr(node.condition):
                self.exec_nodes(node.block)
        elif str(type(node)).split(".")[-1].replace("'>", "") == "ForNode":
            var_name = node.variable
            # Range bounds can be integer literals or variable references
            if node.start.isdigit():
                start_val = int(node.start)
            else:
                start_val = self.env[node.start] if node.start in self.env else self.hyperenv[node.start]
            if node.end.isdigit():
                end_val = int(node.end)
            else:
                end_val = self.env[node.end] if node.end in self.env else self.hyperenv[node.end]
            # Range is inclusive on both ends — hence end_val + 1
            for i in range(start_val, end_val + 1):
                self.env[var_name] = i
                self.exec_nodes(node.block)
        
            
        else:
            raise Exception(f"Unknown node type: {node}")