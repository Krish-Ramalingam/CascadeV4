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
    
    datstack = []
    opstack = []
    
    