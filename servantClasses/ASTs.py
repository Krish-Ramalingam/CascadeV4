class Parser:
    pass

class ASTNode:
    def __init__(self, value):
        self._value = value

class AST:
    def __init__(self):
        self._root = None
        
    def getRoot(self):
        return self._root
    
    def setRoot(self, root):
        self._root = root
        
    def traverse(self):
        pass
    
    