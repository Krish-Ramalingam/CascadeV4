class Variable:
    def __init__(self, name: str, value, scope, type):
        self._name = name
        self._value = value
        self._scope = scope
        self._type = type
        
    def getName(self):
        return self._name
        
    def getValue(self):
        return self._value
        
    def getScope(self):
        return self._scope
        
    def getType(self):
        return self._type
        
    def checkConsistency(self):
        if str(type(self._value))[8:-2] != self._type:
            return False
        return True
    
    def setValue(self, value):
        self._value = value
        
    def setType(self, type):
        self._type = type
        
    def setScope(self, scope):
        self._scope = scope
        
class Array(Variable):
    def __init__(self, name: str, value: list, scope, length: int):
        super().__init__(name, value, scope, type="ARRAY")
        self._length = length
        
class List(Variable):
    def __init__(self, name: str, value: list, scope):
        super().__init__(name, value, scope, type="LIST")
        self._contents = []

num1 = Variable(name="num1", value=3.5, scope="global", type="int")
print(num1.checkConsistency())  # Output: True
print(str(type(1))[8:-2])