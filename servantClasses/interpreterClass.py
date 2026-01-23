class Interpreter:
    def __init__(self, sourceCode):
        self._sourceCode = sourceCode
        self._lineNumber = 0
        self._numErrors = 0
        self._errors = []
    
    def raiseError(self, message):
        self._numErrors += 1
        self._errors.append(f"Error at line {self._lineNumber + 1}: {message}")
  
    def incrementLineNumber(self):
        self._lineNumber += 1
    
    def getErrors(self):
        return self._errors
    
    def getNumErrors(self):
        return self._numErrors
    
    def jumpToLineNumber(self, lineNumber):
        self._lineNumber = lineNumber
        
    def getSourceCode(self):
        return self._sourceCode
    
    def getLineNumber(self):
        return self._lineNumber
    
    def setLineNumber(self, lineNumber):
        self._lineNumber = lineNumber
        
    def setSourceCode(self, sourceCode):
        self._sourceCode = sourceCode
        
    
    
    
    def interpret(self, statements):
        pass
    
    


