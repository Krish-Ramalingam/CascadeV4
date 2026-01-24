def tokeniseArithmeticExpression(expr):
    """
    Tokenises a simple arithmetic expression into numbers and operators and variables.
    Args:
        expr (str): The arithmetic expression as a string.
    Returns:
        list: A list of tokens (numbers and operators).
    """
    tokens = []
    current_number = ''
    current_variable = ''
    
    for char in expr:
        if char.isdigit() or char == '.':
            current_number += char
        else:
            if current_number:
                if '.' in current_number:
                    tokens.append(("float", float(current_number)))
                else:
                    tokens.append(("int", int(current_number)))
                current_number = ''
            if char in '+-*/()':
                tokens.append((char, None))
            else:
                if char.isalpha():
                    current_variable += char
                else:
                    if current_variable:
                        tokens.append(("var", current_variable))
                        current_variable = ''
                        
    if current_number:
        tokens.append(("float", float(current_number)))
    if current_variable:
        tokens.append(("var", current_variable))

    return tokens

print(tokeniseArithmeticExpression("3 + 5 * (x - 2) / 7.5"))

def tokeniseLogicalExpression(expr):
    """
    Tokenises a logical expression into variables, operators, and parentheses.
    Args:
        expr (str): The logical expression as a string.
    Returns:
        list: A list of tokens (variables and operators).
    """
    tokens = []
    current_variable = ''
    
    i = 0
    while i < len(expr):
        char = expr[i]
        if char.isalpha():
            current_variable += char
        else:
            if current_variable:
                tokens.append(("var", current_variable))
                current_variable = ''
            if expr[i:i+2] in ['&&', '||', '==', '!=', '<=', '>=']:
                tokens.append((expr[i:i+2], None))
                i += 1
            elif char in '!<>()':
                tokens.append((char, None))
        i += 1

    if current_variable:
        tokens.append(("var", current_variable))

    return tokens

print(tokeniseLogicalExpression("a && (b || !c) == d"))

