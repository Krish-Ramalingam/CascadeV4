from dataReference.operators import operators

def validateVar(var):
    for char in var:
        if not (char.isalpha()):
            return False
    return True

def validateInt(int):
    if int.isnumeric(): 
        return True
    else: 
        return False

def validateFloat(float):
    for x in str(float): 
        if not (x.isnumeric() or x == '.'): 
            return False
    return True

def validateFuncName(funcName):
    for char in funcName: 
        if not (char.isalpha()): 
            return False
    return True
    
def validateToken(token):
    
    if token[1] == None:
        if token[0] in operators:
            return True
        else:
            return False
    else:
        if token[0] == "var":
            return validateVar(token[1])
        if token[0] == "int": 
            return validateInt(token[1]) 
        if token[0] == "float": 
            return validateFloat(token[1]) 
            
            