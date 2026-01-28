"""
evalpostfix.py used to strict evaluate any postfix expressions iteratively rather than recursively
aim to use if space becomes an issue
"""

postExpr = [...]

def evalPostExpr(expr):
    
    def getType(tok):
        if tok[0] in ["var", "int", "float"]:
            return "dat"
        else:
            return "op"
    
    ramStack = []
    for token in expr:
        if token[0] in 