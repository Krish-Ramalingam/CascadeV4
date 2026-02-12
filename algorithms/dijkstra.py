def dijkstraShuntingYard(tokens):

    # Fairly complicated algorithm...
    """
    1) Iterate through the tokens, addding all data found to the datstack,
    2) For op tokens, if in ascending precedence, fine, like -+^.
    3) if not in that sequence, ie ^-, need to go back and pop stuff and append on the end
    4) Once done, reverse the opstack, and then append to the end
    """
    # hopefully extend to unary ops and can do a full program code.

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
        retstack.extend(datstack)
        opstack.reverse()
        retstack.extend(opstack)   
        
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
        return precedence[op] if op in precedence else "err"
    
    def attemptToRetStack(token, ticker):
        if len(opstack) != 0:

            beneathOperation = peek(opstack)
            lastprec = getPrecedence(beneathOperation[0])
            currprec = getPrecedence(token[0])
            if currprec == "err" or lastprec == "err":
                return "error" 
          
            if lastprec > currprec and ticker==False:
                
                retstack.append(datstack[-2])
                retstack.append(datstack[-1])
                datstack.pop()
                datstack.pop()
                opToAdd = opstack.pop()
                retstack.append(opToAdd)
                attemptToRetStack(token, True)
            if lastprec > currprec and ticker==True:
                retstack.append(datstack[-1])
                datstack.pop()
                opToAdd = opstack.pop()
                retstack.append(opToAdd)
                attemptToRetStack(token, True)
                
    datstack = []
    opstack = []
    retstack = []

    for tok in tokens:
        t = getType(tok)
        if t == "dat":
            datstack.append(tok)
            print("datstack: ", datstack)
            print("retstack: ", retstack)
        if t == "op":
            attemptToRetStack(tok, False)
            opstack.append(tok)
            print("opstack: ", opstack)
            print("retstack: ", retstack)
            
    fileRest()

    return retstack

tokens = [('int', 4), ('*', None), ('int', 2), ('-', None), ('int', 3), ('/', None), ('int', 1), ('*', None), ('int', 3), ('-', None), ('int', 5)]

dijkstraShuntingYard(tokens)