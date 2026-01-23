class Lexer:
    def __init__(self, sourceCode):
        self._sourceCode = sourceCode
        self._lineNumber = 0
        self._numErrors = 0
        self._errors = []
        self._tokenQueue = []
    
    def addError(self, message):
        self._numErrors += 1
        self._errors.append(f"Error at line {self._lineNumber + 1}: {message}")
  
    def incrementLineNumber(self):
        self._lineNumber += 1
    
    def getErrors(self):
        return self._errors
    
    def getNumErrors(self):
        return self._numErrors
    
    def getTokenQueue(self):
        return self._tokenQueue
    
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
        
    def appendToTokenQueue(self, token):
        self._tokenQueue.append(token)
        
    def interpret(self, statements):
        pass
    
    

lexer1 = Lexer("print('Hello, World!')")

