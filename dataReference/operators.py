expressionOperators = ['+', '-', '*', '/', '%', '==', '!=', '>', '<', '>=', '<=', '&&', '||', '!', '=', '+=', '-=', '*=', '/=', '%=', '&=', '|=', '^=', '(', ')', '[', ']', '{', '}', '.', '->', '::', '?', ':', ';']
structuralOperators = ['if', 'else', 'elif', 'for', 'while', 'do', 'switch', 'case', 'default', 'break', 'continue', 'return', 'yield', 'throw', 'catch', 'finally']
varOperators = ['var_kw', 'var', 'int', 'float', 'hvar', 'hvar_kw']
tempOperators = ['once', 'when']
ioOperators = ['out', 'in']
operators = expressionOperators + structuralOperators + varOperators + tempOperators + ioOperators