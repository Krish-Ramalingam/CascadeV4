class Hypervariable:
    def __init__(self, name, relations, expression):
        self._name = name
        self._relations = relations
        self._expression = expression
        
    def getName(self):
        return self._name
    
    def getRelations(self):
        return self._relations

    def getExpression(self):
        return self._expression
    
    def checkExpressionMatchesRelations(self):
        pass
    
    def evaluate(self):
        pass

    def checkRelations(self):
        pass

    def updateRelations(self):
        pass
    
    