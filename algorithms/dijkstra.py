def dijkstraShuntingYard(tokens):
    precedence = {
        "-": 1,
        "+": 2,
        "*": 3,
        "/": 4,
        "^": 5,
        "(": 6,
        ")": 6
    }

    def peek(stack):
        return stack[len(stack)-1]
    
    def getPrecendence(op):
        return precedence[op] if op in precedence else False
    
    def attemptToOpStack(token):
        beneathOperation = peek(opstack)
        prec = getPrecedence(beneathOperation)
        if prec = False:
            return "error"                                       #need to change to make stuff more robust



    datstack = []
    opstack = []
    
    for tok in tokens:
        if tok.isnumeric():
            datstack.append(tok)
        elif getPrecedence(tok) != False:
            attemptToOpStack()
    
    
