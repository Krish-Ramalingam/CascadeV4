"""
Parser: A module for parsing input data and constructing Abstract Syntax Trees (ASTs).
Input: Tokens from the lexer.
Output: An Abstract Syntax Tree (AST) representing the structure of the input data.
"""
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
    


def dijkstraShuntingYard(tokens):
    precedence = {
        "||": 1,
        "&&": 2,
        ">": 3, "<": 3,
        "+": 3, "-": 4,
        "*": 4, "/": 5,
        "^": 6
    }
    
    right_assoc = {"^"}
    output  = []
    opstack = []

    def is_data(tok):
        return tok[0] in ["int", "float", "var", "bool"]

    def peek(stack):
        return stack[-1] if stack else None

    for tok in tokens:
        if is_data(tok):
            output.append(tok)

        elif tok[0] == "(":
            opstack.append(tok)

        elif tok[0] == ")":
            while opstack and peek(opstack)[0] != "(":
                output.append(opstack.pop())
            opstack.pop()

        elif tok[0] in precedence:
            while (opstack and
                   peek(opstack)[0] in precedence and
                   (precedence[peek(opstack)[0]] > precedence[tok[0]] or
                   (precedence[peek(opstack)[0]] == precedence[tok[0]]
                    and tok[0] not in right_assoc))):
                output.append(opstack.pop())
            opstack.append(tok)

    while opstack:
        output.append(opstack.pop())

    return output

class ParserNodes:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consume(self, expected_type=None):
        tok = self.peek()
        if tok is None:
            raise Exception("Unexpected end of tokens")
        if expected_type and tok[0] != expected_type:
            raise Exception(f"Expected {expected_type}, got {tok}")
        self.pos += 1
        return tok

    def parse_program(self):
        stmts = []
        while self.peek() is not None:
            stmts.append(self.parse_statement())
        return stmts

    def parse_statement(self):
        tok = self.peek()
        if tok[0] == 'out':
            self.consume('out')
            expr = self.parse_expression()
            self.consume(';')
            return OutNode(expr)

        elif tok[0] == 'if':
            self.consume('if')
            cond = self.parse_expression()
            # optional semicolon before block
            if self.peek() and self.peek()[0] == ';':
                self.consume(';')
            self.consume('{')
            block = self.parse_block()
            return IfNode(cond, block)
        
        elif tok[0] == 'while':
            self.consume('while')
            cond = self.parse_expression()
            # optional semicolon before block
            if self.peek() and self.peek()[0] == ';':
                self.consume(';')
            self.consume('{')
            block = self.parse_block()
            return WhileNode(cond, block)

        elif tok[0] == 'var_kw':
            self.consume('var_kw')                 # consume 'var' keyword
            var_name_tok = self.consume('var')     # consume variable identifier
            var_name = var_name_tok[1]
            expr = None
            if self.peek() and self.peek()[0] == '=':
                self.consume('=')
                expr = self.parse_expression()
            self.consume(';')
            return VarDeclNode(var_name, expr)
        
        elif tok[0] == 'hvar_kw':
            self.consume('hvar_kw')                 # consume 'hvar' keyword
            var_name_tok = self.consume('var')     # consume hypervariable identifier
            var_name = var_name_tok[1]
            dependencies = []
            while self.peek() and self.peek()[0] == 'var':
                dep_tok = self.consume('var')
                dependencies.append(dep_tok[1])
            self.consume('=')
            expr = self.parse_expression()
            self.consume(';')
            return HyperVarDeclNode(var_name, dependencies, expr)
        else:
            expr = self.parse_expression()
            self.consume(';')
            return ExprStmtNode(expr)

    def parse_block(self):
        stmts = []
        while self.peek() and self.peek()[0] != '}':
            stmts.append(self.parse_statement())
        self.consume('}')
        return stmts

    def parse_expression(self):
        expr_tokens = []
        while self.peek() and self.peek()[0] not in [';', '{', '}']:
            expr_tokens.append(self.consume())
        return ExprNode(dijkstraShuntingYard(expr_tokens))
    
tokens_example = [
    ('out', None), ('var', 'y'), (';', None),
    ('out', None), ('int', 4), (';', None),
    ('out', None), ('var', 'tree'), (';', None),
    ('if', None), ('var', 'tree'), ('>', None), ('int', 4), (';', None), ('{', None),
        ('out', None), ('var', 'x'), (';', None),
        ('out', None), ('var', 'y'), (';', None),
    ('}', None),
    ('var', 'x'), ('=', None), ('int', 5), (';', None),
    ('var', 'y'), ('=', None), ('var', 'x'), ('+', None), ('int', 1), (';', None),
    ('out', None), ('var', 'y'), (';', None)
]

#parser = ParserNodes(tokens_example)
#ast_nodes = parser.parse_program()

#for node in ast_nodes:
    #print(node)
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
        if isinstance(node, OutNode):
            val = self.eval_expr(node.expr)
            print(val)
        elif isinstance(node, VarDeclNode):
            if node.expr:
                val = self.eval_expr(node.expr)
                self.update_ancestors(node)
            else:
                val = None
            self.env[node.name] = val
        elif isinstance(node, ExprStmtNode):
            self.eval_expr(node.expr)
        elif isinstance(node, IfNode):
            cond_val = self.eval_expr(node.condition)
            if cond_val:
                self.exec_nodes(node.block)
        elif isinstance(node, HyperVarDeclNode):
            if node.expr:
                ex = node.expr
            else:
                ex = None
            self.hyperenv[node.name] = ex
            self.hyperdeps[node.name] = node.dependencies
            self.hyperGraph.addNode(HyperNode(node.name, ex))
            for dep in node.dependencies:
                self.hyperGraph.addEdgeFromXToY(node.name, dep)
        
            
        else:
            raise Exception(f"Unknown node type: {node}")
       
 

"""

class Interpreter:
    def __init__(self):
        self.variables = {}

    def run(self, nodes):
        for node in nodes:
            self.execute(node)

    def execute(self, node):
        if isinstance(node, ExprStmtNode):
            evaluate_rpn(node.expr.rpn, self.variables)

        elif isinstance(node, VarDeclNode):
            value = evaluate_rpn(node.expr.rpn, self.variables) if node.expr else None
            self.variables[node.name] = value

        elif isinstance(node, OutNode):
            value = evaluate_rpn(node.expr.rpn, self.variables)
            print(value)

        elif isinstance(node, IfNode):
            cond = evaluate_rpn(node.cond.rpn, self.variables)
            if cond:
                for stmt in node.block:
                    self.execute(stmt)

        elif isinstance(node, WhileNode):
            while evaluate_rpn(node.cond.rpn, self.variables):
                for stmt in node.block:
                    self.execute(stmt)
                    
"""