import os
#from validation import validateTokens as vt

class LineLexer:
    def __init__(self):
        self._line = ""
        self._finalTokens = []
        self._mode = None
        self._tempTokens = []
        self.commentsOn = False
        
    def loadLine(self, line: str):
        self._line = ""
        self._finalTokens = []
        self._mode = None
        self._tempTokens = []
        if not isinstance(line, str):
            raise TypeError("Line must be a string")
        
        if "-----<" in line or "----->" in line:
            self.commentsOn = not self.commentsOn
            self._line = ""
        elif "//" in line and not self.commentsOn:
            self._line = line.split("//")[0].strip()  # Remove comments
        elif not self.commentsOn:
            self._line = line.strip()
        elif self.commentsOn:
            self._line = ""
        
     
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
            if '.' in current_number:
                tokens.append(("float", float(current_number)))
            else:
                tokens.append(("int", int(current_number)))
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
                case "hvar":
                    self._mode = "hassign"
                case "for":
                    self._mode = "for"
                case _:
                    self._mode = "control"
                
            if len(self._tempTokens) == 1 and self._tempTokens[0] != "}":
                self._mode = "shortOut"
            if "=" in self._tempTokens and self._mode == "control":
                self._mode = "shortAssign"
            if ":=" in self._tempTokens and self._mode == "control":
                self._mode = "shortHyperAssign"
        else:
            self._mode = "empty"
            
    
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
                case "hassign":
                    self.tokenizeHyperAssignment()
                case "for":
                    self.tokenizeFor()
                case "shortOut":
                    self.tokenizeShortOutput()
                case "shortAssign":
                    self.tokenizeShortAssignment()
                case "shortHyperAssign":
                    self.tokenizeShortHyperAssign()
                case "empty":
                    pass
        
        return self.getFinalTokens()
    
    def tokenizeHyperAssignment(self):
        # expression in the form hvar varName ( x y ... z ) = expression
        self._finalTokens.append(("hvar_kw", None))
        self._finalTokens.append(("var", self._tempTokens[1]))
        for i in range(2, self._tempTokens.index('=')):
            if self._tempTokens[i] != '(' and self._tempTokens[i] != ')':
                if "(" in self._tempTokens[i]:
                    self._tempTokens[i] = self._tempTokens[i].replace("(", "")
                if ")" in self._tempTokens[i]:
                    self._tempTokens[i] = self._tempTokens[i].replace(")", "")
                self._finalTokens.append(("var", self._tempTokens[i]))
        self._finalTokens.append(("=", None))
        expression = " ".join(self._tempTokens[self._tempTokens.index('=')+1:])
        new_expr = self.concatenateShorthandMultiply(expression)
        tokenizedExpr = self.tokeniseArithmeticExpression(new_expr)
        if tokenizedExpr:
            self._finalTokens.extend(tokenizedExpr)
            self._finalTokens.append((";", None))
    
             
    def tokenizeAssignment(self):
        # expression in the form var varName = expression
        self._finalTokens.append(("var_kw", None))
        self._finalTokens.append(("var", self._tempTokens[1]))
        self._finalTokens.append(("=", None))
        expression = " ".join(self._tempTokens[3:])
        new_expr = self.concatenateShorthandMultiply(expression)
        tokenizedExpr = self.tokeniseArithmeticExpression(new_expr)
        if tokenizedExpr:
            self._finalTokens.extend(tokenizedExpr)
            self._finalTokens.append((";", None))
            
            
    def tokenizeOutput(self):
        # expression in the form out expression
        expression = " ".join(self._tempTokens[1:])
        new_expr = self.concatenateShorthandMultiply(expression)
        tokenisedExpr = self.tokeniseArithmeticExpression(new_expr)
        self._finalTokens.append(("out", None))
        self._finalTokens.extend(tokenisedExpr)
        self._finalTokens.append((";", None))  # Add newline token after output expression
        
    def tokenizeInput(self):
        # expression in the form inp varName
        tokenisedExpr = self.tokeniseArithmeticExpression(self._tempTokens[1])
        self._finalTokens.append(("inp", None))
        self._finalTokens.extend(tokenisedExpr)
        self._finalTokens.append((";", None))

    def tokenizeControl(self):
        # expression in the form key (condition) { ... }
        controlKey = self._tempTokens[0]
        conditionEnd = self._tempTokens.index('{')
        condition = " ".join(self._tempTokens[1:conditionEnd])
        self._finalTokens.append((controlKey, None))
        new_condition = self.concatenateShorthandMultiply(condition)
        tokenizedCondition = self.tokeniseLogicalExpression(new_condition)
        self._finalTokens.extend(tokenizedCondition)
        # The rest can be handled as needed (e.g., body of control structure)
        self._finalTokens.append((";", None))
        self._finalTokens.append(("{", None))

    def tokenizeFor(self):
        # expression in the form for varName in start..end { ... }
        #print(self._tempTokens)
        self._finalTokens.append(("for_kw", None))
        self._finalTokens.append(("var", self._tempTokens[1]))
        self._finalTokens.append(("in_kw", None))
        rangeStart = self._tempTokens[3][0:self._tempTokens[3].index('..')]
        rangeEnd = self._tempTokens[3][self._tempTokens[3].index('..')+2:]
        self._finalTokens.append(("int", rangeStart))
        self._finalTokens.append(("range_sep", None))
        self._finalTokens.append(("int", rangeEnd))
        # The rest can be handled as needed (e.g., body of for loop)
        self._finalTokens.append((";", None))
        self._finalTokens.append(("{", None))
        
    def tokenizeShortOutput(self):
        # used as a shorthand for outputting a single variable, e.g. "x" instead of "out x"
        self._finalTokens.append(("out", None))
        self._finalTokens.append(("var", self._tempTokens[0]))
        self._finalTokens.append((";", None))
        
    def tokenizeShortAssignment(self):
        self._finalTokens.append(("var_kw", None))
        self._finalTokens.append(("var", self._tempTokens[0]))
        self._finalTokens.append(("=", None))
        expression = " ".join(self._tempTokens[2:])
        new_expr = self.concatenateShorthandMultiply(expression)
        tokenizedExpr = self.tokeniseArithmeticExpression(new_expr)
        if tokenizedExpr:
            self._finalTokens.extend(tokenizedExpr)
            self._finalTokens.append((";", None))
            
    def tokenizeShortHyperAssign(self):
        self._finalTokens.append(("hvar_kw", None))
        self._finalTokens.append(("var", self._tempTokens[0]))
        for i in range(1, self._tempTokens.index(':=')):
            if self._tempTokens[i] != '(' and self._tempTokens[i] != ')':
                print(self._tempTokens[i])
                if "(" in self._tempTokens[i]:
                    self._tempTokens[i] = self._tempTokens[i].replace("(", "")
                if ")" in self._tempTokens[i]:
                    self._tempTokens[i] = self._tempTokens[i].replace(")", "")
                self._finalTokens.append(("var", self._tempTokens[i]))
        self._finalTokens.append(("=", None))
        expression = " ".join(self._tempTokens[self._tempTokens.index(':=')+1:])
        new_expr = self.concatenateShorthandMultiply(expression)
        tokenizedExpr = self.tokeniseArithmeticExpression(new_expr)
        if tokenizedExpr:
            self._finalTokens.extend(tokenizedExpr)
            self._finalTokens.append((";", None))
            
    def concatenateShorthandMultiply(self, expr):
        # This function is used to handle cases where multiplication is implied, e.g. "2x"
        # Expression is in string form, e.g. "2x + 3y" or "2(x + 1)"
        print(expr)
        new_expr = ""
        for i in range(len(expr)):
            if i < len(expr) - 1:
                    if (expr[i].isdigit() or expr[i] == ')') and (expr[i+1].isalpha() or expr[i+1] == '('):
                        new_expr += expr[i] + '*'  # Insert multiplication operator
                    else:
                        new_expr += expr[i]
        new_expr += expr[i]
        print(new_expr)
        return new_expr
                
        
        
        
        
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
    
"""
def genTokStream(filename):
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, filename) 
    myLexer = Lexer()
    tokenStream = myLexer.lexFile(file_path)
    return tokenStream


script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, "cascade.txt") 
myLexer = Lexer()
tokenStream = myLexer.lexFile(file_path)
for t in tokenStream:
    if t[1] == None:
        print(t[0])
    else:
        print(t[0], t[1])

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