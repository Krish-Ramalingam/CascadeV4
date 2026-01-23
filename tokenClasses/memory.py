class GlobalMemory:
    def __init__(self):
        self._variables = {
        
        }
        
    def getVariable(self, name):
        for var in self._variables:
            if var.getName() == name:
                return var
        return None
    
    def addVariable(self, variable):
        self._variables[variable.getName()] = variable
    
    def removeVariable(self, name):
        if name in self._variables:
            del self._variables[name]
        
        
    
class LocalMemory:
    def __init__(self):
        self._variables = {
        
        }
        
    def getVariable(self, name):
        for var in self._variables:
            if var.getName() == name:
                return var
        return None
    
    def addVariable(self, variable):
        self._variables[variable.getName()] = variable
    
    def removeVariable(self, name):
        if name in self._variables:
            del self._variables[name]