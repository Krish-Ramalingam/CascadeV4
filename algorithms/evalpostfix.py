"""
evalpostfix.py used to strict evaluate any postfix expressions iteratively rather than recursively
aim to use if space becomes an issue
"""
import dijkstra as k

postExpr = [("int", 3), ("int", 2), ("int", 5), ("+", None), ("*", None)]

def performOperation(first, second, op):
    #assumption that first and second are numbers
    f = int(first[1])
    s = int(second[1])
    match op[0]:
        case "+":
            return f+s
        case "-":
            return s-f
        case "/":
            return s/f
        case "*":
            return f*s
        case "^":
            return s**f

def evalPostExpr(tokenisedExpr):
    print(tokenisedExpr)
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
            l = len(ramQueue)
            firstDat = ramQueue[-1]
            secondDat = ramQueue[-2]
            result = performOperation(firstDat, secondDat, token)
            ramQueue.pop()
            ramQueue.pop()
            ramQueue.append(("int", result))
            
            
    return ramQueue[0][1]





print(evalPostExpr((k.dijkstraShuntingYard(
    [
        ("int", 2),
        ("+", None),
        ("int", 3),
        ("^", None),
        ("int", 2),
        ("-", None),
        ("int", 6),
        ("/", None),
        ("int", 3)
    ]   
))))