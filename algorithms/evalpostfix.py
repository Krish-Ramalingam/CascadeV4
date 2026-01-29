"""
evalpostfix.py used to strict evaluate any postfix expressions iteratively rather than recursively
aim to use if space becomes an issue
"""

postExpr = [...]

def evalPostExpr(tokenisedExpr):
    
    def getType(tok):
        if tok[0] in ["var", "int", "float"]:
            return "dat"
        else:
            return "op"

    ramQueue = []
    for token in tokenisedExpr:
        if getType(token) == "dat":
            ramQueue.append(token)
        if getType(token) == "op"
            firstDat = ramQueue[0]
            secondDat = ramQueue[0]
            result = performOperation(firstDat, secondDat, token)
            ramQueue[1] = result
            ramQueue = ramQueue[1:]


# performOperation(first
