class Interpreter:
    def __init__(self):
        self.variables = {}

    def run(self, nodes):
        for node in nodes:
            self.execute(node)

    def execute(self, node):
        if isinstance(node, ExprStmtNode):
            evaluate_rpn(node.expr.rpn, self.variables)

        elif isinstance(node, VarDeclNode):
            value = evaluate_rpn(node.expr.rpn, self.variables) if node.expr else None
            self.variables[node.name] = value

        elif isinstance(node, OutNode):
            value = evaluate_rpn(node.expr.rpn, self.variables)
            print(value)

        elif isinstance(node, IfNode):
            cond = evaluate_rpn(node.cond.rpn, self.variables)
            if cond:
                for stmt in node.block:
                    self.execute(stmt)

        elif isinstance(node, WhileNode):
            while evaluate_rpn(node.cond.rpn, self.variables):
                for stmt in node.block:
                    self.execute(stmt)