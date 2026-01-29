"""
evalpostfix.py used to strict evaluate any postfix expressions iteratively rather than recursively
aim to use if space becomes an issue
"""

postExpr = [("int", 3), ("int", 2), ("int", 5), ("+", None), ("*", None)]

def performOperation(first, second, op):
    #assumption that first and second are numbers
    f = int(first[1])
    s = int(second[1])
    match op[0]:
        case "+":
            return f+s
        case "-":
            return f-s
        case "/":
            return f/s
        case "*":
            return f*s
        case "^":
            return f**s

def evalPostExpr(tokenisedExpr):
    
    def getType(tok):
        if tok[0] in ["var", "int", "float"]:
            return "dat"
        else:
            return "op"

    ramQueue = []
    for i, token in enumerate(tokenisedExpr):
        if getType(token) == "dat":
            ramQueue.append(token)
        if getType(token) == "op":
            firstDat = ramQueue[i-1]
            secondDat = ramQueue[i-2]
            print(firstDat, secondDat, token)
            result = performOperation(firstDat, secondDat, token)
            print(ramQueue, result)
            ramQueue[i] = ("int", result)
            ramQueue = ramQueue[1:]
    return ramQueue[0]



print(evalPostExpr(postExpr))