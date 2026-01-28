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
    
    def fileRest():
        pass
        
        
        

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
    
    def attemptToRetStack(token):
        beneathOperation = peek(opstack)
        lastprec = getPrecedence(beneathOperation)
        currprec = getPrecedence(token)
        if currprec or lastprec == False:
            return "error"
        if lastprec > currprec:
            retstack.append(datstack[-2])
            retstack.append(datstack[-1])
            datstack.pop()
            datstack.pop()
            opToAdd = opstack.pop()
            retstack.append(opToAdd)
            return True
            
    datstack = []
    opstack = []
    retstack = []

    # simplified, need to add some extra token analysis
    for tok in tokens:
        t = getType(tok)
        if t == "data":
            datstack.append(tok)
        if t == "op":
            attemptToRetStack(tok)
            opstack.append(tok)
            
    

            
    
            
            
            
            
            
dijkstraShuntingYard([("2")])
    
    
