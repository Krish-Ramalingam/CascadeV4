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
        pass 
    
class Eater:
    def __init__(self):
        pass

    def eatIf(self):
        pass