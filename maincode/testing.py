from core import lexer as l
from algorithms import dijkstra as d
from algorithms import evalpostfix as e
from core import parser as p



tstream = (l.genTokStream("cascading.txt"))

parser = p.ParserNodes(tstream)
ast_nodes = parser.parse_program()
"""
for tok in tstream:
        print(tok[0], tok[1])
for node in ast_nodes:
    print(node)
"""
interpreter = p.Interpreter()
interpreter.exec_nodes(ast_nodes)
print(interpreter.hyperGraph.getNodes().__repr__())

"""
#var = tstream[0][1]
#tstream = tstream[2:]
#postTStream = d.dijkstraShuntingYard(tstream)
#print(postTStream)
#evaledTStream = e.evalPostExpr(postTStream)
#print(var, "=", evaledTStream)
"""