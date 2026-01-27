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

    def getType(tok):
        if tok[0] in ["var", "int", "float"]:
            return "dat"
        elif tok[0] in precedence:
            return "op"
        else:
            return "error"
        
    
    
    
    
    def peek(stack):
        return stack[len(stack)-1]
    
    def getPrecedence(op):
        return precedence[op] if op in precedence else False
    
    def attemptToOpStack(token):
        beneathOperation = peek(opstack)
        lastprec = getPrecedence(beneathOperation)
        currprec = getPrecedence(token)
        if currprec == False:
            return "error"
        if currPrec



    datstack = []
    opstack = []
    retstack = []

    # simplified, need to add some extra token analysis
    for tok in tokens:
        t = getType(tok)
        if t == "data":
            datstack.apend(tok)
        if t == "op":
            attemptToOpStack
            
    
    
