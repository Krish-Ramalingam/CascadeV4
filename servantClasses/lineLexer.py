line1 = "out x"
line2 = "var x = 1 + 2 * (3 - 4)"
line3 = "var y = 3.3"
line4 = "inp y"

class LineLexer:
    def __init__(self, line: str):
        self._line = line
        self._finalTokens = []
        self._mode = None
        self._tempTokens = []
        
    def getFinalTokens(self):
        return self._finalTokens
    
    def setLine(self, line: str):
        self._line = line
        
    def getLine(self):
        return self._line
    
    def getMode(self):
        return self._mode
    
    def setMode(self, mode: str):
        self._mode = mode
    
        
    def modeInitialise(self):
        self._tempTokens = self._line.split()  # Simple whitespace tokenizer
        if self._tempTokens[0] == "var":
            self._mode = "assign"
        elif self._tempTokens[0] == "out":
            self._mode = "output"
        elif self._tempTokens[0] == "inp":
            self._mode = "input"
        elif self._tempTokens[0] == "eval":
            self._mode = "evaluation"
        else:
            self._mode = None
    
    def tokeniseExpression(self, expression: str):
        stack = []
        
    
    def tokenize(self):
        if self._mode is None:
            self.modeInitialise()
        if self._mode == "assign":
            self.tokenizeAssignment()
        elif self._mode == "output":
            self.tokenizeOutput()
        elif self._mode == "input":
            self.tokenizeInput()
        elif self._mode == "evaluation":
            self.tokenizeEvaluation()
        
    def tokenizeAssignment(self):
        self._finalTokens.append(("var", None))
        self._finalTokens.append(("id", self._tempTokens[1]))
        self._finalTokens.append(("eq", None))
        expression = " ".join(self._tempTokens[3:])
        self._finalTokens.append(("expr", expression))
    
    def tokenizeOutput(self):
        self._finalTokens.append(("out", None))
        expression = " ".join(self._tempTokens[1:])
        self._finalTokens.append(("expr", expression))
        
    def tokenizeInput(self):
        self._finalTokens.append(("inp", None))
        self._finalTokens.append(("id", self._tempTokens[1]))

    def tokenizeEvaluation(self):
        self._finalTokens.append(("eval", None))
        expression = " ".join(self._tempTokens[1:])
        self._finalTokens.append(("expr", expression))

mylexer = LineLexer(line2)
mylexer.tokenize()
print(mylexer.getFinalTokens())
mylexer2 = LineLexer(line1)
mylexer2.tokenize()
print(mylexer2.getFinalTokens())
