from servantClasses import lineLexer as l
from algorithms import dijkstra as d
from algorithms import postfixToTree as p

newLexer = l.Lexer()

expr = "4 * 2 - 3 / 1 * 3 - 5"
tokenisedExpr = newLexer.tokeniseArithmeticExpression(expr)
print(tokenisedExpr)
postfixExpr = d.dijkstraShuntingYard(tokenisedExpr)
print(postfixExpr)
tree = p.postFixToTree(postfixExpr)
p.printTree(tree)






