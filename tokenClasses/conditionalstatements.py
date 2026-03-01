class ConditionalStatement:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body
        
class IfStatement(ConditionalStatement):
    def __init__(self, condition, body):
        super().__init__(condition, body)
        
class WhileStatement(ConditionalStatement):
    def __init__(self, condition, body):
        super().__init__(condition, body)

class ForStatement(ConditionalStatement):
    def __init__(self, condition, body):
        super().__init__(condition, body)