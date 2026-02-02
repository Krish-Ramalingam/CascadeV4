import os


line1 = "out x // This is an output statement"
line2 = "var x = 1 + 2 * (3 - 4)"
line3 = "var y = 3.3"
line4 = "inp y"
line5 = "if x > (y + 1) {"
line6 = "out (x + y) // Output sum"
line7 = "}"


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
    
    def tokeniseArithmeticExpression(self, expr):
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
                if char in '+-*/()^':
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
           
    def tokeniseLogicalExpression(self, expr):
        """
        Tokenises a logical expression into variables, operators, and parentheses.
        Args:
            expr (str): The logical expression as a string.
        Returns:
            list: A list of tokens (variables and operators).
        """
        tokens = []
        current_variable = ''
        current_number = ''
        i = 0
        while i < len(expr):
            char = expr[i]
            if char.isspace():
                i += 1
                continue
            elif char.isdigit():
                current_number += char
            elif char.isalpha():
                current_variable += char
            else:
                if current_number:
                    tokens.append(("int", int(current_number)))
                    current_number = ''
                if current_variable:
                    tokens.append(("var", current_variable))
                    current_variable = ''
                if expr[i:i+2] in ['&&', '||', '==', '!=', '<=', '>=']:
                    tokens.append((expr[i:i+2], None))
                    i += 1
                elif char in '!<>()+-*/':
                    tokens.append((char, None))
            i += 1

        if current_variable:
            tokens.append(("var", current_variable))
        if current_number:
            tokens.append(("int", int(current_number)))
                

        return tokens
        
    def modeInitialise(self):
        self._tempTokens = self._line.split()  # Simple whitespace tokenizer  
        if len(self._tempTokens) != 0:
            match self._tempTokens[0]:
                case "var":
                    self._mode = "assign"
                case "out":
                    self._mode = "output"
                case "inp":
                    self._mode = "input"
                case _:
                    self._mode = "control" 
        else:
            self._mode = "empty"
   
    """
    def variablesInExpression(self, expression: str):
        variablesInExpr = False
        for x in expression:
            if type(x) == str:
                if x.isalpha():
                    variablesInExpr = True
        return variablesInExpr
    
    def tokeniseExpression(self, expression: str):
        return self.tokeniseArithmeticExpression(expression)
    
        if self.variablesInExpression(expression):
            print("varin")
            return self.tokeniseVariablesInExpression(expression)
        else:
            
            return self.tokeniseArithmeticExpression(expression)

    def tokeniseVariablesInExpression(self, expression: str):
        # this is not finished...
        pass
    
    """
    def tokenize(self):
        if len(self._line) == 0:
            pass
        if self._line.isspace():
            pass
        if self._line == "}":
            self._finalTokens.append(("}", None))
        else:
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
                case "empty":
                    pass
        
        return self.getFinalTokens()
                
    def tokenizeAssignment(self):
        self._finalTokens.append(("var", self._tempTokens[1]))
        self._finalTokens.append(("=", None))
        expression = " ".join(self._tempTokens[3:])
        tokenizedExpr = self.tokeniseArithmeticExpression(expression)
        if tokenizedExpr:
            self._finalTokens.extend(tokenizedExpr)
       
    def tokenizeOutput(self):
        expression = " ".join(self._tempTokens[1:])
        self._finalTokens.append(("out", expression))
        
    def tokenizeInput(self):
        self._finalTokens.append(("inp", self._tempTokens[1]))

    def tokenizeControl(self):
        # expression in the form key (condition) { ... }
        
        controlKey = self._tempTokens[0]
        conditionEnd = self._tempTokens.index('{')
        condition = " ".join(self._tempTokens[1:conditionEnd])
        self._finalTokens.append((controlKey, None))
        tokenizedCondition = self.tokeniseLogicalExpression(condition)
        self._finalTokens.extend(tokenizedCondition)
        # The rest can be handled as needed (e.g., body of control structure)
        self._finalTokens.append(("{", None))

class Lexer(LineLexer):
    def __init__(self):
        super().__init__()
        
    def lexAll(self, lines: list):
        allTokens = []
        for line in lines:
            self.loadLine(line)
            tokens = self.tokenize()
            allTokens.extend(tokens)
        return allTokens
    
    def lexFile(self, filepath: str):
        allTokens = []
        with open(filepath, 'r') as file:
            lines = file.readlines()
            for line in lines:
                self.loadLine(line)
                tokens = self.tokenize()
                allTokens.extend(tokens)
        return allTokens
    
    def lexString(self, codeString: str):
        allTokens = []
        lines = codeString.split('\n')
        for line in lines:
            self.loadLine(line)
            tokens = self.tokenize()
            allTokens.extend(tokens)
        return allTokens
    
def genTokStream():
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, "cascading.txt") 
    myLexer = Lexer()
    tokenStream = myLexer.lexFile(file_path)
    return tokenStream


"""
script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, "cascade.txt") 
myLexer = Lexer()
tokenStream = myLexer.lexFile(file_path)
for t in tokenStream:
    if t[1] == None:
        print(t[0])
    else:
        print(t[0], t[1])
"""