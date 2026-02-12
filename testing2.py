from servantClasses import lineLexer as l
from algorithms import dijkstra as d
from algorithms import postfixToTree as p

newLexer = l.Lexer()



expr = "3 + 4 * 2 / 1 - 5 ^ 2 ^ 3"
tokenisedExpr = newLexer.tokeniseArithmeticExpression(expr)
postfixExpr = d.dijkstraShuntingYard(tokenisedExpr)
tree = p.postFixToTree(postfixExpr)
p.printTree(tree)