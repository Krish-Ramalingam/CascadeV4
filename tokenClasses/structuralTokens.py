"""
FOR TOKEN DEFINITIONS AND CONFIGURATIONS ONLY. 20/1/2026
"""

class Token:
    def __init__(self, data):
        self._data = data
        self._type = None
    
    def getData(self):
        return self._data
    
    def setData(self, data):
        self._data = data
        
    def getType(self):
        return self._type
    
    def setType(self, type):
        self._type = type
    
    
    
class Line(Token):
    def __init__(self, data):
        super().__init__(data)
        self.setType("LINE")
        
class Block(Token):
    def __init__(self, data):
        super().__init__(data)
        self.setType("BLOCK")

line1 = Line("This is a line token.")
print(line1.getType())  # Output: LINE
print(line1.getData())  # Output: This is a line token.