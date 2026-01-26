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
        super().__init__(left, right)
        self._precedence = 0
        self._associativity = "NA"

    def getPrecedence(self):
        return self._precedence
    
    def setPrecedence(self, precedence):
        self._precedence = precedence
        
    def getAssociativity(self):
        return self._associativity
    
    def setAssociativity(self, associativity):
        self._associativity = associativity
        
class Add(AriBinOp):
    def __init__(self, left, right):
        super().__init__(left, right)
        self._precedence = 1
        self._associativity = "LEFT"
        
class Subtract(AriBinOp):
    def __init__(self, left, right):
        super().__init__(left, right)
        self._precedence = 1
        self._associativity = "LEFT"
        
class Multiply(AriBinOp):
    def __init__(self, left, right):
        super().__init__(left, right)
        self._precedence = 2
        self._associativity = "LEFT"
              
class Divide(AriBinOp):
    def __init__(self, left, right):
        super().__init__(left, right)
        self._precedence = 2
        self._associativity = "LEFT"
        
class Exponent(AriBinOp):
    def __init__(self, left, right):
        super().__init__(left, right)
        self._precedence = 3
        self._associativity = "RIGHT"
        
        
class AST:
    def __init__(self, root):
        self._root = root
        
    def getRoot(self):
        return self._root
    
    def preOrderTraversal(self, node):
        if node is not None:
            print(node.__class__.__name__)
            self.preOrderTraversal(node.getLeft())
            self.preOrderTraversal(node.getRight())
            
    def inOrderTraversal(self, node):
        if node is not None:
            self.inOrderTraversal(node.getLeft())
            print(node.__class__.__name__)
            self.inOrderTraversal(node.getRight())
            
    def postOrderTraversal(self, node):
        if node is not None:
            self.postOrderTraversal(node.getLeft())
            self.postOrderTraversal(node.getRight())
            print(node.__class__.__name__)
            
        
# Example usage:
ast = AST(Add(Multiply(None, None), Subtract(None, None)))
print("Pre-order Traversal:")
ast.preOrderTraversal(ast.getRoot())

add = Add(None, None)
print(add.getPrecedence())


# tokens to tree structure
tokenExample = [("int", 3), ("+", None), ("int", 2), ("*", None), ("int", 2)]

class TokenParser:
    def __init__(self, tokens):
        self._tokens = tokens
        
    def parse(self):
        # Simple parser implementation (for demonstration purposes)
        output_queue = []
        operator_stack = []
        
        precedence = {
            "+": 1,
            "-": 1,
            "*": 2,
            "/": 2,
            "^": 3
        }
        
        for token in self._tokens:
            if token[0] == "int":
                output_queue.append(token)
            else:
                while (operator_stack and 
                       precedence[operator_stack[-1][0]] >= precedence[token[0]]):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
        
        while operator_stack:
            output_queue.append(operator_stack.pop())
        
        return output_queue
    
    
"""
Need to convert to post order using shunting yard algorithm, then convert to a tree.
"""

















































































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