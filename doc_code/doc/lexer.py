import os
#from validation import validateTokens as vt


class LineLexer:
    """
    Single-line lexer responsible for tokenising one line of source code at a time.
    
    Manages comment stripping, mode detection, and dispatching to the appropriate
    tokenizer method for each statement type. Intended to be used directly for
    line-by-line processing, or via the Lexer subclass for multi-line / file input.
    
    Token format throughout: (type: str, value: any)
    e.g. ("int", 42), ("var", "x"), ("+", None), ("var_kw", None)
    """
    
    def __init__(self):
        self._line = ""             # the current source line being processed
        self._finalTokens = []      # accumulated tokens for the current line
        self._mode = None           # tokenizer mode, resolved in modeInitialise()
        self._tempTokens = []       # whitespace-split words, used for mode dispatch
        self.commentsOn = False     # tracks whether we're inside a block comment
        
    def loadLine(self, line: str):
        """
        Prepare a new source line for tokenisation.
        
        Handles three comment styles before storing the usable content:
          - Block comments:  delimited by '-----<' (open) and '----->' (close).
                             Toggling commentsOn suppresses all enclosed lines.
          - Inline comments: '// ...' strips everything from the marker to end of line.
          - Normal lines:    stripped of surrounding whitespace and stored as-is.
          
        Resets all per-line state so the instance can be reused across lines.
        """
        # Reset per-line state before processing the new input
        self._line = ""
        self._finalTokens = []
        self._mode = None
        self._tempTokens = []
        if not isinstance(line, str):
            raise TypeError("Line must be a string")
        
        if "-----<" in line or "----->" in line:
            # Block comment boundary — flip the toggle and produce no tokens
            self.commentsOn = not self.commentsOn
            self._line = ""
        elif "//" in line and not self.commentsOn:
            # Inline comment — keep only the code that precedes the marker
            self._line = line.split("//")[0].strip()  # Remove comments
        elif not self.commentsOn:
            self._line = line.strip()
        elif self.commentsOn:
            # Inside a block comment — discard the entire line
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
                # Accumulate digit/decimal characters to form a full numeric literal
                current_number += char
            else:
                if current_number:
                    # Flush the buffered number — decide int vs float by presence of '.'
                    if '.' in current_number:
                        tokens.append(("float", float(current_number)))
                    else:
                        tokens.append(("int", int(current_number)))
                    current_number = ''
                if char in '+-*/()^':
                    tokens.append((char, None))
                else:
                    if char.isalpha():
                        # Accumulate alphabetic characters into a variable name
                        current_variable += char
                    else:
                        if current_variable:
                            # Flush the buffered variable name on any non-alpha character
                            tokens.append(("var", current_variable))
                            current_variable = ''
                            
        # Flush any remaining number or variable that was still buffered at end of string
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
                # Non-alphanumeric character — flush any buffered variable or number first
                if current_number:
                    tokens.append(("int", int(current_number)))
                    current_number = ''
                if current_variable:
                    tokens.append(("var", current_variable))
                    current_variable = ''
                # Check for two-character operators before falling back to single-char
                if expr[i:i+2] in ['&&', '||', '==', '!=', '<=', '>=']:
                    tokens.append((expr[i:i+2], None))
                    i += 1  # skip the second character of the two-char operator
                elif char in '!<>()+-*/':
                    tokens.append((char, None))
            i += 1

        # Flush any variable or number still in the buffer at end of string
        if current_variable:
            tokens.append(("var", current_variable))
        if current_number:
            tokens.append(("int", int(current_number)))
                

        return tokens
        
    def modeInitialise(self):
        """
        Determine the tokenization mode for the current line by inspecting the
        first whitespace-delimited token.
        
        Mode assignments:
          assign          — standard variable declaration:  var x = ...
          output          — output statement:               out ...
          input           — input statement:                inp x
          hassign         — hypervariable declaration:      hvar z (x y) = ...
          for             — range-based for loop:           for x in 1..10 {
          control         — if/while/other control flow:    if (cond) {
          shortOut        — single-token line treated as an implicit output:  x
          shortAssign     — assignment without 'var' keyword:  x = ...
          shortHyperAssign— hypervariable shorthand:           z := ...
          empty           — blank or whitespace-only line
        """
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
                
            # A single non-'}' token with no keyword is treated as shorthand output
            if len(self._tempTokens) == 1 and self._tempTokens[0] != "}":
                self._mode = "shortOut"
            # '=' in a non-keyword line signals a shorthand assignment
            if "=" in self._tempTokens and self._mode == "control":
                self._mode = "shortAssign"
            # ':=' signals a shorthand hypervariable assignment
            if ":=" in self._tempTokens and self._mode == "control":
                self._mode = "shortHyperAssign"
        else:
            self._mode = "empty"
            
    
    def tokenize(self):
        """
        Main tokenization entry point for the current line.
        
        On the first call (mode is None), runs modeInitialise() to determine the
        correct tokenizer, then recurses once with the mode set. After the recursive
        call returns the mode is cleared so the next loadLine() starts fresh.
        
        Returns the final token list for the current line.
        """
        if len(self._line) == 0:
            pass
        if self._line.isspace():
            pass
        if self._line == "}":
            # Closing brace is a standalone structural token — no mode needed
            self._finalTokens.append(("}", None))
        else:
            match self._mode:
                case None:
                    # First call — resolve mode then re-enter
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
        """
        Tokenise a full hypervariable declaration.
        Expected form:  hvar varName ( dep1 dep2 ... ) = expression
        
        Dependency names between 'hvar varName' and '=' are emitted as ("var", name).
        Parentheses around the dependency list are stripped before emitting.
        The RHS expression is run through concatenateShorthandMultiply then
        tokeniseArithmeticExpression before being appended.
        """
        self._finalTokens.append(("hvar_kw", None))
        self._finalTokens.append(("var", self._tempTokens[1]))
        for i in range(2, self._tempTokens.index('=')):
            if self._tempTokens[i] != '(' and self._tempTokens[i] != ')':
                # Strip any parentheses that are attached to the token rather than
                # separated by whitespace (e.g. "(x" or "y)")
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
        """
        Tokenise a standard variable declaration.
        Expected form:  var varName = expression
        
        Emits: var_kw, var name, '=', expression tokens, ';'
        """
        self._finalTokens.append(("var_kw", None))
        self._finalTokens.append(("var", self._tempTokens[1]))
        self._finalTokens.append(("=", None))
        # Everything after 'var name =' is the RHS expression
        expression = " ".join(self._tempTokens[3:])
        new_expr = self.concatenateShorthandMultiply(expression)
        tokenizedExpr = self.tokeniseArithmeticExpression(new_expr)
        if tokenizedExpr:
            self._finalTokens.extend(tokenizedExpr)
            self._finalTokens.append((";", None))
            
            
    def tokenizeOutput(self):
        """
        Tokenise an output statement.
        Expected form:  out expression
        
        Emits: 'out', expression tokens, ';'
        Note: the trailing ';' serves as a statement boundary for the parser.
        """
        expression = " ".join(self._tempTokens[1:])
        new_expr = self.concatenateShorthandMultiply(expression)
        tokenisedExpr = self.tokeniseArithmeticExpression(new_expr)
        self._finalTokens.append(("out", None))
        self._finalTokens.extend(tokenisedExpr)
        self._finalTokens.append((";", None))  # Add newline token after output expression
        
    def tokenizeInput(self):
        """
        Tokenise an input statement.
        Expected form:  inp varName
        
        Emits: 'inp', var token, ';'
        """
        tokenisedExpr = self.tokeniseArithmeticExpression(self._tempTokens[1])
        self._finalTokens.append(("inp", None))
        self._finalTokens.extend(tokenisedExpr)
        self._finalTokens.append((";", None))

    def tokenizeControl(self):
        """
        Tokenise a control-flow statement (if, while, etc.).
        Expected form:  keyword condition {
        
        The condition spans from token[1] up to (but not including) the '{' token.
        Emits: keyword, condition tokens (logical), ';', '{'
        
        The ';' is injected as a separator so the parser can cleanly delimit
        the condition from the block opener.
        """
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
        """
        Tokenise a range-based for-loop header.
        Expected form:  for varName in start..end {
        
        The range string (e.g. "1..10") is split on '..' to extract start and end.
        Emits: for_kw, var name, in_kw, int start, range_sep, int end, ';', '{'
        """
        #print(self._tempTokens)
        self._finalTokens.append(("for_kw", None))
        self._finalTokens.append(("var", self._tempTokens[1]))
        self._finalTokens.append(("in_kw", None))
        # Split "start..end" on the range separator to get the two bounds
        rangeStart = self._tempTokens[3][0:self._tempTokens[3].index('..')]
        rangeEnd = self._tempTokens[3][self._tempTokens[3].index('..')+2:]
        self._finalTokens.append(("int", rangeStart))
        self._finalTokens.append(("range_sep", None))
        self._finalTokens.append(("int", rangeEnd))
        # The rest can be handled as needed (e.g., body of for loop)
        self._finalTokens.append((";", None))
        self._finalTokens.append(("{", None))
        
    def tokenizeShortOutput(self):
        """
        Shorthand output: a bare variable name on its own line implicitly prints it.
        e.g.  x   →   out x;
        
        Emits: 'out', var token, ';'
        """
        self._finalTokens.append(("out", None))
        self._finalTokens.append(("var", self._tempTokens[0]))
        self._finalTokens.append((";", None))
        
    def tokenizeShortAssignment(self):
        """
        Shorthand assignment — omits the 'var' keyword.
        Expected form:  varName = expression
        
        Emits: var_kw, var name, '=', expression tokens, ';'
        Semantically identical to a full var declaration; the keyword is injected
        so the parser doesn't need a separate code path.
        """
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
        """
        Shorthand hypervariable assignment — uses ':=' instead of 'hvar ... ='.
        Expected form:  varName dep1 dep2 ... := expression
        
        Dependency names between the variable and ':=' are collected and stripped
        of any attached parentheses (same logic as tokenizeHyperAssignment).
        Emits: hvar_kw, var name, dep vars..., '=', expression tokens, ';'
        """
        self._finalTokens.append(("hvar_kw", None))
        self._finalTokens.append(("var", self._tempTokens[0]))
        for i in range(1, self._tempTokens.index(':=')):
            if self._tempTokens[i] != '(' and self._tempTokens[i] != ')':
                print(self._tempTokens[i])
                # Strip parentheses that are attached to the token rather than
                # separated by whitespace
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
        """
        Pre-processes an expression string to make implied multiplication explicit.
        
        Inserts a '*' operator between a digit (or closing paren) and an alphabetic
        character (or opening paren) so the downstream arithmetic tokenizer doesn't
        need to handle juxtaposition.
        
        Examples:
            "2x"      →  "2*x"
            "3(x+1)"  →  "3*(x+1)"
            "2x + 3y" →  "2*x + 3*y"
            
        Args:
            expr (str): Raw expression string, potentially containing implied products.
        Returns:
            str: Expression string with explicit '*' operators inserted.
        """
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
    """
    Full-program lexer built on top of LineLexer.
    
    Provides convenience methods for lexing a list of lines, a file on disk,
    or a raw multi-line string. All methods return a single flat token list
    suitable for passing directly to the parser.
    """
    def __init__(self):
        super().__init__()
        
    def lexAll(self, lines: list):
        """
        Lex a pre-split list of source lines.
        
        Args:
            lines (list[str]): Source lines (newlines may or may not be present).
        Returns:
            list: Flat token list for the entire input.
        """
        allTokens = []
        for line in lines:
            self.loadLine(line)
            tokens = self.tokenize()
            allTokens.extend(tokens)
        return allTokens
    
    def lexFile(self, filepath: str):
        """
        Lex a source file from disk.
        
        Opens the file, reads all lines, and processes them in order.
        The file is closed automatically after reading.
        
        Args:
            filepath (str): Absolute or relative path to the source file.
        Returns:
            list: Flat token list for the entire file.
        """
        allTokens = []
        with open(filepath, 'r') as file:
            lines = file.readlines()
            for line in lines:
                self.loadLine(line)
                tokens = self.tokenize()
                allTokens.extend(tokens)
        return allTokens
    
    def lexString(self, codeString: str):
        """
        Lex a raw multi-line source string (e.g. from a REPL or test fixture).
        
        Splits on newlines before processing — each resulting substring is treated
        as a single source line, consistent with lexAll and lexFile behaviour.
        
        Args:
            codeString (str): Multi-line source code as a single string.
        Returns:
            list: Flat token list for the entire input.
        """
        allTokens = []
        lines = codeString.split('\n')
        for line in lines:
            self.loadLine(line)
            tokens = self.tokenize()
            allTokens.extend(tokens)
        return allTokens