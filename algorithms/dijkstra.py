def dijkstraShuntingYard(tokens):
    precedence = {
        "-": 1,
        "+": 2,
        "*": 3,
        "/": 4,
        "^": 5,
        "(": 6,
        ")": 7
    }
    
    def getPrecendence(op):
        return precedence[op] if op in precedence else 0
    
    def getType(tok):
        if tok[0] in ["var", "int", "float"]:
            return "data"
        elif tok[0] in precedence:
            return "op"
        else:
            return "error"
        
    def peek(stack):
        return stack[len(stack)-1]

        
    def opStackLogic(op):
        currprec = getPrecendence(op)
        topprec = getPrecendence(peek(opstack))
    
    
    
    datstack = []
    opstack = []
    retstack = []

    # simplified, need to add some extra token analysis
    for tok in tokens:
        t = getType(tok)
        if t == "data":
            datstack = tok
        if t == "op":
            
    