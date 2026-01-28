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
        print(opstack)
        if len(opstack) != 0:

            beneathOperation = peek(opstack)
            lastprec = getPrecedence(beneathOperation[0])
            currprec = getPrecedence(token[0])

            if currprec or lastprec == False:
                return "error"
                
            if lastprec > currprec:
                retstack.append(datstack[-2])
                retstack.append(datstack[-1])
                print("yo")
                datstack.pop()
                datstack.pop()
                opToAdd = opstack.pop()
                retstack.append(opToAdd)
                return True
            
    datstack = []
    opstack = []
    retstack = []

    for tok in tokens:
        t = getType(tok)
        print(t)
        if t == "dat":
            datstack.append(tok)
        if t == "op":
            attemptToRetStack(tok)
            opstack.append(tok)

    return (datstack, opstack, retstack)


print(dijkstraShuntingYard([
    ("int","2"), 
    ("+", None), 
    ("int", "3")
]))


    
    
