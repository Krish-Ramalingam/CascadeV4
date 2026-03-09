"""
Defines the operators used in the language, categorized by their functionality.
This module serves as a reference for all operators that can be used in expressions, control structures, variable declarations, and other language constructs.
"""

expressionOperators = ['+', '-', '*', '/', '%', '==', '!=', '>', '<', '>=', '<=',
                       '&&', '||', '!', '=', '+=', '-=', '*=', '/=', '%=', '&=',
                       '|=', '^=', '(', ')', '[', ']', '{', '}', '.', '->',
                       '::', '?', ':', ';']
structuralOperators = ['if', 'else', 'elif', 'for', 'while', 'do',
                       'switch', 'case', 'default', 'break', 'continue',
                       'return', 'yield', 'throw', 'catch', 'finally']
varOperators = ['var_kw', 'var', 'int',
                'float', 'hvar', 'hvar_kw']
tempOperators = ['once', 'when']
ioOperators = ['out', 'inp']

operators = expressionOperators + structuralOperators + varOperators + tempOperators + ioOperators

