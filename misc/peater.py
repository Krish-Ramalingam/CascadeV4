from tokenClasses import conditionalstatements





tokens = [
    ("start", None),
    ("if", None),
    ("var", "x"),
    ("==", None),
    ("int", 5),
    (";", None),
    ("{", None),
    ("var", "y"),
    ("=", None),
    ("int", 10),
    (";", None),
    ("}", None)
]



class UnaryNode:
    def __init__(self, name, value=None):
        self._name = name
        self._value = value
        self._child = None

    def getChild(self):
        return self._child

    def setChild(self, node):
        self._child = node
        
        
        
class StartNode(UnaryNode):
    def __init__(self):
        super().__init__("START")
    
class IfNode():
    def __init__(self, condition, body, rest):
        self._condition = condition
        self._body = body
        self._else = rest
        
class VarNode():
    def __init__(self, name):
        self._name = name
        self.value


class BinNode:
    def __init__(self, name, value=None):
        self._name = name
        self._value = value
        self._right = None
        self._left = None

    def getRight(self):
        return self._right

    def getLeft(self):
        return self._left

    def setRight(self, node):
        self._right = node

    def setLeft(self, node):
        self._left = node



class Eater:
    def __init__(self):
        pass


    def advance(self):
        self.tokPosition += 1
        self._currentToken = self._tokenStream[self.tokPosition]
        
        
    def eatIf(self):
        if self._currentToken[0] == "if":
            self.advance()
        else:
            raise SyntaxError("Expected 'if' keyword")
    
class Parser:
    def __init__(self, tokenStream):
        self._tokenStream = tokenStream
        self.tokPosition = 0
        self._currentToken = self._tokenStream[self.tokPosition]
        
    def nextToken(self):
        self.tokPosition += 1
        self._currentToken = self._tokenStream[self.tokPosition]
    
    def peekToken(self):
        return self._tokenStream[self.tokPosition + 1]
    
    def parse(self):
        #this is where the main parsing will happen, it will call other functions to parse different types of statements and expressions pass
        if self._currentToken[0] == "start":
            self.nextToken()
        if self._currentToken[0] == "if":
            self.eatIf() 
        if self._currentToken[0] == "var":
            
        

class ProgramAST:
    def __init__(self):
        self._head = Node("START")
        
    def getHead(self):
        return self._head
    
    def setHead(self, node):
        self._head = node
    
    
    