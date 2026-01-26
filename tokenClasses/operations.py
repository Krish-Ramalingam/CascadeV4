class BinOp:
    def __init__(self, left, right):
        self._type = None
        self._left = left
        self._right = right
     
    def getType(self):
        return self._type
    
    def setType(self):
        return self._type


    def setLeft(self, l):
        self._left = l

    def setRight(self, r):
        self._right = r

    def getLeft(self):
        return self._left

    def getRight(self):
        return self._right
    
class AriBinOp(BinOp):
    def __init__(self, left, right):
        super.__init(self, left, right)
        self._precedence = 0
        self._associativity = "NA"
        self._symbol =  "+"

    def getPr


        
class Add(AriBinOp):
    def __init__(self, left, right):
        super.__init(self, left, right)
        self._precedence = 
        self._associativity = 
        self._symbol = 

    def getPrecedence(self):
        return self._precedence
    
    def setPrecedence(self, precedence):
        self._precedence = precedence






















































































"""
class ArithmeticOperation(BinaryOperation):
    def __init__(self, symbol, precedence, left, right, associativity):
        super().__init__(symbol, precedence, associativity)
        self._associativity = associativity
        
    def getAssociativity(self):
        return self._associativity
    
    def setAssociativity(self, associativity):
        self._associativity = associativity

class Add(ArithmeticOperation):
    def __init__(self):
        super().__init__(left, symbol="+", precedence=1, associativity="LEFT")
        self._class = "ArithmeticOperation"
        
class Subtract(ArithmeticOperation):
    def __init__(self):
        super().__init__(symbol="-", precedence=1, left, right, associativity="LEFT")
        self._class = "SubtractionOperation"

class Multiply(ArithmeticOperation):
    def __init__(self):
        super().__init__(symbol="*", precedence=2, left, right, associativity="LEFT")
        self._class = "MultiplicationOperation"

class Divide(ArithmeticOperation):
    def __init__(self):
        super().__init__(symbol="/", precedence=2, left, right associativity=None)
        self._class = "DivideOperation"

class IntegerDivide(ArithmeticOperation):
    def __init__(self):
        super().__init__(symbol="//", precedence=2, left, right associativity=None)
        self._class = "IntegerDivideOperation"
        
class Modulo(ArithmeticOperation):
    def __init__(self):
        super().__init__(symbol="%", precedence=2, left, right associativity=None)
        self._class = "ModuloOperation"
        
class Exponent(ArithmeticOperation):
    def __init__(self):
        super().__init__(symbol="^", precedence=3, left, right, associativity="RIGHT")
        self._class = "ExponentOperation"
        
class LogicalOperation(Operation):
    def __init__(self, symbol, precedence, left, right):
        super().__init__(symbol, precedence)
        self._class = "LogicalOperation"
        
class And(LogicalOperation):
    def __init__(self):
        super().__init__(symbol="AND", precedence=1, left, right)
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

add  =  Add()
"""