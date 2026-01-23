class Operation:
    def __init__(self, symbol, precedence):
        self._symbol = symbol
        self._precedence = precedence
        self._class = None
    
    def getSymbol(self):
        return self._symbol
    
    def setSymbol(self, symbol):
        self._symbol = symbol

    def getPrecedence(self):
        return self._precedence
    
    def setPrecedence(self, precedence):
        self._precedence = precedence

class ArithmeticOperation(Operation):
    def __init__(self, symbol, precedence, associativity):
        super().__init__(symbol, precedence, associativity)
        self._associativity = associativity
        
    def getAssociativity(self):
        return self._associativity
    
    def setAssociativity(self, associativity):
        self._associativity = associativity

class Add(ArithmeticOperation):
    def __init__(self):
        super().__init__(symbol="+", precedence=1, associativity="LEFT")
        self._class = "ArithmeticOperation"
        
class Subtract(ArithmeticOperation):
    def __init__(self):
        super().__init__(symbol="-", precedence=1, associativity="LEFT")
        self._class = "SubtractionOperation"

class Multiply(ArithmeticOperation):
    def __init__(self):
        super().__init__(symbol="*", precedence=2, associativity="LEFT")
        self._class = "MultiplicationOperation"

class Divide(ArithmeticOperation):
    def __init__(self):
        super().__init__(symbol="/", precedence=2, associativity=None)
        self._class = "DivideOperation"

class IntegerDivide(ArithmeticOperation):
    def __init__(self):
        super().__init__(symbol="//", precedence=2, associativity=None)
        self._class = "IntegerDivideOperation"
        
class Modulo(ArithmeticOperation):
    def __init__(self):
        super().__init__(symbol="%", precedence=2, associativity=None)
        self._class = "ModuloOperation"
        
class Exponent(ArithmeticOperation):
    def __init__(self):
        super().__init__(symbol="^", precedence=3, associativity="RIGHT")
        self._class = "ExponentOperation"
        
class LogicalOperation(Operation):
    def __init__(self, symbol, precedence):
        super().__init__(symbol, precedence)
        self._class = "LogicalOperation"
        
class And(LogicalOperation):
    def __init__(self):
        super().__init__(symbol="AND", precedence=1)
        self._class = "AndOperation"
        
class Or(LogicalOperation):
    def __init__(self):
        super().__init__(symbol="OR", precedence=1)
        self._class = "OrOperation"
        
class Not(LogicalOperation):
    def __init__(self):
        super().__init__(symbol="NOT", precedence=2)
        self._class = "NotOperation"
        
class ComparisonOperation(Operation):
    def __init__(self, symbol, precedence):
        super().__init__(symbol, precedence)
        self._class = "ComparisonOperation"

class Equal(ComparisonOperation):
    def __init__(self):
        super().__init__(symbol="==", precedence=1)
        self._class = "EqualOperation"

class NotEqual(ComparisonOperation):
    def __init__(self):
        super().__init__(symbol="!=", precedence=1)
        self._class = "NotEqualOperation"
        
class GreaterThan(ComparisonOperation):
    def __init__(self):
        super().__init__(symbol=">", precedence=1)
        self._class = "GreaterThanOperation"
        
class LessThan(ComparisonOperation):
    def __init__(self):
        super().__init__(symbol="<", precedence=1)
        self._class = "LessThanOperation"
        
class GreaterThanOrEqual(ComparisonOperation):
    def __init__(self):
        super().__init__(symbol=">=", precedence=1)
        self._class = "GreaterThanOrEqualOperation"
        
class LessThanOrEqual(ComparisonOperation):
    def __init__(self):
        super().__init__(symbol="<=", precedence=1)
        self._class = "LessThanOrEqualOperation"

class AssignmentOperation(Operation):
    def __init__(self, symbol):
        super().__init__(symbol, precedence=0)

class Assign(AssignmentOperation):
    def __init__(self):
        super().__init__(symbol="=")
        self._class = "AssignOperation"

class PlusAssign(AssignmentOperation):
    def __init__(self):
        super().__init__(symbol="+=")
        self._class = "PlusAssignOperation"
        
class MinusAssign(AssignmentOperation):
    def __init__(self):
        super().__init__(symbol="-=")
        self._class = "MinusAssignOperation"
        
class MultiplyAssign(AssignmentOperation):
    def __init__(self):
        super().__init__(symbol="*=")
        self._class = "MultiplyAssignOperation"

class DivideAssign(AssignmentOperation):
    def __init__(self):
        super().__init__(symbol="/=")
        self._class = "DivideAssignOperation"

