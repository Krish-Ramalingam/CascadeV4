line1 = "out x // This is an output statement"
line2 = "var x = 1 + 2 * (3 - 4)"
line3 = "var y = 3.3"
line4 = "inp y"
line5 = "if ( x > 0 ) {"

class LineLexer:
    def __init__(self):
        self._line = ""
        self._finalTokens = []
        self._mode = None
        self._tempTokens = []
        
    def loadLine(self, line: str):
        self._line = ""
        self._finalTokens = []
        self._mode = None
        self._tempTokens = []
        if not isinstance(line, str):
            raise TypeError("Line must be a string")
        if "//" in line:
            self._line = line.split("//")[0].strip()  # Remove comments
        else:
            self._line = line.strip()
    
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
    
    def tokeniseArithmeticExpression(expr):
        """
        Tokenises a simple arithmetic expression into numbers and operators and variables.
        Args:
            expr (str): The arithmetic expression as a string.
        Returns:
            list: A list of tokens (numbers and operators).
        """
        tokens = []
        current_number = ''
        current_variable = ''
        
        for char in expr:
            if char.isdigit() or char == '.':
                current_number += char
            else:
                if current_number:
                    if '.' in current_number:
                        tokens.append(("float", float(current_number)))
                    else:
                        tokens.append(("int", int(current_number)))
                    current_number = ''
                if char in '+-*/()':
                    tokens.append((char, None))
                else:
                    if char.isalpha():
                        current_variable += char
                    else:
                        if current_variable:
                            tokens.append(("var", current_variable))
                            current_variable = ''
                            
        if current_number:
            tokens.append(("float", float(current_number)))
        if current_variable:
            tokens.append(("var", current_variable))

        return tokens
        
        
    def tokeniseLogicalExpression(expr):
        """
        Tokenises a logical expression into variables, operators, and parentheses.
        Args:
            expr (str): The logical expression as a string.
        Returns:
            list: A list of tokens (variables and operators).
        """
        tokens = []
        current_variable = ''
        
        i = 0
        while i < len(expr):
            char = expr[i]
            if char.isalpha():
                current_variable += char
            else:
                if current_variable:
                    tokens.append(("var", current_variable))
                    current_variable = ''
                if expr[i:i+2] in ['&&', '||', '==', '!=', '<=', '>=']:
                    tokens.append((expr[i:i+2], None))
                    i += 1
                elif char in '!<>()':
                    tokens.append((char, None))
            i += 1

        if current_variable:
            tokens.append(("var", current_variable))

        return tokens
        
    def modeInitialise(self):
        self._tempTokens = self._line.split()  # Simple whitespace tokenizer    
        match self._tempTokens[0]:
            case "var":
                self._mode = "assign"
            case "out":
                self._mode = "output"
            case "inp":
                self._mode = "input"
            case _:
                self._mode = "control"

                
            
            
            
            
            
    def variablesInExpression(self, expression: str):
        variablesInExpr = False
        for x in expression:
            if type(x) == str:
                variablesInExpr = True
        return variablesInExpr
    
    def tokeniseExpression(self, expression: str):
        if self.variablesInExpression(expression):
            return self.tokeniseVariablesInExpression(expression)
        else:
            return self.tokeniseArithmeticExpression(expression)
            
    def tokeniseArithmeticExpression(self, expression: str):
        pass

    def tokeniseVariablesInExpression(self, expression: str):
        pass
    
    def tokenize(self):
        match self._mode:
            case None:
                self.modeInitialise()
                self.tokenize()
                self._mode = None  # Reset mode after tokenization  
            case "assign":
                self.tokenizeAssignment()
            case "output":
                self.tokenizeOutput()
            case "input":
                self.tokenizeInput()
            case "control":
                self.tokenizeControl()
                
            
        
    def tokenizeAssignment(self):
        self._finalTokens.append(("var", self._tempTokens[1]))
        self._finalTokens.append(("=", None))
        expression = " ".join(self._tempTokens[3:])
        self._finalTokens.append(("expr", expression))
    
    def tokenizeOutput(self):
        expression = " ".join(self._tempTokens[1:])
        self._finalTokens.append(("out", expression))
        
    def tokenizeInput(self):
        self._finalTokens.append(("inp", self._tempTokens[1]))

    def tokenizeControl(self):
        # expression in the form key (condition) { ... }
        controlKey = self._tempTokens[0]
        print(self._tempTokens)
        conditionStart = self._tempTokens.index('(')
        conditionEnd = self._tempTokens.index(')')
        condition = " ".join(self._tempTokens[conditionStart + 1:conditionEnd])
        self._finalTokens.append((controlKey, condition))
        # The rest can be handled as needed (e.g., body of control structure)
        self._finalTokens.append(("{", None))

mylexer = LineLexer()
mylexer.loadLine(line1)
mylexer.tokenize()
print(mylexer.getFinalTokens())
mylexer.loadLine(line2)
mylexer.tokenize()
print(mylexer.getFinalTokens())
mylexer.loadLine(line5)
mylexer.tokenize()
print(mylexer.getFinalTokens())