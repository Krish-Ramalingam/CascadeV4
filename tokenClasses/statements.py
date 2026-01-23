class Statement:
    def __init__(self, content):
        self._content = content
        
    def getContent(self):
        return self._content
    
    def setContent(self, content):
        self._content = content
        
class ExpressionStatement(Statement):
    def __init__(self, content):
        super().__init__(content)
        
class DeclarationStatement(Statement):
    def __init__(self, content):
        super().__init__(content)
        
class ReturnStatement(Statement):
    def __init__(self, content):
        super().__init__(content)

class IfStatement(Statement):
    def __init__(self, content):
        super().__init__(content)
        
class WhileStatement(Statement):
    def __init__(self, content):
        super().__init__(content)
        
class ForStatement(Statement):
    def __init__(self, content):
        super().__init__(content)
        
class BreakStatement(Statement):
    def __init__(self, content):
        super().__init__(content)
    
